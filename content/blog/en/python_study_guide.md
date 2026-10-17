## Python Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Python study guide: about 200 questions](../../images/python_study_guide_title_img.png)

About 200 questions on Python for data engineering interviews: the language itself, the standard library, object-oriented programming, generators and decorators, concurrency, testing and packaging, Python for data work, and a set of coding problems with solutions. Examples target Python 3.12. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Language basics and data types

#### What are the main characteristics of Python?

An interpreted, dynamically typed, strongly typed, garbage-collected language that supports procedural, object-oriented and functional styles. It favors readability (significant indentation) and has a large standard library and ecosystem.

#### What does "dynamically typed" and "strongly typed" mean for Python?

Dynamically typed: a variable's type is known at run time and a name can be rebound to an object of another type. Strongly typed: Python doesn't silently convert incompatible types, so `"1" + 1` raises `TypeError` instead of guessing.

#### What are Python's built-in data types?

Numbers (`int`, `float`, `complex`, `bool`), text (`str`), sequences (`list`, `tuple`, `range`), binary (`bytes`, `bytearray`, `memoryview`), sets (`set`, `frozenset`), mappings (`dict`) and `NoneType`.

#### What is the difference between mutable and immutable objects?

Mutable objects can change in place after creation (`list`, `dict`, `set`, `bytearray`, most user classes). Immutable objects can't (`int`, `float`, `str`, `tuple`, `frozenset`, `bytes`): operations create new objects. Only hashable (usually immutable) objects can be dict keys or set members.

#### What is the difference between `is` and `==`?

`==` compares values (calls `__eq__`). `is` compares identity: whether both names refer to the same object. Use `is` only for singletons such as `None`: `if x is None`.

#### What does "everything is an object" mean in Python?

Numbers, functions, classes and modules are all objects with a type, an identity (`id()`) and attributes. Variables are names bound to objects, not boxes holding values.

#### How are arguments passed to functions in Python?

By assignment ("call by object reference"): the parameter is bound to the same object as the argument. Mutating a mutable argument is visible to the caller, rebinding the parameter isn't.

#### What is `None`?

The single instance of `NoneType`, representing the absence of a value. Functions without a `return` statement return `None`.

#### What values are falsy in Python?

`None`, `False`, zero of any numeric type, and empty collections and strings (`''`, `[]`, `{}`, `set()`, `range(0)`). Objects can define `__bool__` or `__len__` to control their truthiness.

#### What is the difference between `/` and `//`?

`/` is true division and always returns a float (`7 / 2 == 3.5`). `//` is floor division (`7 // 2 == 3`, `-7 // 2 == -4`).

#### Why is `0.1 + 0.2 != 0.3`?

Floats are binary IEEE 754 numbers, and 0.1 has no exact binary representation. Compare with `math.isclose()`, and use `decimal.Decimal` for money.

#### How big can an int be in Python?

Arbitrarily large: Python integers have unlimited precision, limited only by memory.

#### What is the walrus operator?

`:=` assigns a value inside an expression:

```python
while (line := f.readline()):
    process(line)
```

#### What is a `match` statement?

Structural pattern matching (Python 3.10+), matching values against patterns with destructuring:

```python
match event:
    case {"type": "click", "x": x, "y": y}:
        handle_click(x, y)
    case {"type": "key", "key": k}:
        handle_key(k)
    case _:
        pass
```

#### What is the difference between a list and a tuple?

Lists are mutable and meant for homogeneous collections that change. Tuples are immutable, hashable (if their items are), slightly lighter, and used for fixed records or dictionary keys.

#### What is the difference between a shallow and a deep copy?

A shallow copy (`copy.copy`, `list(x)`, `x[:]`) creates a new container holding references to the same inner objects. A deep copy (`copy.deepcopy`) recursively copies the inner objects too.

#### What is the LEGB rule?

The order in which Python resolves names: Local, Enclosing function scopes, Global (module), Built-in.

#### What do `global` and `nonlocal` do?

`global x` makes assignments in a function rebind the module-level `x`. `nonlocal x` rebinds `x` in the nearest enclosing function scope, which is needed to modify a closure variable.

#### What is the difference between a module and a package?

A module is a single `.py` file. A package is a directory of modules, normally with an `__init__.py`, imported with dotted names.

#### What does `if __name__ == "__main__":` do?

Its block runs only when the file is executed as a script, not when it's imported as a module. It is used for command-line entry points.

### Strings, collections and comprehensions

#### How do f-strings work?

Prefix a string with `f` and put expressions in braces, with optional format specs:

```python
total = 1234.5
print(f"Total: {total:,.2f} EUR, items: {len(items)}")   # Total: 1,234.50 EUR
print(f"{total=}")                                         # total=1234.5 (debugging)
```

#### Why are strings immutable, and how do you build a long string efficiently?

Immutability makes strings hashable and safe to share. Repeated `+=` in a loop creates many intermediate strings, so collect parts in a list and use `"".join(parts)`.

#### What is the difference between `str` and `bytes`?

`str` is Unicode text. `bytes` is a sequence of raw bytes. Convert with `text.encode("utf-8")` and `data.decode("utf-8")`, always naming the encoding when reading files.

#### How do slices work?

`seq[start:stop:step]`, with `stop` excluded and negative indices counting from the end. `s[::-1]` reverses a sequence, `s[-3:]` takes the last three items.

#### What is a list comprehension?

A concise way to build a list from an iterable with optional filtering:

```python
squares = [x * x for x in range(10) if x % 2 == 0]
```

#### What are dict and set comprehensions?

```python
lengths = {name: len(name) for name in names}
initials = {name[0] for name in names}
```

#### What is the difference between a list comprehension and a generator expression?

A list comprehension builds the whole list in memory. A generator expression (parentheses) yields items lazily, one at a time: `sum(x * x for x in range(10**8))` uses constant memory.

#### How is a Python dict implemented, and what are its complexities?

As a hash table: lookup, insertion and deletion are O(1) on average. Since Python 3.7, dicts preserve insertion order.

#### What is the time complexity of common list operations?

Indexing and `append` are O(1) (amortized for append), `insert(0, x)` and `pop(0)` are O(n), `x in list` is O(n), sorting is O(n log n). Use `collections.deque` for fast operations at both ends and sets for membership tests.

#### What does `dict.get()` do, and how is it different from `dict[key]`?

`d[key]` raises `KeyError` for a missing key. `d.get(key, default)` returns `default` (or `None`) instead.

#### What is `collections.defaultdict`?

A dict that creates a default value for missing keys from a factory:

```python
from collections import defaultdict
by_country = defaultdict(list)
for company in companies:
    by_country[company.country].append(company)
```

#### What is `collections.Counter`?

A dict subclass for counting hashable items, with `most_common()`:

```python
from collections import Counter
Counter("mississippi").most_common(2)   # [('i', 4), ('s', 4)]
```

#### What is a `namedtuple`, and how does it compare to a dataclass?

`namedtuple` creates an immutable tuple subclass with named fields. A `dataclass` generates `__init__`, `__repr__` and `__eq__` for a regular class: mutable by default, more flexible, with defaults, type hints and optional `frozen=True`.

#### What is `collections.deque`?

A double-ended queue with O(1) appends and pops at both ends, and an optional `maxlen` for bounded buffers.

#### How do you sort a list of dicts by a key?

```python
rows.sort(key=lambda r: (r["country"], -r["revenue"]))
top = sorted(rows, key=operator.itemgetter("revenue"), reverse=True)[:10]
```

Sorting is stable, so you can sort by several keys in successive passes.

#### What is the difference between `sort()` and `sorted()`?

`list.sort()` sorts in place and returns `None`. `sorted()` takes any iterable and returns a new list.

#### How do you merge two dicts?

`merged = a | b` (Python 3.9+), or `{**a, **b}`. Values from `b` win on duplicate keys. `a |= b` updates in place.

#### What do `zip` and `enumerate` do?

`zip(a, b)` pairs items from several iterables (stopping at the shortest, or raising with `strict=True`). `enumerate(seq, start=0)` yields `(index, item)` pairs.

#### How do you remove duplicates from a list while keeping order?

```python
unique = list(dict.fromkeys(items))
```

#### What are the set operations?

Union `a | b`, intersection `a & b`, difference `a - b`, symmetric difference `a ^ b`, and the subset test `a <= b`. Membership tests are O(1) on average.

### Functions, scope and closures

#### What are `*args` and `**kwargs`?

`*args` collects extra positional arguments into a tuple, `**kwargs` collects extra keyword arguments into a dict. At a call site, `*` and `**` unpack sequences and mappings into arguments.

#### What are keyword-only and positional-only parameters?

Parameters after `*` must be passed by keyword. Parameters before `/` must be passed by position:

```python
def connect(host, /, port=5432, *, timeout=10): ...
```

#### Why shouldn't you use a mutable default argument?

Defaults are evaluated once, when the function is defined, so a mutable default is shared between calls:

```python
def add(item, bucket=None):     # not bucket=[]
    bucket = [] if bucket is None else bucket
    bucket.append(item)
    return bucket
```

#### What is a lambda?

An anonymous function limited to one expression: `lambda x: x * 2`. Mostly used as a short `key=` argument. Use `def` for anything more complex.

#### What is a closure?

A function that remembers variables from the enclosing scope where it was defined, even after that scope has returned:

```python
def multiplier(n):
    def times(x):
        return x * n
    return times

double = multiplier(2)
double(5)   # 10
```

#### What is the late-binding closure gotcha?

Closures look up variables when called, not when defined:

```python
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]                       # [2, 2, 2]
funcs = [lambda i=i: i for i in range(3)]  # binds the current value: [0, 1, 2]
```

#### What are first-class functions?

Functions are objects: they can be assigned to variables, stored in data structures, passed as arguments and returned from other functions.

#### What are `map`, `filter` and `functools.reduce`?

`map(f, xs)` applies `f` to each item, `filter(pred, xs)` keeps items where `pred` is true (both lazy), and `reduce(f, xs, init)` folds a sequence into one value. Comprehensions are usually more readable than `map` and `filter`.

#### What does `functools.partial` do?

It creates a new function with some arguments fixed: `parse_fr = partial(parse_date, fmt="%d/%m/%Y")`.

#### What does `functools.lru_cache` (or `cache`) do?

It memoizes a function's results by its arguments (which must be hashable):

```python
from functools import cache

@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

#### What is recursion, and what is Python's recursion limit?

A function calling itself. CPython limits depth (1000 by default, `sys.getrecursionlimit()`) and has no tail-call optimization, so deep recursion is usually rewritten as a loop.

#### What are docstrings?

String literals as the first statement of a module, class or function, available as `__doc__` and shown by `help()`.

#### What is a higher-order function?

A function that takes or returns other functions, such as `sorted(key=...)`, decorators or `map`.

#### What are type hints?

Annotations of expected types that Python doesn't enforce at run time, but that tools (mypy, pyright, IDEs) check:

```python
def total(prices: list[float], vat: float = 0.2) -> float:
    return sum(prices) * (1 + vat)
```

#### What is `typing.Optional[X]`?

A hint meaning `X | None`. Since Python 3.10 you can write `X | None` directly.

#### What is the difference between a function and a method?

A method is a function defined in a class and accessed through an instance or class, which binds the first argument (`self` or `cls`) automatically.

#### How do you return multiple values from a function?

Return a tuple and unpack it: `low, high = bounds(values)`. For more than a few values, return a dataclass or named tuple.

#### What does unpacking with `*` do in assignments?

It collects the remaining items: `first, *middle, last = [1, 2, 3, 4]` gives `middle == [2, 3]`.

#### What are `any()` and `all()`?

`any(it)` is true if at least one item is truthy, `all(it)` if every item is (and true for an empty iterable). Both short-circuit.

#### How does Python evaluate `and` and `or`?

With short-circuiting, returning one of the operands rather than a bool: `x or default` returns `x` if it's truthy, else `default`.

### Object-oriented programming

#### What is the difference between a class and an instance?

A class is a blueprint that defines attributes and methods. An instance is an object created from it with its own state: `p = Point(1, 2)`.

#### What is `self`?

The first parameter of instance methods, bound to the instance the method is called on. The name is a convention, not a keyword.

#### What is `__init__`, and how does it differ from `__new__`?

`__new__` creates and returns the instance (rarely overridden, mostly for immutable types and singletons). `__init__` initializes an instance that already exists.

#### What is the difference between class attributes and instance attributes?

Class attributes are shared by all instances. Instance attributes belong to one object. Assigning through `self.x = ...` creates an instance attribute that hides the class one.

#### What are `@staticmethod` and `@classmethod`?

A static method receives no implicit first argument and is a plain function in the class namespace. A class method receives the class (`cls`), which is useful for alternative constructors:

```python
class Company:
    @classmethod
    def from_row(cls, row: dict) -> "Company":
        return cls(row["id"], row["name"])
```

#### What is `@property`?

A decorator that exposes a method as an attribute, with optional setter and deleter, so you can add validation or computation without changing the interface.

#### What is inheritance, and what does `super()` do?

A class can extend another and override its methods. `super()` calls the parent's implementation according to the method resolution order:

```python
class Lakehouse(Warehouse):
    def __init__(self, path):
        super().__init__()
        self.path = path
```

#### What is the method resolution order (MRO)?

The order Python searches classes for an attribute under multiple inheritance, computed with C3 linearization. Inspect it with `Class.__mro__`.

#### What are dunder (magic) methods?

Methods with double underscores that hook into language behavior: `__repr__`, `__str__`, `__len__`, `__eq__`, `__hash__`, `__lt__`, `__iter__`, `__getitem__`, `__enter__`, `__call__`, `__add__`.

#### What is the difference between `__str__` and `__repr__`?

`__repr__` is an unambiguous representation for developers (ideally valid code to recreate the object). `__str__` is a readable representation for users. `print()` uses `__str__` and falls back to `__repr__`.

#### What is a dataclass?

A class decorated with `@dataclass`, which generates `__init__`, `__repr__` and `__eq__` from annotated fields, with options such as `frozen=True`, `order=True` and `slots=True`:

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Snapshot:
    country: str
    rows: int
    files: list[str] = field(default_factory=list)
```

#### What are abstract base classes?

Classes deriving from `abc.ABC` with methods marked `@abstractmethod`. They can't be instantiated until a subclass implements every abstract method, which enforces an interface.

#### What is duck typing?

Using an object according to its behavior rather than its type: "if it walks like a duck…". Any object with a `read()` method can be used where a file is expected.

#### What is a Protocol?

`typing.Protocol` defines structural interfaces for static type checkers: any class with matching methods satisfies it, without inheriting from it.

#### What are `__slots__`?

A class attribute listing allowed instance attributes. It removes the per-instance `__dict__`, reducing memory use and speeding up attribute access for many small objects.

#### What is composition, and why is it often preferred to inheritance?

Building objects from other objects ("has a") instead of extending classes ("is a"). It gives looser coupling and avoids deep, fragile class hierarchies.

#### What is encapsulation in Python?

Python has no private members. By convention, `_name` is internal, and `__name` triggers name mangling (`_Class__name`) to avoid clashes in subclasses.

#### What makes an object hashable?

A `__hash__` that doesn't change during its lifetime, and an `__eq__` consistent with it (equal objects must have equal hashes). Defining `__eq__` without `__hash__` makes a class unhashable.

#### What is a metaclass?

The class of a class (by default `type`), which controls how classes are created. Rarely needed. Class decorators and `__init_subclass__` cover most use cases.

#### What is `__call__`?

A method that makes instances callable like functions, which is useful for configurable function objects.

### Iterators, generators, decorators and context managers

#### What is the difference between an iterable and an iterator?

An iterable can produce an iterator (`__iter__`), such as lists, dicts and files. An iterator yields items one by one through `__next__` and raises `StopIteration` at the end. An iterator can only be consumed once.

#### What is a generator?

A function containing `yield`. Calling it returns an iterator that runs the function lazily, pausing at each `yield` and keeping its state between calls:

```python
def read_batches(path, size=10_000):
    batch = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            batch.append(line)
            if len(batch) == size:
                yield batch
                batch = []
    if batch:
        yield batch
```

#### Why are generators useful in data engineering?

They process data as streams, with constant memory, regardless of input size: reading huge files line by line, paginating APIs, chaining transformations lazily.

#### What does `yield from` do?

It delegates to a sub-iterator, yielding all its items: `yield from read_batches(path)`.

#### What is `itertools`, and name a few useful functions?

A module of fast iterator building blocks: `chain`, `islice`, `groupby`, `product`, `permutations`, `combinations`, `accumulate`, `count`, `cycle`, `tee`, `zip_longest` and `batched` (Python 3.12).

#### How does `itertools.groupby` work, and what's the catch?

It groups consecutive items with the same key, so the input must be sorted by that key first:

```python
from itertools import groupby
for country, rows in groupby(sorted(data, key=key), key=key):
    print(country, sum(1 for _ in rows))
```

#### What is a decorator?

A callable that takes a function and returns a replacement, applied with `@`. It adds behavior (logging, timing, retries, caching, access control) without changing the function's code.

#### How do you write a decorator that keeps the original function's metadata?

Use `functools.wraps`:

```python
import functools, time

def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
    return wrapper
```

#### How do you write a decorator with arguments?

Add an outer function that receives the arguments and returns the decorator:

```python
def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    if attempt == times:
                        raise
        return wrapper
    return decorator
```

#### What is a context manager?

An object used with `with` that sets up and tears down a resource reliably: `__enter__` runs at the start, `__exit__` at the end even if an exception occurs. Files, locks and database connections are context managers.

#### How do you write a context manager with `contextlib`?

```python
from contextlib import contextmanager

@contextmanager
def transaction(conn):
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
```

#### What does `__exit__` return?

A truthy value suppresses the exception raised in the `with` block, a falsy value lets it propagate. Suppressing should be rare and deliberate.

#### What is `contextlib.ExitStack`?

A context manager that manages a dynamic number of other context managers, for example opening a variable list of files.

#### What is lazy evaluation?

Computing values only when needed. Generators, `range`, `map`, `zip` and dictionary views are lazy, which saves memory and allows infinite sequences.

#### How do you make a class iterable?

Implement `__iter__`, typically as a generator method:

```python
class Batch:
    def __init__(self, rows):
        self.rows = rows
    def __iter__(self):
        yield from self.rows
```

#### What happens if you iterate over a generator twice?

The second loop yields nothing: the generator is exhausted. Recreate it, or store the results in a list if you need them twice.

#### What is a coroutine in Python?

A function defined with `async def`, which can pause at `await` points. It runs in an event loop (asyncio) and enables concurrency for I/O-bound tasks.

#### How do you read only the first n items of an iterator?

`itertools.islice(it, n)`, which works on any iterator, including infinite ones.

#### How would you chunk an iterable into fixed-size batches?

`itertools.batched(iterable, n)` in Python 3.12+, or with `islice` in a loop for older versions.

#### What is the difference between `return` and `yield` in a function?

`return` ends the function and gives back one value. `yield` turns the function into a generator that produces a series of values over time, resuming where it left off.

### Errors, files and the standard library

#### How does exception handling work in Python?

```python
try:
    value = int(raw)
except ValueError as exc:
    log.warning("bad value %r: %s", raw, exc)
    value = None
else:
    log.debug("parsed")         # runs if no exception
finally:
    cleanup()                   # always runs
```

#### Why should you avoid a bare `except:`?

It also catches `KeyboardInterrupt`, `SystemExit` and programming errors, hiding bugs. Catch the specific exceptions you can handle, or at most `Exception`.

#### How do you define a custom exception?

Subclass `Exception` (or a more specific built-in), usually with a project-level base class:

```python
class PipelineError(Exception):
    """Base class for pipeline failures."""

class SchemaDriftError(PipelineError):
    pass
```

#### What is exception chaining?

`raise NewError(...) from exc` keeps the original exception as the cause, so the traceback shows both. `from None` hides the original.

#### What are exception groups?

Python 3.11 added `ExceptionGroup` to raise several exceptions at once (for example from concurrent tasks) and `except*` to handle them by type.

#### What is EAFP versus LBYL?

"Easier to ask forgiveness than permission" (try the operation and catch the error) versus "Look before you leap" (check first). EAFP is idiomatic in Python and avoids race conditions between the check and the action.

#### How do you read a large file without loading it into memory?

Iterate over the file object, which yields one line at a time:

```python
with open("big.csv", encoding="utf-8") as f:
    for line in f:
        process(line)
```

#### Why should you always use `with` when opening files?

It guarantees the file is closed, even if an exception occurs, releasing the handle and flushing buffered writes.

#### What is `pathlib`?

An object-oriented API for file paths: `Path("data") / "raw" / "file.csv"`, `.exists()`, `.glob("*.csv")`, `.read_text()`, `.suffix`, `.stem`, `.mkdir(parents=True, exist_ok=True)`.

#### How do you read and write CSV files with the standard library?

```python
import csv

with open("in.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name"])
    writer.writeheader()
    writer.writerows(rows)
```

#### How do you work with JSON?

`json.loads`/`json.dumps` for strings, `json.load`/`json.dump` for files. Pass `default=` to serialize unsupported types such as dates, and `ensure_ascii=False` to keep accented characters readable.

#### How do you parse and format dates?

With `datetime`:

```python
from datetime import datetime, timezone
d = datetime.strptime("15/10/2026", "%d/%m/%Y")
d.isoformat()                                  # '2026-10-15T00:00:00'
datetime.now(timezone.utc)                     # timezone-aware
```

`zoneinfo.ZoneInfo("Europe/Paris")` gives IANA time zones.

#### What is the difference between naive and aware datetimes?

A naive datetime has no time zone, an aware one has `tzinfo`. Mixing them raises errors. Store and compute in UTC with aware datetimes, and convert only for display.

#### How do you use the `logging` module properly?

Create a module logger with `logging.getLogger(__name__)`, log with lazy formatting (`log.info("loaded %d rows", n)`), configure handlers and levels once at the application entry point, and use `log.exception()` inside `except` blocks to include the traceback.

#### What is `argparse` used for?

Building command-line interfaces with arguments, options, types, defaults and automatic `--help`.

#### What does the `re` module offer?

Regular expressions: `re.search`, `re.match`, `re.fullmatch`, `re.findall`, `re.sub`, `re.split`, compiled patterns, and named groups:

```python
m = re.fullmatch(r"(?P<code>\d{2})\.(?P<sub>\d{2})", "03.11")
m["code"]   # '03'
```

#### How do you run an external command from Python?

With `subprocess.run`, passing a list of arguments (no shell) and checking the result:

```python
result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
```

#### How do you hash data or files in Python?

With `hashlib`: `hashlib.sha256(data).hexdigest()`. For files, read in chunks and call `update()` to keep memory constant.

#### What is `tempfile` used for?

Creating temporary files and directories that are cleaned up automatically: `with tempfile.TemporaryDirectory() as tmp: ...`.

#### How do you compress or decompress files in Python?

The `gzip`, `bz2`, `lzma` and `zipfile` modules. `gzip.open(path, "rt", encoding="utf-8")` reads a gzipped text file line by line.

### Concurrency and performance

#### What is the GIL?

The Global Interpreter Lock in CPython lets only one thread execute Python bytecode at a time. Threads still help for I/O-bound work, because the GIL is released while waiting, but not for CPU-bound pure-Python code. Python 3.13 introduced an optional free-threaded build without the GIL.

#### What is the difference between threading, multiprocessing and asyncio?

- **threading:** several threads in one process. Good for I/O-bound tasks (network, disk), limited by the GIL for CPU work.
- **multiprocessing:** several processes, each with its own interpreter. Good for CPU-bound work, with higher overhead and data passed by pickling.
- **asyncio:** cooperative concurrency in one thread with an event loop, for very many concurrent I/O operations.

#### What is `concurrent.futures`?

A high-level interface with `ThreadPoolExecutor` and `ProcessPoolExecutor`:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=8) as pool:
    pages = list(pool.map(fetch, urls))
```

#### How does asyncio work?

An event loop runs coroutines. At each `await` on an I/O operation, the coroutine yields control so others can run. `asyncio.gather` runs several at once:

```python
import asyncio

async def main(urls):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(fetch(session, u) for u in urls))

asyncio.run(main(urls))
```

#### What is a race condition, and how do you prevent one in threads?

Two threads accessing shared data and producing a result that depends on timing. Prevent it with locks (`threading.Lock`), thread-safe queues (`queue.Queue`), or by avoiding shared mutable state.

#### How do you limit concurrency when calling a rate-limited API?

Bound the worker pool size, or use `asyncio.Semaphore`, and add backoff with retries on 429 responses.

#### How do you profile Python code?

`cProfile` (`python -m cProfile -s cumtime script.py`) for function-level time, `timeit` for small snippets, `tracemalloc` for memory, and sampling profilers such as py-spy for running processes.

#### What makes Python code faster in practice?

Better algorithms and data structures (sets and dicts for lookups), built-in functions and comprehensions instead of manual loops, vectorized libraries (NumPy, pandas, Polars) for bulk numeric work, avoiding repeated work (caching), and moving heavy work to compiled code or a distributed engine.

#### Why is iterating over a pandas DataFrame row by row slow?

Each row becomes a Python object and the work happens in the interpreter. Vectorized operations run in optimized C code over whole columns at once.

#### What is memory leak-like behavior in Python, and how do you find it?

Memory that keeps growing because references are kept (global caches, lists that grow, reference cycles with `__del__`). Investigate with `tracemalloc`, `gc` and `objgraph`.

#### How does Python manage memory?

Reference counting frees most objects immediately when their count drops to zero, and a cyclic garbage collector (`gc`) cleans up reference cycles.

#### What is `__pycache__`?

The folder where Python caches compiled bytecode (`.pyc` files) of imported modules, to speed up later imports.

#### What is the difference between CPython and PyPy?

CPython is the reference interpreter, written in C. PyPy is an alternative implementation with a JIT compiler that speeds up long-running pure-Python code but is less compatible with C extensions.

#### When would you use multiprocessing over Spark?

For CPU-bound work that fits on one machine and in memory. Use Spark when data or computation exceeds one machine, or when the platform already runs on Spark.

#### What is pickling, and what are its risks?

Serializing Python objects to bytes with `pickle`. Never unpickle untrusted data: it can execute arbitrary code. Use JSON or Parquet for data exchange.

#### Why can't a lambda be sent to a process pool?

`ProcessPoolExecutor` pickles the function to send it to workers, and lambdas and nested functions can't be pickled by reference. Use module-level functions.

#### What is a daemon thread?

A background thread that doesn't prevent the program from exiting. It is killed abruptly at exit, so it shouldn't hold resources that need cleaning up.

#### How do you set a timeout on a blocking network call?

Pass a timeout to the library (`requests.get(url, timeout=30)`). Never call external services without one: a hung connection otherwise blocks forever.

#### How does `asyncio.run` differ from calling a coroutine directly?

Calling an `async def` function only creates a coroutine object. `asyncio.run(coro)` creates an event loop, runs the coroutine to completion and closes the loop.

#### What is backpressure, and how do you handle it in Python pipelines?

When producers are faster than consumers, memory grows until something breaks. Use bounded queues (`queue.Queue(maxsize=...)`, `asyncio.Queue(maxsize=...)`) so producers wait.

### Typing, packaging, environments and testing

#### What is a virtual environment, and why use one?

An isolated Python installation with its own packages (`python -m venv .venv`), so each project has its own dependency versions and doesn't break the system Python or other projects.

#### What is `pyproject.toml`?

The standard configuration file for Python projects: build system, project metadata, dependencies, entry points, and tool settings (pytest, ruff, mypy).

#### How do you make dependency installs reproducible?

Pin exact versions in a lock file (`uv lock`, `pip-tools`, Poetry), install from it in CI and production, and update dependencies deliberately.

#### What is `uv`?

A fast Python package and project manager written in Rust that replaces pip, pip-tools and virtualenv workflows (`uv add`, `uv sync`, `uv run`) and can install Python versions.

#### What is a wheel?

A built distribution format (`.whl`) that installs without a build step. Databricks jobs, for example, run code packaged as wheels.

#### What is an entry point?

A console script declared in `pyproject.toml` that installs a command which calls a Python function:

```toml
[project.scripts]
registry-lakehouse = "registry_lakehouse.cli:main"
```

#### What is pytest, and why is it preferred to unittest?

A testing framework where tests are plain functions with plain `assert`s, with detailed failure messages, fixtures, parametrization and a large plugin ecosystem.

#### What are pytest fixtures?

Functions that provide test dependencies (data, connections, a Spark session), injected by argument name, with scopes (function, module, session) and teardown after `yield`:

```python
@pytest.fixture(scope="session")
def spark():
    session = SparkSession.builder.master("local[2]").getOrCreate()
    yield session
    session.stop()
```

#### What is parametrization in pytest?

Running one test with several inputs:

```python
@pytest.mark.parametrize("raw, expected", [("311.0", "03.11"), ("4782", "47.82")])
def test_nace(raw, expected):
    assert nace_from_numeric(raw) == expected
```

#### What is mocking, and how do you do it?

Replacing a dependency with a fake object in a test, to isolate the code and avoid network or database calls: `unittest.mock.patch`, `MagicMock`, or pytest's `monkeypatch`.

#### What is property-based testing?

Generating many random inputs to check that a property always holds, instead of writing examples by hand. Hypothesis is the Python library for it, and it shrinks failures to a minimal example.

#### What is test coverage, and is 100% a good goal?

The share of code executed by tests (`pytest-cov`). It shows untested areas, but high coverage doesn't prove tests check the right things. Aim for meaningful tests of risky logic.

#### What is the difference between unit, integration and end-to-end tests?

Unit tests check one function or class in isolation. Integration tests check components working together (code plus a database). End-to-end tests run the whole system on realistic inputs.

#### What tools keep Python code quality high?

A formatter and linter (ruff, or black and flake8), a type checker (mypy, pyright), pre-commit hooks, tests in CI, and code review.

#### How do you check types with mypy?

Add type hints and run `mypy src/`. It reports type inconsistencies statically, before run time. Adopt it gradually with per-module settings.

#### What is `TypedDict`?

A typing construct that describes dictionaries with a fixed set of keys and value types, useful for JSON-like records.

#### What are generics in type hints?

Parameterized types such as `list[int]` or `dict[str, float]`, and your own generic classes and functions. Python 3.12 has a compact syntax: `def first[T](xs: list[T]) -> T: ...`.

#### How do you manage configuration and secrets in a Python application?

Read them from environment variables or a secrets manager at start-up, validate them (for example with pydantic-settings), keep `.env` files out of version control, and never hard-code credentials.

#### What is pydantic?

A data validation library that parses data into typed models and raises clear errors for invalid input. It is used for API payloads, configuration and contracts.

#### How do you structure a Python project for a data pipeline?

A `src/` layout with a package split by responsibility (ingestion, transformations, quality, io), a thin CLI entry point, configuration separate from code, tests mirroring the package, and `pyproject.toml` for dependencies and tooling.

### Python for data engineering

#### How do you read a large CSV with pandas without running out of memory?

Read in chunks, select only needed columns, set compact dtypes, or use a columnar format and a lazy engine:

```python
for chunk in pd.read_csv("big.csv", usecols=["id", "amount"], dtype={"id": "int64"}, chunksize=500_000):
    process(chunk)
```

#### What is the difference between `loc` and `iloc` in pandas?

`loc` selects by labels (index values and column names, end inclusive). `iloc` selects by integer position (end exclusive).

#### How do you avoid `SettingWithCopyWarning` in pandas?

Use `.loc[row_selector, column] = value` on the original DataFrame, or take an explicit `.copy()` when you mean to work on a subset. With copy-on-write (the default in pandas 3), chained assignment simply doesn't modify the original.

#### How do you group and aggregate in pandas?

```python
summary = (df.groupby(["country", "industry"], as_index=False)
             .agg(companies=("id", "count"), employees=("employees", "sum")))
```

#### What are the join types in `pandas.merge`?

`how="inner"`, `"left"`, `"right"`, `"outer"` and `"cross"`, on `on=` or `left_on`/`right_on` columns. `validate="one_to_one"` or `"many_to_one"` catches unexpected duplicate keys, and `indicator=True` shows each row's origin.

#### How do you handle missing values in pandas?

Detect them with `isna()`, drop them with `dropna()`, fill them with `fillna()` or `ffill()`, and use nullable dtypes (`Int64`, `string`, `boolean`) so integers with missing values don't become floats.

#### What is Apache Parquet, and why is it preferred to CSV?

A columnar, compressed, typed file format. Queries read only the columns they need, files are much smaller, types are preserved and statistics allow skipping data. CSV is row-based text with no types.

#### What is Apache Arrow?

A standard in-memory columnar format. It lets pandas, Polars, DuckDB, Spark and others exchange data without copying or converting it. PyArrow is its Python library.

#### What is Polars, and when would you use it instead of pandas?

A DataFrame library written in Rust, multi-threaded, with a lazy query optimiser. It's often much faster and more memory-efficient than pandas for large single-machine workloads.

#### What is DuckDB?

An embedded analytical SQL database. It queries Parquet, CSV and DataFrames directly and very fast, without a server: `duckdb.sql("select country, count(*) from 'data/*.parquet' group by 1")`.

#### How do you call a REST API robustly from Python?

Use a session, set timeouts, retry transient errors with exponential backoff, handle pagination, respect rate limits, and validate responses:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=Retry(total=5, backoff_factor=1,
                                                         status_forcelist=[429, 500, 502, 503, 504])))
resp = session.get(url, params={"page": 1}, timeout=30)
resp.raise_for_status()
```

#### How do you download a large file without loading it into memory?

Stream it in chunks:

```python
with requests.get(url, stream=True, timeout=60) as r:
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
```

#### How do you connect to a database from Python safely?

With a driver (psycopg for PostgreSQL) or SQLAlchemy, using parameterized queries, never string formatting, to avoid SQL injection:

```python
cur.execute("select * from companies where country = %s", (country,))
```

#### How do you load many rows into PostgreSQL quickly from Python?

Use `COPY` (psycopg's `cursor.copy()`) rather than row-by-row inserts, or batch inserts with `executemany` and page sizes. Wrap the load in one transaction.

#### What is SQLAlchemy?

A database toolkit with a Core layer (SQL expression language, connection pooling, engines) and an ORM. pandas uses SQLAlchemy engines for `read_sql` and `to_sql`.

#### How do you read files from Amazon S3 in Python?

With boto3 (`s3.get_object`, `download_file`, paginators for listing), or through fsspec and s3fs so pandas, Polars and PyArrow read `s3://` paths directly. Credentials should come from roles or environment, never code.

#### How do you make a data pipeline step idempotent?

Running it twice with the same input must give the same result: write to a deterministic location and overwrite it (or merge on keys) instead of appending, use run IDs, and check whether the work was already done.

#### How would you validate a dataset in Python before loading it?

Check the schema (columns and types), nulls in required fields, value ranges, uniqueness of keys and row counts against expectations, with code, pydantic or a library like pandera or Great Expectations. Fail loudly or quarantine bad rows.

#### What is PySpark, and how does it relate to Python?

The Python API for Apache Spark. Python code builds a query plan that runs on the JVM across a cluster, so DataFrame operations are distributed and optimized. Python UDFs run in Python workers and are much slower than built-in functions.

#### Why are Python UDFs slow in PySpark, and what are the alternatives?

Each row is serialized between the JVM and Python. Prefer built-in functions in `pyspark.sql.functions`, then pandas UDFs (vectorized with Arrow) if custom Python is unavoidable.

#### How do you handle encoding problems when reading files?

Pass the right `encoding` explicitly, use `errors="replace"` only knowingly, detect a BOM with `encoding="utf-8-sig"`, and repair mojibake (`'TravesÃ­a'.encode('latin-1').decode('utf-8')`) with a guard for strings where the round trip fails.

#### How do you schedule and orchestrate Python pipelines?

With an orchestrator such as Airflow, Dagster or Prefect (dependencies, retries, alerts, backfills), or a cloud scheduler triggering serverless functions or containers for simple cases.

#### How do you process a JSON file that is too large to load at once?

Prefer newline-delimited JSON and read it line by line. For one huge JSON array, use a streaming parser such as ijson to iterate over elements without loading everything.

#### What is the difference between ETL and ELT from a Python developer's point of view?

In ETL, Python code transforms data before loading it. In ELT, Python mainly extracts and loads raw data, and transformations run as SQL in the warehouse (often with dbt). Python remains for what SQL handles poorly: APIs, files, complex parsing.

#### How do you write a Parquet file partitioned by a column?

```python
import pyarrow as pa, pyarrow.parquet as pq
pq.write_to_dataset(pa.Table.from_pandas(df), root_path="out/", partition_cols=["country"])
```

This creates folders such as `out/country=FR/`, which query engines can prune.

### Coding problems

#### Parse a log file and report how long a device was on, and when errors happened.

Each line looks like `Jul 11 16:11:51:490 [139681125603136] dut: Device State: ON`. Only `ON`, `ERR` and `OFF` messages matter. The report should say how long the device was on and list the timestamps of the error events.

```python
from datetime import datetime

def device_report(path: str) -> str:
    start = end = None
    errors = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "Device State:" not in line:
                continue
            month, day, clock = line.split()[:3]          # 'Jul', '11', '16:11:51:490'
            stamp = f"{month} {day} {clock}"
            state = line.rsplit(":", 1)[1].strip()
            when = datetime.strptime(stamp, "%b %d %H:%M:%S:%f")
            if state == "ON" and start is None:
                start = when
            elif state == "ERR":
                errors.append(stamp)
            elif state == "OFF" and start is not None:
                end = when
                break
    lines = []
    if start and end:
        lines.append(f"Device was on for {int((end - start).total_seconds())} seconds")
    lines.append("Timestamps of error events:")
    lines += [f"    {stamp}" for stamp in errors]
    return "\n".join(lines)
```

The timestamp is the first three fields of the line (month, day, time), not the third field alone. Parsing it with `strptime` (`%f` accepts the milliseconds) gives a datetime, and subtracting two datetimes gives a `timedelta`. Note also `errors.append()` (lists have no `add`), iterating directly over the file object, and checking the state at the end of the line so that `ON` isn't matched inside another word.

#### Reverse a string, and check whether it is a palindrome ignoring case and punctuation.

```python
def is_palindrome(text: str) -> bool:
    letters = [c.lower() for c in text if c.isalnum()]
    return letters == letters[::-1]
```

#### Find the two numbers in a list that add up to a target (two-sum).

Use a dict of values already seen for O(n):

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i
    return None
```

#### Count word frequencies in a text and return the top ten.

```python
import re
from collections import Counter

def top_words(text: str, n: int = 10) -> list[tuple[str, int]]:
    return Counter(re.findall(r"\w+", text.lower())).most_common(n)
```

#### Flatten an arbitrarily nested list.

```python
def flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

list(flatten([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]
```

#### Group a list of anagrams.

```python
from collections import defaultdict

def group_anagrams(words: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())
```

#### Deduplicate records, keeping the most recent version of each key.

```python
def latest_by_key(rows: list[dict], key: str, ts: str) -> list[dict]:
    latest = {}
    for row in rows:
        current = latest.get(row[key])
        if current is None or row[ts] > current[ts]:
            latest[row[key]] = row
    return list(latest.values())
```

#### Merge overlapping intervals.

```python
def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged
```

#### Check whether a string of brackets is balanced.

```python
def balanced(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for c in s:
        if c in "([{":
            stack.append(c)
        elif c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
    return not stack
```

#### Implement a function that splits a list into chunks of size n.

```python
def chunks(items: list, n: int) -> list[list]:
    return [items[i:i + n] for i in range(0, len(items), n)]
```

#### Find the first non-repeating character in a string.

```python
from collections import Counter

def first_unique(s: str) -> str | None:
    counts = Counter(s)
    return next((c for c in s if counts[c] == 1), None)
```

#### Validate a French SIREN number with the Luhn algorithm.

```python
def luhn_valid(number: str) -> bool:
    if not number.isdigit():
        return False
    total = 0
    for i, d in enumerate(reversed(number)):
        n = int(d)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0
```

#### Compute a running (cumulative) total and a 3-item moving average.

```python
from itertools import accumulate

values = [3, 5, 2, 8, 6]
running = list(accumulate(values))                                         # [3, 8, 10, 18, 24]
moving = [sum(values[i - 2:i + 1]) / 3 for i in range(2, len(values))]     # [3.33, 5.0, 5.33]
```

#### Read a CSV of transactions and compute the total amount per user and the cities whose average exceeds 8,000.

```python
import csv
from collections import defaultdict

totals = defaultdict(float)
city_sum, city_count = defaultdict(float), defaultdict(int)
with open("transactions.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter=";"):
        amount = float(row["amount"])
        totals[row["user_id"]] += amount
        city_sum[row["city"]] += amount
        city_count[row["city"]] += 1

rich_cities = {c: city_sum[c] / city_count[c] for c in city_sum if city_sum[c] / city_count[c] > 8000}
```

#### Write a generator that yields Fibonacci numbers indefinitely, and take the first ten.

```python
from itertools import islice

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

list(islice(fibonacci(), 10))   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```
