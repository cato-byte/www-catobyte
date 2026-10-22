## Python Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Python study guide: about 220 questions](../../images/python_study_guide_title_img.png)

About 220 questions on Python for data engineering interviews: the language itself, the standard library, object-oriented programming, generators and decorators, concurrency, testing and packaging, Python for data work, and a set of coding problems with solutions. Examples target Python 3.12 and later, and the answers cover what changed up to Python 3.15 (October 2026).

The guide follows a learning path in four stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Language basics and data types

<!-- unit: Python's object model -->

<!-- goals -->

- Explain dynamic and strong typing and "everything is an object".
- Distinguish mutable and immutable objects, identity and equality, and how arguments are passed.

<!-- concept -->

Python names are labels attached to objects, not boxes holding values. A name can be re-pointed to an object of any type (dynamic typing), but objects never silently change type (strong typing). Every object has an identity, a type and a value.

Mutability decides what happens when two names share an object. Changing a mutable object through one name is visible through the other; immutable objects can only be replaced. Function arguments follow the same rule: the parameter is another label on the caller's object.

<!-- example -->

```python
def add_tag(tags):
    tags.append("new")      # mutates the caller's list

my_tags = ["a"]
add_tag(my_tags)
print(my_tags)              # ['a', 'new']

x = 1000; y = 1000
print(x == y, x is y)       # True, and identity is an implementation detail
```

#### What are the main characteristics of Python?

An interpreted, dynamically typed, strongly typed, garbage-collected language that supports procedural, object-oriented and functional styles. It favors readability (significant indentation) and has a large standard library and ecosystem.

#### What do "dynamically typed" and "strongly typed" mean for Python?

Dynamically typed: a variable's type is known at run time and a name can be rebound to an object of another type. Strongly typed: Python doesn't silently convert incompatible types, so `"1" + 1` raises `TypeError` instead of guessing.

#### What does "everything is an object" mean in Python?

Numbers, functions, classes and modules are all objects with a type, an identity (`id()`) and attributes. Variables are names bound to objects, not boxes holding values.

#### What is the difference between mutable and immutable objects?

Mutable objects can change in place after creation (`list`, `dict`, `set`, `bytearray`, most user classes). Immutable objects can't (`int`, `float`, `str`, `tuple`, `frozenset`, `bytes`): operations create new objects. Only hashable (usually immutable) objects can be dict keys or set members.

#### What is the difference between `is` and `==`?

`==` compares values (calls `__eq__`). `is` compares identity: whether both names refer to the same object. Use `is` only for singletons such as `None`: `if x is None`.

#### How are arguments passed to functions in Python?

By assignment ("call by object reference"): the parameter is bound to the same object as the argument. Mutating a mutable argument is visible to the caller, rebinding the parameter isn't.

#### What is `None`?

The single instance of `NoneType`, representing the absence of a value. Functions without a `return` statement return `None`.

<!-- challenge -->

A function receives a dict of settings, sets `settings["debug"] = True` for its own use, and other parts of the program start logging in debug mode. Why, and how do you fix it?

<!-- solution -->

The function mutated the caller's dict, shared by everyone. Copy it before changing (`local = {**settings, "debug": True}`) or pass the flag as a separate argument.

<!-- takeaways -->

- Names are labels on objects.
- Mutating shared objects affects every name.
- Use `==` for values, `is` for identity (and `None`).

<!-- unit: Numbers and truthiness -->

<!-- goals -->

- Know Python's built-in types and what counts as falsy.
- Handle division, float precision and big integers correctly.

<!-- concept -->

Python's built-in types cover most needs without imports: numbers, text, sequences, mappings and sets. Every object also has a truth value, which makes conditions concise but can hide bugs, since zero and empty collections are false just like `None`.

Numbers have their own traps. True division always gives a float; floor division rounds down, even for negatives. Floats are binary approximations, so money needs `Decimal`, while integers simply grow as large as memory allows.

<!-- example -->

```python
from decimal import Decimal
print(7 / 2, 7 // 2, -7 // 2)            # 3.5 3 -4
print(0.1 + 0.2 == 0.3)                  # False
print(Decimal("0.1") + Decimal("0.2"))   # 0.3
count = 0
if not count:                            # also true for None, [], ""
    print("zero or missing?")
```

#### What are Python's built-in data types?

Numbers (`int`, `float`, `complex`, `bool`), text (`str`), sequences (`list`, `tuple`, `range`), binary (`bytes`, `bytearray`, `memoryview`), sets (`set`, `frozenset`), mappings (`dict`) and `NoneType`.

#### What values are falsy in Python?

`None`, `False`, zero of any numeric type, and empty collections and strings (`''`, `[]`, `{}`, `set()`, `range(0)`). Objects can define `__bool__` or `__len__` to control their truthiness.

#### What is the difference between `/` and `//`?

`/` is true division and always returns a float (`7 / 2 == 3.5`). `//` is floor division (`7 // 2 == 3`, `-7 // 2 == -4`).

#### Why is `0.1 + 0.2 != 0.3`?

Floats are binary IEEE 754 numbers, and 0.1 has no exact binary representation. Compare with `math.isclose()`, and use `decimal.Decimal` for money.

#### How big can an int be in Python?

Arbitrarily large: Python integers have unlimited precision, limited only by memory.

<!-- challenge -->

`if not discount:` treats a discount of 0 the same as a missing discount, and orders without discount get the default 10%. Fix the condition.

<!-- solution -->

Test for missing explicitly: `if discount is None: discount = 0.10`, so a real value of 0 stays 0.

<!-- takeaways -->

- Zero, empty and `None` are all falsy.
- `//` floors; `/` returns floats.
- Use `Decimal` for exact decimal arithmetic.

<!-- unit: Modern syntax -->

<!-- goals -->

- Use the walrus operator and structural pattern matching.
- Choose lists or tuples and make shallow or deep copies.

<!-- concept -->

Recent Python versions added syntax that removes common boilerplate. The walrus operator assigns inside an expression, which tidies read-and-test loops. Pattern matching checks structure and extracts values at the same time, useful for messages with different shapes.

Two older choices still matter daily: lists for collections that change, tuples for fixed records, and copies that duplicate only the outer container versus the whole nested structure.

<!-- example -->

```python
import copy
match event:
    case {"type": "order", "id": int(order_id)}:
        handle_order(order_id)
    case {"type": "refund", "amount": amount} if amount > 0:
        handle_refund(amount)
    case _:
        log.warning("unknown event %r", event)

config = {"retries": [1, 2]}
shallow = copy.copy(config); deep = copy.deepcopy(config)
shallow["retries"].append(3)        # also changes config!
```

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

<!-- challenge -->

A test copies a nested config with `dict(config)` and modifies a nested list, and later tests fail. What happened?

<!-- solution -->

`dict(config)` is a shallow copy: the nested list is shared, so the change leaked into the original. Use `copy.deepcopy(config)` for nested structures.

<!-- takeaways -->

- `:=` assigns inside expressions.
- `match` checks structure and extracts values.
- Shallow copies share nested objects.

<!-- unit: Names, modules and scripts -->

<!-- goals -->

- Explain the LEGB rule, global and nonlocal.
- Distinguish modules and packages and use the `__main__` guard.

<!-- concept -->

When Python sees a name, it looks in four places in order: the local function, enclosing functions, the module, then built-ins. Assigning to a name inside a function makes it local unless declared otherwise, which is the source of the classic "referenced before assignment" error.

Code is organized in modules (files) and packages (directories of modules). The `__main__` guard lets one file work both as an importable module and as a script, without running script code on import.

<!-- example -->

```python
counter = 0
def bump():
    global counter          # without this: UnboundLocalError
    counter += 1

def main():
    bump(); print(counter)

if __name__ == "__main__":  # runs only as a script, not on import
    main()
```

#### What is the LEGB rule?

The order in which Python resolves names: Local, Enclosing function scopes, Global (module), Built-in.

#### What do `global` and `nonlocal` do?

`global x` makes assignments in a function rebind the module-level `x`. `nonlocal x` rebinds `x` in the nearest enclosing function scope, which is needed to modify a closure variable.

#### What is the difference between a module and a package?

A module is a single `.py` file. A package is a directory of modules, normally with an `__init__.py`, imported with dotted names.

#### What does `if __name__ == "__main__":` do?

Its block runs only when the file is executed as a script, not when it's imported as a module. It is used for command-line entry points.

#### How does Python find a module when you import it?

It first checks `sys.modules`: a module already imported is reused, so its top-level code runs only once per process. Otherwise it searches the directories in `sys.path`: the script's directory (or the current one), `PYTHONPATH`, the standard library and site-packages. A local file named `json.py` or `pandas.py` shadows the real module, and since 3.13 the error message points this out.

#### What are lazy imports?

Python 3.15 adds `lazy import json` and `lazy from pathlib import Path` (PEP 810): the module is loaded only when the name is first used, which shortens the start-up time of command-line tools and large applications. `lazy` is allowed only at module level, not inside functions, classes or `try` blocks. On older versions, the workaround is to import inside the function that needs the module.

<!-- challenge -->

Importing a helper module in a test starts a 10-minute data load. Why, and how do you fix it?

<!-- solution -->

The module runs its load at the top level, which executes on import. Move it into a `main()` function called under `if __name__ == "__main__":`.

<!-- takeaways -->

- Names resolve Local, Enclosing, Global, Built-in.
- Assignment makes names local unless declared.
- Guard script code with `__main__`.

### Strings, collections and comprehensions

<!-- unit: Strings and bytes -->

<!-- goals -->

- Format, slice and build strings efficiently.
- Distinguish text from bytes and solve classic string problems.

<!-- concept -->

Strings are immutable sequences of Unicode characters. Immutability makes them safe to share and use as dict keys, but it means every change creates a new string, so building long text with repeated concatenation is slow and joining a list is the idiom.

Text becomes bytes when it leaves the program, through files or networks, so encoding is explicit. Slicing, with its exclusive stop and negative indices, solves many interview problems in one line.

<!-- example -->

```python
name, total = "Ana", 1234.5
print(f"{name:<6}|{total:>10,.2f}|")     # Ana   |  1,234.50|
parts = [f"{i}" for i in range(5)]
print(",".join(parts))                   # efficient building
data = "café".encode("utf-8")            # b'caf\xc3\xa9'
print("racecar"[::-1])                   # reverse with a slice
```

#### How do f-strings work?

Prefix a string with `f` and put expressions in braces, with optional format specs:

```python
total = 1234.5
print(f"Total: {total:,.2f} EUR, items: {len(items)}")   # Total: 1,234.50 EUR
print(f"{total=}")                                         # total=1234.5 (debugging)
```

#### What are template strings (t-strings)?

Python 3.14 added `t"..."` literals (PEP 750). They look like f-strings but evaluate to a `string.templatelib.Template` object, not a `str`: the static parts and the interpolated values stay separate, so a library can escape or parameterize the values before combining them, for example to build safe SQL or HTML.

```python
name = "O'Brien"
query = t"SELECT * FROM users WHERE name = {name}"
query.strings   # ('SELECT * FROM users WHERE name = ', '')
query.values    # ("O'Brien",)
```

#### Why are strings immutable, and how do you build a long string efficiently?

Immutability makes strings hashable and safe to share. Repeated `+=` in a loop creates many intermediate strings, so collect parts in a list and use `"".join(parts)`.

#### What is the difference between `str` and `bytes`?

`str` is Unicode text. `bytes` is a sequence of raw bytes. Convert with `text.encode("utf-8")` and `data.decode("utf-8")`, always naming the encoding when reading files.

#### How do slices work?

`seq[start:stop:step]`, with `stop` excluded and negative indices counting from the end. `s[::-1]` reverses a sequence, `s[-3:]` takes the last three items.

#### Reverse a string, and check whether it is a palindrome ignoring case and punctuation.

```python
def is_palindrome(text: str) -> bool:
    letters = [c.lower() for c in text if c.isalnum()]
    return letters == letters[::-1]
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

<!-- challenge -->

A loop builds a 50 MB report with `report += line` and takes minutes. What do you change?

<!-- solution -->

Collect lines in a list and `"".join(lines)` once at the end (or write lines directly to a file). Each `+=` copies the whole growing string.

<!-- takeaways -->

- Strings are immutable; join instead of concatenating.
- Encode text to bytes explicitly.
- Slices: `[start:stop:step]`, stop excluded.

<!-- unit: Comprehensions and iteration helpers -->

<!-- goals -->

- Write list, dict and set comprehensions.
- Choose generator expressions and use zip and enumerate.

<!-- concept -->

Comprehensions build collections from iterables in one readable expression, with optional filtering. They come in list, dict and set forms. Swapping brackets for parentheses gives a generator expression, which produces items lazily instead of building everything in memory, ideal when you only iterate once.

Two helpers pair naturally with them: `enumerate` gives positions without manual counters, and `zip` walks several sequences together.

<!-- example -->

```python
names = ["ana", "luis", "marta"]
upper = [n.upper() for n in names if len(n) > 3]
lengths = {n: len(n) for n in names}
initials = {n[0] for n in names}
total_chars = sum(len(n) for n in names)        # generator: no list built
for i, (name, score) in enumerate(zip(names, [9, 7, 8]), start=1):
    print(i, name, score)
```

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

#### What do `zip` and `enumerate` do?

`zip(a, b)` pairs items from several iterables (stopping at the shortest, or raising with `strict=True`). `enumerate(seq, start=0)` yields `(index, item)` pairs.

#### How do you flatten a list of lists in a comprehension?

`[x for row in rows for x in row]`, with the `for` clauses in the same order as nested loops. Python 3.15 adds unpacking in comprehensions (PEP 798): `[*row for row in rows]` does the same, and `{**d for d in dicts}` merges a list of dicts, later keys winning.

<!-- challenge -->

`sum([row["amount"] for row in read_rows(path)])` runs out of memory on a 40 GB file. What is the one-character fix, and why?

<!-- solution -->

Remove the brackets: `sum(row["amount"] for row in read_rows(path))`. The generator expression yields one value at a time instead of building a full list.

<!-- takeaways -->

- Comprehensions build collections concisely.
- Generator expressions are lazy and memory-light.
- `enumerate` and `zip` replace manual indexing.

<!-- unit: Dicts and lists -->

<!-- goals -->

- Explain dict and list performance characteristics.
- Use get, merging, set operations and order-preserving deduplication.

<!-- concept -->

Choosing the right container is the biggest performance decision in everyday Python. Dicts and sets are hash tables, so membership and lookup take constant time; lists are arrays, fast at the end but slow to search or change at the front. Many slow loops become fast by replacing a list lookup with a set or dict.

Dicts also keep insertion order, which makes order-preserving deduplication and "latest per key" problems simple.

<!-- example -->

```python
seen = set(existing_ids)                       # O(1) membership
new = [r for r in rows if r["id"] not in seen]
latest = {}
for r in rows:                                 # keep the newest row per key
    if r["id"] not in latest or r["ts"] > latest[r["id"]]["ts"]:
        latest[r["id"]] = r
merged = defaults | overrides                  # overrides win
```

#### How is a Python dict implemented, and what are its complexities?

As a hash table: lookup, insertion and deletion are O(1) on average. Since Python 3.7, dicts preserve insertion order.

#### What is the time complexity of common list operations?

Indexing and `append` are O(1) (amortized for append), `insert(0, x)` and `pop(0)` are O(n), `x in list` is O(n), sorting is O(n log n). Use `collections.deque` for fast operations at both ends and sets for membership tests.

#### What does `dict.get()` do, and how is it different from `dict[key]`?

`d[key]` raises `KeyError` for a missing key. `d.get(key, default)` returns `default` (or `None`) instead.

#### How do you merge two dicts?

`merged = a | b` (Python 3.9+), or `{**a, **b}`. Values from `b` win on duplicate keys. `a |= b` updates in place.

#### What is `frozendict`?

A built-in immutable mapping added in Python 3.15 (PEP 814). It can't change after creation and is hashable when its keys and values are, so it can be a dict key, a set member or a safe default value. It isn't a subclass of `dict`. On older versions, `types.MappingProxyType` gives a read-only view of a dict.

#### How do you remove duplicates from a list while keeping order?

```python
unique = list(dict.fromkeys(items))
```

#### What are the set operations?

Union `a | b`, intersection `a & b`, difference `a - b`, symmetric difference `a ^ b`, and the subset test `a <= b`. Membership tests are O(1) on average.

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

<!-- challenge -->

A job checks `if customer_id in processed_ids` where `processed_ids` is a list of 2 million IDs, and it takes hours. What do you change?

<!-- solution -->

Make `processed_ids` a set: membership becomes O(1) instead of scanning the list, turning hours into seconds.

<!-- takeaways -->

- Dicts and sets give O(1) lookups.
- Lists are slow to search and to change at the front.
- Dicts keep insertion order.

<!-- unit: The collections module -->

<!-- goals -->

- Use defaultdict, Counter, namedtuple and deque.
- Solve counting, grouping and stack problems with them.

<!-- concept -->

The `collections` module packages patterns you'd otherwise write by hand. `defaultdict` creates missing values automatically, perfect for grouping. `Counter` counts and ranks. `namedtuple` gives tuples readable field names. `deque` adds and removes at both ends in constant time, so it serves as queue, stack or sliding window.

Many interview problems are one of these patterns in disguise.

<!-- example -->

```python
from collections import Counter, defaultdict, deque
words = "the cat and the hat".split()
print(Counter(words).most_common(2))            # [('the', 2), ('cat', 1)]
groups = defaultdict(list)
for w in ["eat", "tea", "tan", "ate"]:
    groups["".join(sorted(w))].append(w)
last_three = deque(maxlen=3)
for x in range(10):
    last_three.append(x)                        # keeps 7, 8, 9
```

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

#### Count word frequencies in a text and return the top ten.

```python
import re
from collections import Counter

def top_words(text: str, n: int = 10) -> list[tuple[str, int]]:
    return Counter(re.findall(r"\w+", text.lower())).most_common(n)
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

#### Find the first non-repeating character in a string.

```python
from collections import Counter

def first_unique(s: str) -> str | None:
    counts = Counter(s)
    return next((c for c in s if counts[c] == 1), None)
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

<!-- challenge -->

A function keeps the last 1,000 log lines with `lines.append(x)` followed by `lines.pop(0)`, and it slows down as traffic grows. What do you use?

<!-- solution -->

A `deque(maxlen=1000)`: appending automatically drops the oldest item in O(1), while `list.pop(0)` shifts every element.

<!-- takeaways -->

- `defaultdict` groups; `Counter` counts.
- `deque` is O(1) at both ends.
- Many problems are these patterns in disguise.

<!-- unit: Sorting -->

<!-- goals -->

- Sort lists and records by one or several keys.
- Choose between sort and sorted and apply sorting to interval problems.

<!-- concept -->

Python sorts with a key function: tell it what to compare, and it handles the rest, stably and efficiently. Tuples as keys sort by several fields at once; negating a number reverses one field. `sort()` changes a list in place and returns `None`, a frequent bug when assigned; `sorted()` returns a new list from any iterable.

Sorting is also a problem-solving step: once intervals are sorted by start, overlaps become neighbors.

<!-- example -->

```python
from operator import itemgetter
rows = [{"country": "CO", "revenue": 50}, {"country": "AR", "revenue": 80}, {"country": "CO", "revenue": 90}]
rows.sort(key=lambda r: (r["country"], -r["revenue"]))     # country asc, revenue desc
top = sorted(rows, key=itemgetter("revenue"), reverse=True)[:2]
```

#### How do you sort a list of dicts by a key?

```python
rows.sort(key=lambda r: (r["country"], -r["revenue"]))
top = sorted(rows, key=operator.itemgetter("revenue"), reverse=True)[:10]
```

Sorting is stable, so you can sort by several keys in successive passes.

#### What is the difference between `sort()` and `sorted()`?

`list.sort()` sorts in place and returns `None`. `sorted()` takes any iterable and returns a new list.

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

<!-- challenge -->

`result = rows.sort(key=...)` and then `result[0]` fails with `TypeError: 'NoneType' object is not subscriptable`. Why?

<!-- solution -->

`list.sort()` sorts in place and returns `None`. Either call `rows.sort(...)` and use `rows`, or `result = sorted(rows, key=...)`.

<!-- takeaways -->

- Sort with key functions; tuples for several fields.
- `sort()` returns None; `sorted()` returns a list.
- Sorting turns overlap problems into neighbor checks.

<!-- stage: Writing Python -->

### Functions, scope and closures

<!-- unit: Parameters and arguments -->

<!-- goals -->

- Use *args, **kwargs, keyword-only and positional-only parameters.
- Avoid mutable defaults and return or unpack several values.

<!-- concept -->

Function signatures are an interface, and Python gives fine control over it: collect extra arguments, force some to be named for readability, or force others to be positional so they can be renamed later. Unpacking returns several values naturally.

One trap catches everyone once: default values are created when the function is defined, not when it's called, so a mutable default is shared by every call.

<!-- example -->

```python
def load(path, /, *, batch_size=1000, tags=None):   # path positional-only, rest keyword-only
    tags = [] if tags is None else list(tags)       # never a mutable default
    ...

def bounds(values):
    return min(values), max(values)

low, high = bounds([3, 9, 4])
first, *middle, last = [1, 2, 3, 4, 5]
```

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

#### How do you return multiple values from a function?

Return a tuple and unpack it: `low, high = bounds(values)`. For more than a few values, return a dataclass or named tuple.

#### What does unpacking with `*` do in assignments?

It collects the remaining items: `first, *middle, last = [1, 2, 3, 4]` gives `middle == [2, 3]`.

<!-- challenge -->

`def add_item(item, basket=[])` returns baskets that contain items from previous calls. Fix it.

<!-- solution -->

Use `basket=None` and create the list inside: `if basket is None: basket = []`. The default list was created once and shared across calls.

<!-- takeaways -->

- `*args` and `**kwargs` collect extra arguments.
- `*` forces keywords; `/` forces positions.
- Use `None` instead of mutable defaults.

<!-- unit: Functions as values -->

<!-- goals -->

- Use lambdas, higher-order functions, map, filter, reduce and partial.
- Understand any, all and short-circuit evaluation.

<!-- concept -->

Functions are objects, so they can be passed, returned and stored like any value. That's what makes sorting by key, callbacks and decorators possible. Small throwaway functions can be lambdas; partial application fixes some arguments to build specialized versions.

Logical operators share this flexibility: `and` and `or` return one of their operands rather than a boolean, and `any`/`all` stop as soon as the answer is known.

<!-- example -->

```python
from functools import partial, reduce
parse_bin = partial(int, base=2)                           # parse_bin("1010") == 10
total = reduce(lambda acc, x: acc + x, [1, 2, 3], 0)
has_errors = any(r["status"] == "error" for r in results)  # stops at the first error
name = user_input or "anonymous"                           # returns an operand
```

#### What is a lambda?

An anonymous function limited to one expression: `lambda x: x * 2`. Mostly used as a short `key=` argument. Use `def` for anything more complex.

#### What are first-class functions?

Functions are objects: they can be assigned to variables, stored in data structures, passed as arguments and returned from other functions.

#### What is a higher-order function?

A function that takes or returns other functions, such as `sorted(key=...)`, decorators or `map`.

#### What are `map`, `filter` and `functools.reduce`?

`map(f, xs)` applies `f` to each item, `filter(pred, xs)` keeps items where `pred` is true (both lazy), and `reduce(f, xs, init)` folds a sequence into one value. Comprehensions are usually more readable than `map` and `filter`.

#### What does `functools.partial` do?

It creates a new function with some arguments fixed: `parse_fr = partial(parse_date, fmt="%d/%m/%Y")`.

#### What are `any()` and `all()`?

`any(it)` is true if at least one item is truthy, `all(it)` if every item is (and true for an empty iterable). Both short-circuit.

#### How does Python evaluate `and` and `or`?

With short-circuiting, returning one of the operands rather than a bool: `x or default` returns `x` if it's truthy, else `default`.

<!-- challenge -->

`timeout = config.get("timeout") or 30` sets 30 when the config explicitly says `0` (no timeout). How do you fix it?

<!-- solution -->

`or` treats 0 as false. Test for missing values explicitly: `timeout = config.get("timeout"); timeout = 30 if timeout is None else timeout`.

<!-- takeaways -->

- Functions are values you can pass and return.
- `partial` fixes arguments; lambdas are one-liners.
- `and`/`or` return operands and short-circuit.

<!-- unit: Closures and scope -->

<!-- goals -->

- Write closures and avoid the late-binding gotcha.
- Use recursion and memoization wisely.

<!-- concept -->

A function defined inside another remembers the variables around it, even after the outer function returns. That's a closure, the mechanism behind decorators and factory functions. It looks up those variables when called, not when defined, which surprises people in loops.

Recursion suits naturally recursive structures but has a depth limit and repeated work. Caching results by argument removes the repeats.

<!-- example -->

```python
def make_multiplier(k):
    def mul(x):
        return x * k          # remembers k
    return mul

funcs = [lambda i=i: i for i in range(3)]   # bind i now, not at call time
print([f() for f in funcs])                 # [0, 1, 2]

from functools import cache
@cache
def fib(n): return n if n < 2 else fib(n - 1) + fib(n - 2)
```

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

#### What is recursion, and what is Python's recursion limit?

A function calling itself. CPython limits depth (1000 by default, `sys.getrecursionlimit()`) and has no tail-call optimization, so deep recursion is usually rewritten as a loop.

#### What does `functools.lru_cache` (or `cache`) do?

It memoizes a function's results by its arguments (which must be hashable):

```python
from functools import cache

@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

<!-- challenge -->

A recursive function that walks a deeply nested JSON fails with `RecursionError` on one file. What do you do?

<!-- solution -->

Rewrite it iteratively with an explicit stack (a list or deque) of items to visit, which has no depth limit; raising the recursion limit only delays the crash.

<!-- takeaways -->

- Closures remember enclosing variables.
- They read variables at call time; bind with defaults.
- Recursion has limits; caching avoids repeated work.

<!-- unit: Documenting and typing functions -->

<!-- goals -->

- Write docstrings and type hints, including optional values.
- Distinguish functions from methods.

<!-- concept -->

A function's signature tells callers how to use it; docstrings and type hints tell them what it means. Hints aren't enforced at run time, but editors and type checkers use them to catch mistakes before code runs, and they document intent better than names alone.

Methods are functions attached to classes, with the instance passed automatically. Knowing that helps when passing methods around as callbacks.

<!-- example -->

```python
def parse_amount(raw: str, default: float | None = None) -> float | None:
    """Parse '1.234,56' or '1234.56' into a float.

    Returns `default` when the value is empty or invalid.
    """
    ...
```

#### What are docstrings?

String literals as the first statement of a module, class or function, available as `__doc__` and shown by `help()`.

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

#### When are annotations evaluated?

Since Python 3.14 (PEPs 649 and 749), annotations of functions, classes and modules are evaluated lazily, only when something reads them. Forward references to classes defined later no longer need quotes or `from __future__ import annotations`. The new `annotationlib` module inspects them, and `typing.get_type_hints()` still works.

<!-- challenge -->

A function is annotated `-> float` but returns `None` on bad input, and callers crash on `None + 1`. How do hints help prevent this?

<!-- solution -->

Annotate it honestly as `-> float | None` and run a type checker (mypy, pyright), which then flags callers that use the result without handling `None`.

<!-- takeaways -->

- Docstrings explain behavior; hints describe types.
- Hints aren't enforced but power type checkers.
- `X | None` marks optional values.

### Object-oriented programming

<!-- unit: Classes and instances -->

<!-- goals -->

- Define classes with __init__, instance and class attributes.
- Use staticmethod, classmethod and property.

<!-- concept -->

A class bundles data and the behavior that works on it. Instances get their own attributes in `__init__`, while class attributes are shared by every instance, which is useful for constants and dangerous for mutable data.

Decorators shape the interface: class methods build alternative constructors, static methods group helpers, and properties expose computed values or validation behind plain attribute syntax.

<!-- example -->

```python
class Order:
    vat_rate = 0.19                          # class attribute (shared)

    def __init__(self, net: float):
        self.net = net                       # instance attribute

    @property
    def gross(self) -> float:
        return round(self.net * (1 + self.vat_rate), 2)

    @classmethod
    def from_dict(cls, d: dict) -> "Order":
        return cls(net=float(d["net"]))
```

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

<!-- challenge -->

A class defines `items = []` at class level, and every instance ends up sharing the same items. Fix it.

<!-- solution -->

Create the list per instance in `__init__` (`self.items = []`). Class-level mutable attributes are shared by all instances.

<!-- takeaways -->

- Instance attributes live in `__init__`; class attributes are shared.
- Classmethods are alternative constructors.
- Properties hide computation behind attributes.

<!-- unit: Inheritance and composition -->

<!-- goals -->

- Use inheritance, super() and abstract base classes.
- Explain the MRO and when composition is better.

<!-- concept -->

Inheritance lets a class reuse and specialize another's behavior, with `super()` calling the parent's version. With multiple inheritance, the method resolution order decides which implementation wins. Abstract base classes define methods subclasses must implement.

Deep hierarchies become rigid, though. Composition, building objects from other objects, often gives the same reuse with less coupling: a pipeline that has a reader and a writer is easier to change than one that is a special kind of both.

<!-- example -->

```python
from abc import ABC, abstractmethod

class Sink(ABC):
    @abstractmethod
    def write(self, rows: list[dict]) -> None: ...

class S3Sink(Sink):
    def write(self, rows): ...

class Pipeline:                       # composition: has a sink
    def __init__(self, sink: Sink):
        self.sink = sink
```

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

#### What are abstract base classes?

Classes deriving from `abc.ABC` with methods marked `@abstractmethod`. They can't be instantiated until a subclass implements every abstract method, which enforces an interface.

#### What is composition, and why is it often preferred to inheritance?

Building objects from other objects ("has a") instead of extending classes ("is a"). It gives looser coupling and avoids deep, fragile class hierarchies.

<!-- challenge -->

A team has `CsvS3Pipeline`, `CsvLocalPipeline`, `JsonS3Pipeline`, `JsonLocalPipeline`… and every new format or target doubles the classes. How do you restructure?

<!-- solution -->

Compose: a `Pipeline` that takes a `Reader` (CSV, JSON) and a `Sink` (S3, local) as parameters. New formats or targets add one class each instead of multiplying combinations.

<!-- takeaways -->

- `super()` calls the parent implementation.
- ABCs define required methods.
- Prefer composition to deep hierarchies.

<!-- unit: The data model and dunder methods -->

<!-- goals -->

- Implement dunder methods such as __repr__, __eq__, __hash__ and __call__.
- Use dataclasses and __slots__.

<!-- concept -->

Python's syntax is powered by special methods. Defining `__repr__` gives readable debugging output; `__eq__` and `__hash__` decide equality and whether objects can be dict keys; `__call__` makes instances behave like functions. Implementing them makes your classes feel built in.

Dataclasses generate the common ones from field declarations, and `__slots__` trims memory for classes with millions of instances.

<!-- example -->

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CustomerKey:
    source: str
    customer_id: int          # frozen → hashable, usable as dict key

key = CustomerKey("crm", 552)
print(key)                    # CustomerKey(source='crm', customer_id=552)
seen = {key: True}
```

#### What are dunder (magic) methods?

Methods with double underscores that hook into language behavior: `__repr__`, `__str__`, `__len__`, `__eq__`, `__hash__`, `__lt__`, `__iter__`, `__getitem__`, `__enter__`, `__call__`, `__add__`.

#### What is the difference between `__str__` and `__repr__`?

`__repr__` is an unambiguous representation for developers (ideally valid code to recreate the object). `__str__` is a readable representation for users. `print()` uses `__str__` and falls back to `__repr__`.

#### What makes an object hashable?

A `__hash__` that doesn't change during its lifetime, and an `__eq__` consistent with it (equal objects must have equal hashes). Defining `__eq__` without `__hash__` makes a class unhashable.

#### What is `__call__`?

A method that makes instances callable like functions, which is useful for configurable function objects.

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

#### What does `copy.replace()` do?

Added in Python 3.13, it returns a copy of an object with some fields changed: `copy.replace(order, status="paid")`. It works with dataclasses (like `dataclasses.replace`), named tuples and `datetime` objects, and any class can support it by defining `__replace__`. It's the idiomatic way to "modify" frozen objects.

#### What are `__slots__`?

A class attribute listing allowed instance attributes. It removes the per-instance `__dict__`, reducing memory use and speeding up attribute access for many small objects.

<!-- challenge -->

Objects of a mutable dataclass are used as dict keys, then a field changes, and lookups stop finding them. Why, and the fix?

<!-- solution -->

The hash depends on fields; changing a field changes the hash, so the dict looks in the wrong place. Use `frozen=True` for key objects (or don't mutate them).

<!-- takeaways -->

- Dunder methods plug classes into syntax.
- Hashable objects must not change their hash.
- Dataclasses generate the boilerplate.

<!-- unit: Interfaces by behavior -->

<!-- goals -->

- Apply duck typing and Protocols.
- Understand Python's encapsulation conventions and metaclasses.

<!-- concept -->

Python cares about what an object can do, not what it is. Any object with a `read` method can be treated like a file; that's duck typing. Protocols let type checkers verify this structurally, without inheritance.

Privacy is by convention: a leading underscore means "internal", double underscores mangle names to avoid clashes. Metaclasses, which customize how classes themselves are created, exist but are rarely the right tool in application code.

<!-- example -->

```python
from typing import Protocol

class SupportsRead(Protocol):
    def read(self, n: int = -1) -> bytes: ...

def checksum(src: SupportsRead) -> str:     # works with files, BytesIO, S3 streams...
    import hashlib
    return hashlib.sha256(src.read()).hexdigest()
```

#### What is duck typing?

Using an object according to its behavior rather than its type: "if it walks like a duck…". Any object with a `read()` method can be used where a file is expected.

#### What is a Protocol?

`typing.Protocol` defines structural interfaces for static type checkers: any class with matching methods satisfies it, without inheriting from it.

#### What is encapsulation in Python?

Python has no private members. By convention, `_name` is internal, and `__name` triggers name mangling (`_Class__name`) to avoid clashes in subclasses.

#### What is a metaclass?

The class of a class (by default `type`), which controls how classes are created. Rarely needed. Class decorators and `__init_subclass__` cover most use cases.

#### What is a descriptor?

An object stored as a class attribute that defines `__get__` (and optionally `__set__` or `__delete__`), so it controls what happens when that attribute is accessed on instances. Properties, methods, `classmethod`, `staticmethod` and `__slots__` are all built on descriptors; you write your own for reusable field validation.

<!-- challenge -->

A function requires `isinstance(f, io.FileIO)` and rejects S3 streams and `BytesIO` objects that would work fine. How do you make it accept them?

<!-- solution -->

Drop the `isinstance` check and rely on behavior (call `read()`), typing the parameter as a `Protocol` with `read`, so any readable object is accepted and checkers still verify it.

<!-- takeaways -->

- Duck typing: behavior over type.
- Protocols type-check behavior structurally.
- Underscore names are internal by convention.

### Iterators, generators, decorators and context managers

<!-- unit: Iterators and generators -->

<!-- goals -->

- Distinguish iterables from iterators and write generators.
- Make classes iterable and delegate with yield from.

<!-- concept -->

Anything you can loop over is an iterable; looping asks it for an iterator, which hands out items one at a time until exhausted. Generators are the easy way to write iterators: a function with `yield` pauses after each item and resumes on the next request.

Because iterators are consumed as you go, a generator can only be looped over once. That's the price of their benefit: they can produce endless or huge sequences with almost no memory.

<!-- example -->

```python
def flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)     # delegate to the nested generator
        else:
            yield item

print(list(flatten([1, [2, [3, 4]], 5])))   # [1, 2, 3, 4, 5]
gen = flatten([1, [2]]); list(gen); print(list(gen))   # [] — exhausted
```

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

#### What is the difference between `return` and `yield` in a function?

`return` ends the function and gives back one value. `yield` turns the function into a generator that produces a series of values over time, resuming where it left off.

#### What happens if you iterate over a generator twice?

The second loop yields nothing: the generator is exhausted. Recreate it, or store the results in a list if you need them twice.

#### How do you make a class iterable?

Implement `__iter__`, typically as a generator method:

```python
class Batch:
    def __init__(self, rows):
        self.rows = rows
    def __iter__(self):
        yield from self.rows
```

#### What does `yield from` do?

It delegates to a sub-iterator, yielding all its items: `yield from read_batches(path)`.

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

<!-- challenge -->

A function passes a generator to two consumers: one validates rows, the other loads them. The loader receives nothing. Why, and what are two fixes?

<!-- solution -->

The validator exhausted the generator. Either call the generator function twice (fresh iterators), or validate and load in one pass; `itertools.tee` works but buffers data.

<!-- takeaways -->

- Iterables produce iterators; iterators are consumed.
- Generators pause at `yield` and use little memory.
- A generator can be iterated only once.

<!-- unit: Lazy pipelines with itertools -->

<!-- goals -->

- Build memory-light pipelines with generators and itertools.
- Use groupby, islice and batched correctly.

<!-- concept -->

Chaining generators creates pipelines that process data as a stream: read a line, parse it, filter it, write it, without ever holding the whole file. `itertools` supplies the fittings: concatenate, slice, group, batch and accumulate any iterator.

One fitting surprises people: `groupby` only groups consecutive items with the same key, so input must already be sorted by that key.

<!-- example -->

```python
from itertools import batched, islice, groupby, accumulate

def read_rows(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n").split(";")

for batch in batched(read_rows("big.csv"), 10_000):   # Python 3.12+
    load(batch)
print(list(accumulate([3, 5, 2])))                    # [3, 8, 10]
```

#### Why are generators useful in data engineering?

They process data as streams, with constant memory, regardless of input size: reading huge files line by line, paginating APIs, chaining transformations lazily.

#### What is lazy evaluation?

Computing values only when needed. Generators, `range`, `map`, `zip` and dictionary views are lazy, which saves memory and allows infinite sequences.

#### What is `itertools`, and name a few useful functions?

A module of fast iterator building blocks: `chain`, `islice`, `groupby`, `product`, `permutations`, `combinations`, `accumulate`, `count`, `cycle`, `tee`, `zip_longest`, `pairwise` (3.10, consecutive pairs) and `batched` (3.12; since 3.13, `strict=True` rejects a short last batch).

#### How does `itertools.groupby` work, and what's the catch?

It groups consecutive items with the same key, so the input must be sorted by that key first:

```python
from itertools import groupby
for country, rows in groupby(sorted(data, key=key), key=key):
    print(country, sum(1 for _ in rows))
```

#### How do you read only the first n items of an iterator?

`itertools.islice(it, n)`, which works on any iterator, including infinite ones.

#### How would you chunk an iterable into fixed-size batches?

`itertools.batched(iterable, n)` in Python 3.12+, or with `islice` in a loop for older versions.

#### Implement a function that splits a list into chunks of size n.

```python
def chunks(items: list, n: int) -> list[list]:
    return [items[i:i + n] for i in range(0, len(items), n)]
```

#### Compute a running (cumulative) total and a 3-item moving average.

```python
from itertools import accumulate

values = [3, 5, 2, 8, 6]
running = list(accumulate(values))                                         # [3, 8, 10, 18, 24]
moving = [sum(values[i - 2:i + 1]) / 3 for i in range(2, len(values))]     # [3.33, 5.0, 5.33]
```

<!-- challenge -->

`groupby(rows, key=lambda r: r["country"])` returns "CO" three times as separate groups. What is wrong?

<!-- solution -->

`groupby` groups only consecutive items; the rows aren't sorted by country. Sort first (`sorted(rows, key=...)`) or use a `defaultdict(list)` to group without sorting.

<!-- takeaways -->

- Generator pipelines stream data in constant memory.
- `itertools` provides slicing, batching and grouping.
- `groupby` needs input sorted by the key.

<!-- unit: Decorators -->

<!-- goals -->

- Write decorators that preserve function metadata.
- Write decorators that take arguments.

<!-- concept -->

A decorator wraps a function to add behavior around it, such as timing, retries, caching or logging, without changing its code. The `@` syntax is shorthand for replacing the function with the wrapped version.

Two details make decorators production-ready: copying the original function's name and docstring with `functools.wraps`, and an extra layer of nesting when the decorator itself needs parameters.

<!-- example -->

```python
import functools, time

def retry(times: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    if attempt == times:
                        raise
                    time.sleep(delay * attempt)
        return wrapper
    return decorator

@retry(times=5)
def fetch(url): ...
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

<!-- challenge -->

After decorating functions with a homemade `@timed`, all functions in logs and tracebacks are named "wrapper". What is missing?

<!-- solution -->

`@functools.wraps(func)` on the inner wrapper, which copies the original function's name, docstring and other metadata.

<!-- takeaways -->

- Decorators wrap functions to add behavior.
- Always use `functools.wraps`.
- Parameterized decorators add one nesting level.

<!-- unit: Context managers -->

<!-- goals -->

- Use and write context managers, including with contextlib.
- Control exception handling in __exit__ and manage many resources with ExitStack.

<!-- concept -->

Resources such as files, connections, locks and transactions need cleanup even when errors happen. Context managers guarantee it: setup runs on entering the `with` block, teardown on leaving it, however it's left.

`contextlib` turns a generator into a context manager in a few lines. `__exit__` decides whether an exception propagates, and `ExitStack` manages a variable number of resources at once.

<!-- example -->

```python
from contextlib import contextmanager, ExitStack

@contextmanager
def transaction(conn):
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise

with ExitStack() as stack:
    files = [stack.enter_context(open(p, encoding="utf-8")) for p in paths]   # all closed at the end
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

<!-- challenge -->

A homemade context manager's `__exit__` returns `True` "to be safe", and errors inside `with` blocks disappear. What is happening?

<!-- solution -->

Returning a truthy value from `__exit__` suppresses the exception. Return `None`/`False` (or re-raise) so errors propagate after cleanup.

<!-- takeaways -->

- Context managers guarantee cleanup.
- `@contextmanager` builds them from generators.
- Truthy `__exit__` results swallow exceptions.

<!-- stage: Working with the outside world -->

### Errors, files and the standard library

<!-- unit: Exceptions -->

<!-- goals -->

- Handle, raise and chain exceptions correctly.
- Define custom exceptions and choose between EAFP and LBYL.

<!-- concept -->

Good error handling catches only what you can handle and lets everything else surface. Specific `except` clauses, cleanup in `finally`, and an `else` for code that should run only on success keep intent clear. A bare `except` hides bugs and even blocks Ctrl+C.

Custom exceptions give callers meaningful types to catch, chaining keeps the original cause in tracebacks, and exception groups report several failures at once.

<!-- example -->

```python
class PipelineError(Exception): ...
class BadRecordError(PipelineError): ...

def parse(raw: str) -> int:
    try:
        return int(raw)
    except ValueError as exc:
        raise BadRecordError(f"not a number: {raw!r}") from exc
```

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

#### How do you catch several exception types in one clause?

List them in a tuple: `except (ConnectionError, TimeoutError) as exc:`. Since Python 3.14 (PEP 758), the parentheses can be dropped when there is no `as` clause: `except ConnectionError, TimeoutError:`. Across clauses, the first matching `except` wins, so put specific exceptions before general ones.

#### What is EAFP versus LBYL?

"Easier to ask forgiveness than permission" (try the operation and catch the error) versus "Look before you leap" (check first). EAFP is idiomatic in Python and avoids race conditions between the check and the action.

<!-- challenge -->

A loader wraps everything in `try: ... except: pass`, and missing data goes unnoticed for weeks. How do you rewrite it?

<!-- solution -->

Catch only expected errors (for example `ValueError` for bad records), log them with context and count them, and let unexpected exceptions propagate so the job fails visibly.

<!-- takeaways -->

- Catch specific exceptions only.
- Chain with `raise ... from exc`.
- Custom exception types help callers.

<!-- unit: Files and paths -->

<!-- goals -->

- Read large files safely with `with` and line iteration.
- Use pathlib, compression and temporary files.

<!-- concept -->

Files are the most common input in data work, and two habits prevent most problems. Open them with `with`, so they're closed even on errors. Iterate line by line, so memory stays constant regardless of size.

`pathlib` makes paths objects you can join, inspect and glob; compression modules read and write compressed files as if they were plain; and temporary files clean themselves up.

<!-- example -->

```python
from pathlib import Path
import gzip

raw = Path("data") / "raw"
for path in sorted(raw.glob("*.log.gz")):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        errors = sum(1 for line in f if " ERROR " in line)
    print(path.name, errors)
```

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

#### How do you compress or decompress files in Python?

The `gzip`, `bz2`, `lzma` and `zipfile` modules. `gzip.open(path, "rt", encoding="utf-8")` reads a gzipped text file line by line.

#### What is `tempfile` used for?

Creating temporary files and directories that are cleaned up automatically: `with tempfile.TemporaryDirectory() as tmp: ...`.

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

<!-- challenge -->

A script calls `open(path).read().splitlines()` on 30 GB log files and crashes. Rewrite the reading part.

<!-- solution -->

`with open(path, encoding="utf-8") as f: for line in f: process(line)`, which streams one line at a time and closes the file reliably.

<!-- takeaways -->

- Open files with `with`.
- Iterate lines to keep memory constant.
- `pathlib` for paths; `gzip` for compressed files.

<!-- unit: Data formats and dates -->

<!-- goals -->

- Read and write CSV and JSON with the standard library.
- Parse dates and use time-zone-aware datetimes.

<!-- concept -->

The standard library handles the everyday formats. The `csv` module deals with quoting and delimiters that naive splitting gets wrong; `json` converts between text and dicts, with hooks for types it doesn't know.

Dates need care: parse with explicit formats, and keep times aware of their time zone, preferably in UTC, since mixing naive and aware datetimes causes errors and silent shifts.

<!-- example -->

```python
import csv, json
from datetime import datetime, timezone

with open("in.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))
ts = datetime.strptime("17/10/2026 09:41", "%d/%m/%Y %H:%M").replace(tzinfo=timezone.utc)
print(json.dumps({"rows": len(rows), "loaded_at": ts}, default=str))
```

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

#### Why is `datetime.utcnow()` deprecated?

It returns a naive datetime that only looks like UTC, so code that later treats it as local time shifts values silently. It's deprecated since Python 3.12 (with `utcfromtimestamp()`): use `datetime.now(timezone.utc)` or `datetime.fromtimestamp(ts, tz=timezone.utc)`, which return aware datetimes. `datetime.UTC` (3.11) is a shorter alias for `timezone.utc`.

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

<!-- challenge -->

A script splits CSV lines with `line.split(",")`, and some rows have too many fields. Why, and the fix?

<!-- solution -->

Fields like `"Pérez, Ana"` contain commas inside quotes. Use `csv.reader`/`DictReader`, which handles quoting and escaping correctly.

<!-- takeaways -->

- Use `csv` instead of splitting lines.
- `json` handles text ↔ dicts; `default=` for custom types.
- Keep datetimes aware, ideally in UTC.

<!-- unit: Useful standard modules -->

<!-- goals -->

- Log properly and build command-line interfaces.
- Use regular expressions, subprocesses and hashing.

<!-- concept -->

Batteries included means most utilities are already there. `logging` gives levels, formatting and handlers, so messages can go to the console in development and to files or collectors in production. `argparse` turns scripts into proper command-line tools.

Regular expressions extract structure from text; `subprocess` runs external commands safely without a shell; `hashlib` computes checksums for files and pseudonymized keys.

<!-- example -->

```python
import argparse, logging, re, subprocess, hashlib

log = logging.getLogger(__name__)
parser = argparse.ArgumentParser(description="Load a day of orders")
parser.add_argument("--date", required=True)
args = parser.parse_args()
log.info("loading %s", args.date)                         # lazy formatting
m = re.search(r"order=(\d+)", "ts=... order=98123 status=ok")
subprocess.run(["aws", "s3", "cp", "out.csv", "s3://bucket/"], check=True)
digest = hashlib.sha256(b"ana@example.com").hexdigest()
```

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

#### What is the `enum` module used for?

Defining a fixed set of named constants, which beats string literals scattered through the code: members are typed, iterable and compared by identity. `StrEnum` (3.11) members are also strings, convenient for JSON and databases; `IntEnum` and `Flag` cover integers and bit flags.

```python
from enum import StrEnum

class Status(StrEnum):
    PENDING = "pending"
    DONE = "done"

Status("done") is Status.DONE   # True
```

<!-- challenge -->

A script runs `subprocess.run(f"rm -rf {folder}", shell=True)` with a folder name from user input. What is the risk, and the fix?

<!-- solution -->

Shell injection: a crafted name could run arbitrary commands. Pass a list of arguments without `shell=True`, validate the path, and prefer `shutil.rmtree` over shelling out.

<!-- takeaways -->

- Use `logging` with module loggers and lazy formatting.
- `argparse` builds command-line interfaces.
- Run subprocesses with argument lists, no shell.

### Concurrency and performance

<!-- unit: The GIL and concurrency models -->

<!-- goals -->

- Explain the GIL and compare threading, multiprocessing and asyncio.
- Use concurrent.futures, avoid race conditions and pickling pitfalls, and know the free-threaded build and subinterpreters.

<!-- concept -->

In the default CPython build, only one thread runs Python bytecode at a time. Threads still help when work waits on networks or disks, because waiting releases the lock; CPU-heavy work needs processes, each with its own interpreter. Asyncio handles many waits in a single thread.

Each model has its traps: threads sharing data need locks to avoid race conditions; processes need picklable functions and data; daemon threads die abruptly at exit.

<!-- example -->

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=16) as pool:          # I/O-bound: downloads
    pages = list(pool.map(fetch, urls))

def heavy(chunk): ...                                     # module-level: picklable
with ProcessPoolExecutor() as pool:                       # CPU-bound: parsing
    results = list(pool.map(heavy, chunks))
```

#### What is the GIL?

The Global Interpreter Lock in CPython lets only one thread execute Python bytecode at a time. Threads still help for I/O-bound work, because the GIL is released while waiting, but not for CPU-bound pure-Python code. A free-threaded build without the GIL exists since 3.13 and is officially supported since 3.14, but the default build still has the GIL.

#### What is free-threaded Python?

A CPython build without the GIL (PEP 703), where threads run Python code in parallel on several cores. It was experimental in 3.13 and is officially supported since 3.14 (PEP 779), installed as a separate interpreter such as `python3.14t`. Single-threaded code runs somewhat slower, and C extensions must be built for it, otherwise importing them re-enables the GIL.

#### What are subinterpreters?

Several isolated interpreters in one process, each with its own GIL, exposed by the `concurrent.interpreters` module in Python 3.14 (PEP 734) and by `InterpreterPoolExecutor` in `concurrent.futures`. They give CPU parallelism with less overhead than processes, but objects aren't shared: data passes through queues or is copied.

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

#### What is a race condition, and how do you prevent one in threads?

Two threads accessing shared data and producing a result that depends on timing. Prevent it with locks (`threading.Lock`), thread-safe queues (`queue.Queue`), or by avoiding shared mutable state.

#### What is a daemon thread?

A background thread that doesn't prevent the program from exiting. It is killed abruptly at exit, so it shouldn't hold resources that need cleaning up.

#### Why can't a lambda be sent to a process pool?

`ProcessPoolExecutor` pickles the function to send it to workers, and lambdas and nested functions can't be pickled by reference. Use module-level functions.

#### Which start method does multiprocessing use?

`spawn` on Windows and macOS, and since Python 3.14 `forkserver` on Linux and other Unix systems (it used to be `fork`). With both, workers start from a fresh interpreter, so functions and arguments must be picklable and the script needs the `if __name__ == "__main__":` guard. Code that relied on inherited globals can request `multiprocessing.get_context("fork")` explicitly.

#### What is pickling, and what are its risks?

Serializing Python objects to bytes with `pickle`. Never unpickle untrusted data: it can execute arbitrary code. Use JSON or Parquet for data exchange.

<!-- challenge -->

A team speeds up a CPU-heavy parsing job with 16 threads and sees no gain. Why, and what do you suggest?

<!-- solution -->

The GIL lets only one thread run Python code at a time, so CPU-bound threads don't run in parallel. Use a `ProcessPoolExecutor` (or a vectorized library) to use several cores.

<!-- takeaways -->

- Threads for I/O; processes for CPU.
- Shared data in threads needs locks.
- Process pools need picklable, module-level functions.

<!-- unit: asyncio -->

<!-- goals -->

- Explain coroutines, the event loop and asyncio.run.
- Limit concurrency, set timeouts and handle backpressure.

<!-- concept -->

Async code runs many I/O tasks in one thread. Coroutines pause at each `await`, letting the event loop run others while they wait. Calling an async function only creates a coroutine; the loop must run it, which `asyncio.run` does at the top level.

Concurrency needs limits. Rate-limited APIs need semaphores and backoff, every network call needs a timeout, and fast producers need bounded queues so memory doesn't grow without end.

<!-- example -->

```python
import asyncio, httpx

async def fetch_all(urls, limit=10):
    sem = asyncio.Semaphore(limit)
    async with httpx.AsyncClient(timeout=30) as client:
        async def one(url):
            async with sem:                      # at most 10 in flight
                r = await client.get(url)
                r.raise_for_status()
                return r.json()
        return await asyncio.gather(*(one(u) for u in urls))

results = asyncio.run(fetch_all(urls))
```

#### What is a coroutine in Python?

A function defined with `async def`, which can pause at `await` points. It runs in an event loop (asyncio) and enables concurrency for I/O-bound tasks.

#### How does asyncio work?

An event loop runs coroutines. At each `await` on an I/O operation, the coroutine yields control so others can run. `asyncio.gather` runs several at once:

```python
import asyncio, httpx

async def main(urls):
    async with httpx.AsyncClient(timeout=30) as client:
        return await asyncio.gather(*(client.get(u) for u in urls))

asyncio.run(main(urls))
```

#### What is `asyncio.TaskGroup`?

A context manager (3.11+) for structured concurrency: the block waits for every task created in the group, and if one fails, the others are cancelled and the errors are raised together as an `ExceptionGroup`. It's safer than `gather`, which by default lets the other tasks keep running after a failure.

```python
async with asyncio.TaskGroup() as tg:
    orders = tg.create_task(fetch_orders())
    users = tg.create_task(fetch_users())
print(orders.result(), users.result())
```

#### How does `asyncio.run` differ from calling a coroutine directly?

Calling an `async def` function only creates a coroutine object. `asyncio.run(coro)` creates an event loop, runs the coroutine to completion and closes the loop.

#### How do you limit concurrency when calling a rate-limited API?

Bound the worker pool size, or use `asyncio.Semaphore`, and add backoff with retries on 429 responses.

#### How do you set a timeout on a network call?

Pass a timeout to the library (`requests.get(url, timeout=30)`, `httpx.AsyncClient(timeout=30)`), and in async code bound a block of awaits with `async with asyncio.timeout(10):` (3.11+) or a single one with `asyncio.wait_for`. Never call external services without one: a hung connection otherwise blocks forever.

#### What is backpressure, and how do you handle it in Python pipelines?

When producers are faster than consumers, memory grows until something breaks. Use bounded queues (`queue.Queue(maxsize=...)`, `asyncio.Queue(maxsize=...)`) so producers wait.

<!-- challenge -->

An async scraper fires 50,000 requests with `gather` at once and the API bans the client. How do you fix it?

<!-- solution -->

Limit concurrency with an `asyncio.Semaphore` (or a bounded worker pool), respect `Retry-After`, retry 429s with exponential backoff, and set timeouts on every request.

<!-- takeaways -->

- Coroutines pause at `await`; the loop runs others.
- `asyncio.run` starts the event loop.
- Bound concurrency; always set timeouts.

<!-- unit: Making code faster -->

<!-- goals -->

- Profile before optimizing and know what makes Python fast.
- Avoid row-by-row pandas, and choose between PyPy, multiprocessing and Spark.

<!-- concept -->

Speed comes from measuring, then changing the slowest part. Profilers show where time goes, often somewhere unexpected. Most wins come from better algorithms and data structures, and from pushing loops into C: built-ins, NumPy, pandas or Polars vectorized operations.

Other interpreters and parallelism help in specific cases. Spark is for data that outgrows one machine, not for making small jobs faster.

<!-- example -->

```bash
python -m cProfile -s cumtime pipeline.py | head -20
```
```python
# slow: Python loop over rows
df["total"] = [r.price * r.qty for r in df.itertuples()]
# fast: vectorized
df["total"] = df["price"] * df["qty"]
```

#### How do you profile Python code?

`cProfile` (`python -m cProfile -s cumtime script.py`) for function-level time, `timeit` for small snippets, `tracemalloc` for memory, and sampling profilers for running processes. Python 3.15 adds a `profiling` package: `profiling.sampling` attaches to a running process with very low overhead and produces flame graphs, and `profiling.tracing` is the new home of `cProfile`. On older versions, py-spy fills that role.

#### What makes Python code faster in practice?

Better algorithms and data structures (sets and dicts for lookups), built-in functions and comprehensions instead of manual loops, vectorized libraries (NumPy, pandas, Polars) for bulk numeric work, avoiding repeated work (caching), and moving heavy work to compiled code or a distributed engine.

#### Why is iterating over a pandas DataFrame row by row slow?

Each row becomes a Python object and the work happens in the interpreter. Vectorized operations run in optimized C code over whole columns at once.

#### What is the difference between CPython and PyPy?

CPython is the reference interpreter, written in C. PyPy is an alternative implementation with a JIT compiler that speeds up long-running pure-Python code but is less compatible with C extensions.

#### Does CPython have a JIT compiler?

An experimental one, added in 3.13 (PEP 744) and shipped in the Windows and macOS installers since 3.14, but off by default (`PYTHON_JIT=1` turns it on). Its gains are still modest; most of CPython's speedups since 3.11 come from the specializing adaptive interpreter. For large wins on numeric code, vectorized libraries or PyPy remain the options.

#### When would you use multiprocessing over Spark?

For CPU-bound work that fits on one machine and in memory. Use Spark when data or computation exceeds one machine, or when the platform already runs on Spark.

<!-- challenge -->

A pandas transformation uses `df.apply(func, axis=1)` on 20 million rows and takes 40 minutes. What do you try first?

<!-- solution -->

Rewrite `func` with vectorized column operations (arithmetic, `np.where`, `str` and `dt` accessors) so the work runs in C; profile to confirm, and consider Polars if it's still slow.

<!-- takeaways -->

- Profile first.
- Better data structures and vectorization win most.
- Spark is for scale, not small-job speed.

<!-- unit: Memory -->

<!-- goals -->

- Explain how Python manages memory.
- Find leak-like memory growth and understand bytecode caches.

<!-- concept -->

CPython frees most objects the moment nothing refers to them, through reference counting, and a cycle collector cleans up groups of objects that refer only to each other. Memory problems in long-running programs are therefore usually references kept alive: global caches, growing lists, closures holding large objects.

Finding them means measuring allocations over time. Bytecode caches are unrelated but often confused with memory: they only speed up imports.

<!-- example -->

```python
import tracemalloc
tracemalloc.start()
run_batch()
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("lineno")[:5]:
    print(stat)          # top allocation sites
```

#### What is memory leak-like behavior in Python, and how do you find it?

Memory that keeps growing because references are kept (global caches, lists that grow, reference cycles with `__del__`). Investigate with `tracemalloc`, `gc` and `objgraph`.

#### How does Python manage memory?

Reference counting frees most objects immediately when their count drops to zero, and a cyclic garbage collector (`gc`) cleans up reference cycles.

#### What is `__pycache__`?

The folder where Python caches compiled bytecode (`.pyc` files) of imported modules, to speed up later imports.

#### What are weak references?

References that don't keep an object alive (`weakref.ref`, `WeakValueDictionary`, `WeakKeyDictionary`): once no strong reference remains, the object is freed and the weak reference returns `None`. They suit caches and registries that shouldn't keep objects in memory on their own.

<!-- challenge -->

A long-running worker's memory grows by 100 MB an hour until it's killed. The code has a module-level `CACHE = {}` filled per request. What do you change?

<!-- solution -->

Bound the cache: use `functools.lru_cache(maxsize=...)` or a size- or time-limited cache, or clear it periodically; confirm with `tracemalloc` that it was the source.

<!-- takeaways -->

- Reference counting frees objects immediately.
- Leaks are usually references kept alive.
- Measure allocations with `tracemalloc`.

<!-- stage: Engineering practice -->

### Typing, packaging, environments and testing

<!-- unit: Environments and packaging -->

<!-- goals -->

- Isolate projects with virtual environments and pyproject.toml.
- Make installs reproducible and build wheels with entry points.

<!-- concept -->

Every project needs its own set of packages, or upgrades for one break another. Virtual environments isolate them; `pyproject.toml` declares the project, its dependencies and its tools in one place.

Reproducibility comes from lock files that pin every package version, installed the same way in development, CI and production. Wheels package your code for deployment, and entry points turn functions into commands.

<!-- example -->

```toml
[project]
name = "orders-etl"
version = "1.4.0"
requires-python = ">=3.11"
dependencies = ["pyarrow>=17", "httpx>=0.27"]

[project.scripts]
orders-etl = "orders_etl.cli:main"
```
```bash
uv sync --frozen && uv build    # install exactly from uv.lock, then build the wheel
```

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

#### Which Python version should a new project target?

A recent one with years of support left. A new version ships every October, gets about two years of bug fixes, then security fixes until five years after release (PEP 602). In late 2026 that means 3.13 to 3.15, limited by what your platform supports (Databricks runtimes, Lambda, Airflow images). Declare it in `requires-python` and test it in CI.

<!-- challenge -->

A job works on a developer's laptop but fails in production after a library released a new major version. What do you put in place?

<!-- solution -->

A lock file (uv, pip-tools or Poetry) pinning all versions, installed with `--frozen` in CI and production, with dependency upgrades done deliberately through pull requests.

<!-- takeaways -->

- One virtual environment per project.
- `pyproject.toml` declares the project.
- Lock files make installs reproducible.

<!-- unit: Testing with pytest -->

<!-- goals -->

- Write pytest tests with fixtures, parametrization and mocks.
- Choose test levels and use coverage and property-based testing wisely.

<!-- concept -->

pytest keeps tests simple: plain functions with plain `assert`, and helpful failure messages. Fixtures provide what tests need, from sample data to temporary directories; parametrization runs one test over many inputs; mocks replace slow or external dependencies.

A balanced suite has many fast unit tests, some integration tests and a few end-to-end ones. Coverage shows untested areas; property-based tests find edge cases you didn't think of.

<!-- example -->

```python
import pytest
from orders_etl.parse import parse_amount

@pytest.mark.parametrize("raw, expected", [
    ("1234.56", 1234.56), ("1.234,56", 1234.56), ("", None), ("abc", None),
])
def test_parse_amount(raw, expected):
    assert parse_amount(raw) == expected

def test_fetch_uses_timeout(mocker):
    get = mocker.patch("orders_etl.api.httpx.get")
    fetch_orders("2026-10-17")
    assert get.call_args.kwargs["timeout"] == 30
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

<!-- challenge -->

Tests for an API client call the real API, so they're slow and fail when it's down. How do you fix them?

<!-- solution -->

Mock the HTTP layer in unit tests (pytest-mock, respx or responses) with recorded responses, and keep one or two integration tests against a sandbox, run separately.

<!-- takeaways -->

- pytest: plain asserts, fixtures, parametrization.
- Mock external dependencies in unit tests.
- Coverage is a signal, not a goal.

<!-- unit: Static checks and types -->

<!-- goals -->

- Keep code quality high with formatters, linters and type checkers.
- Use mypy, TypedDict and generics.

<!-- concept -->

Automated checks catch mistakes before tests run. A formatter ends style debates, a linter flags bugs and bad patterns, and a type checker finds wrong arguments and unhandled `None`s using your hints. Running them in pre-commit and CI makes them routine.

Type hints become more useful with richer types: `TypedDict` describes dict-shaped records, and generics describe containers and functions that work with any type consistently.

<!-- example -->

```python
from typing import TypedDict

class OrderRow(TypedDict):
    order_id: int
    amount: float
    country: str

def first_or_none[T](items: list[T]) -> T | None:     # Python 3.12 generics syntax
    return items[0] if items else None
```
```bash
ruff check . && ruff format --check . && mypy src/
```

#### What tools keep Python code quality high?

A formatter and linter (ruff, or black and flake8), a type checker (mypy, pyright), pre-commit hooks, tests in CI, and code review.

#### How do you check types with mypy?

Add type hints and run `mypy src/`. It reports type inconsistencies statically, before run time. Adopt it gradually with per-module settings.

#### What is `TypedDict`?

A typing construct that describes dictionaries with a fixed set of keys and value types, useful for JSON-like records.

#### What are generics in type hints?

Parameterized types such as `list[int]` or `dict[str, float]`, and your own generic classes and functions. Python 3.12 has a compact syntax: `def first[T](xs: list[T]) -> T: ...`.

#### What does the `type` statement do?

It declares a type alias (Python 3.12, PEP 695): `type Row = dict[str, str | int]`. Aliases are evaluated lazily and can be generic: `type Pair[T] = tuple[T, T]`. The same PEP lets classes and functions declare type parameters in brackets (`class Box[T]: ...`), which replaces most uses of `TypeVar`.

<!-- challenge -->

A function receives rows as dicts, and typos like `row["ammount"]` reach production. How can typing catch them?

<!-- solution -->

Describe rows with a `TypedDict` (or a dataclass/pydantic model) and annotate the function; mypy then flags unknown keys like `"ammount"` before the code runs.

<!-- takeaways -->

- Format, lint and type-check automatically.
- `TypedDict` types dict records.
- Generics keep container types consistent.

<!-- unit: Configuration and project structure -->

<!-- goals -->

- Manage configuration and secrets safely.
- Validate settings with pydantic and structure a pipeline project.

<!-- concept -->

The same code must run in development, CI and production with different settings, so configuration comes from the environment, never from hard-coded values, and secrets from a secrets manager. Validating it at start-up, with clear errors, beats discovering a missing variable halfway through a job.

Project structure follows responsibilities: a `src` package split into ingestion, transformations and outputs, thin entry points, and tests next to the code they cover.

<!-- example -->

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str
    batch_size: int = 1000
    s3_bucket: str

settings = Settings()          # reads env vars, fails fast if db_url or s3_bucket is missing
```
```text
src/orders_etl/{ingest.py, transform.py, load.py, cli.py}
tests/{test_transform.py, conftest.py}
pyproject.toml  uv.lock
```

#### How do you manage configuration and secrets in a Python application?

Read them from environment variables or a secrets manager at start-up, validate them (for example with pydantic-settings), keep `.env` files out of version control, and never hard-code credentials.

#### What is pydantic?

A data validation library that parses data into typed models and raises clear errors for invalid input. It is used for API payloads, configuration and contracts.

#### How do you read TOML configuration?

With `tomllib`, in the standard library since 3.11. It only reads, and the file must be opened in binary mode; writing needs a package such as `tomli-w`. Python 3.15 updates it to TOML 1.1.

```python
import tomllib
with open("settings.toml", "rb") as f:
    config = tomllib.load(f)
```

#### How do you structure a Python project for a data pipeline?

A `src/` layout with a package split by responsibility (ingestion, transformations, quality, io), a thin CLI entry point, configuration separate from code, tests mirroring the package, and `pyproject.toml` for dependencies and tooling.

<!-- challenge -->

A job reads `os.environ["BATCH_SIZE"]` deep inside a loop and crashes after two hours when it's missing in production. How do you prevent it?

<!-- solution -->

Load and validate all configuration once at start-up (pydantic settings or a validation function), with types and defaults, so missing or invalid values fail immediately.

<!-- takeaways -->

- Configuration from the environment; secrets from a manager.
- Validate settings at start-up.
- Structure projects by responsibility.

### Python for data engineering

<!-- unit: pandas essentials -->

<!-- goals -->

- Read large files with pandas and select data with loc and iloc.
- Group, merge and handle missing values without warnings.

<!-- concept -->

pandas is the everyday tool for data that fits in memory. Its core moves are selecting (by label or position), grouping with named aggregations, merging like SQL joins and dealing with missing values deliberately.

Memory is the usual limit: reading only needed columns with compact types, or in chunks, stretches it far. Chained indexing triggers the famous warning because pandas can't tell whether you're changing a copy or the original.

<!-- example -->

```python
import pandas as pd
df = pd.read_csv("companies.csv", usecols=["country", "industry", "revenue"],
                 dtype={"country": "category", "industry": "category"})
summary = (df.groupby(["country", "industry"], as_index=False, observed=True)
             .agg(companies=("revenue", "size"), revenue=("revenue", "sum")))
df.loc[df["revenue"] < 0, "revenue"] = pd.NA       # assign on the original, no warning
```

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

<!-- challenge -->

`pd.merge(orders, customers, on="customer_id")` returns more rows than `orders`. What happened, and how do you catch it?

<!-- solution -->

`customers` has duplicate `customer_id`s, so orders fan out. Deduplicate customers first and use `validate="many_to_one"` in `merge`, which raises if the right side isn't unique.

<!-- takeaways -->

- Read only needed columns with compact dtypes.
- Use `.loc` for assignments.
- `merge(validate=...)` catches fan-out.

<!-- unit: Columnar formats and fast engines -->

<!-- goals -->

- Explain Parquet and Arrow and write partitioned Parquet.
- Know when Polars or DuckDB beat pandas.

<!-- concept -->

CSV is a poor format for analytics: untyped, uncompressed, read in full. Parquet stores data by column with types and statistics, so tools read only what they need. Arrow is the matching in-memory format that lets pandas, Polars, DuckDB and Spark exchange data without copying.

On top of them, newer engines change what one machine can do: Polars runs multi-threaded with a query optimizer, and DuckDB runs SQL directly over Parquet files and DataFrames.

<!-- example -->

```python
import duckdb, polars as pl
top = duckdb.sql("""
    SELECT country, sum(revenue) AS revenue
    FROM 'lake/companies/*.parquet'
    GROUP BY country ORDER BY revenue DESC LIMIT 5
""").pl()
lazy = pl.scan_parquet("lake/orders/*.parquet").filter(pl.col("amount") > 0).group_by("day").agg(pl.sum("amount"))
print(lazy.collect())
```

#### What is Apache Parquet, and why is it preferred to CSV?

A columnar, compressed, typed file format. Queries read only the columns they need, files are much smaller, types are preserved and statistics allow skipping data. CSV is row-based text with no types.

#### What is Apache Arrow?

A standard in-memory columnar format. It lets pandas, Polars, DuckDB, Spark and others exchange data without copying or converting it. PyArrow is its Python library.

#### What is Polars, and when would you use it instead of pandas?

A DataFrame library written in Rust, multi-threaded, with a lazy query optimizer. It's often much faster and more memory-efficient than pandas for large single-machine workloads.

#### What is DuckDB?

An embedded analytical SQL database. It queries Parquet, CSV and DataFrames directly and very fast, without a server: `duckdb.sql("select country, count(*) from 'data/*.parquet' group by 1")`.

#### How do you write a Parquet file partitioned by a column?

```python
import pyarrow as pa, pyarrow.parquet as pq
pq.write_to_dataset(pa.Table.from_pandas(df), root_path="out/", partition_cols=["country"])
```

This creates folders such as `out/country=FR/`, which query engines can prune.

<!-- challenge -->

An analyst loads 8 GB of CSVs into pandas to compute one aggregate and runs out of memory. What would you suggest?

<!-- solution -->

Convert the files to Parquet once, then query them with DuckDB (or Polars lazy scans), which read only the needed columns, stream through the data and use all cores.

<!-- takeaways -->

- Parquet is typed, columnar and compressed.
- Arrow lets tools share data without copies.
- Polars and DuckDB stretch single-machine limits.

<!-- unit: APIs, files and databases -->

<!-- goals -->

- Call REST APIs robustly and stream large downloads.
- Connect to databases safely, bulk load rows and read from S3.

<!-- concept -->

Pipelines spend much of their time talking to other systems, and each conversation can fail. API calls need sessions, timeouts, retries with backoff and pagination. Large downloads should stream to disk instead of filling memory.

Databases need parameterized queries for safety and bulk paths like `COPY` for speed; SQLAlchemy adds pooling and portability. Object storage has its own clients, or file-like access through fsspec.

<!-- example -->

```python
import requests
from requests.adapters import HTTPAdapter, Retry

session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=Retry(total=5, backoff_factor=1,
                                                        status_forcelist=[429, 500, 502, 503])))
with session.get(URL, stream=True, timeout=60) as r:
    r.raise_for_status()
    with open("export.csv.gz", "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 20):
            f.write(chunk)
```

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

<!-- challenge -->

A job builds SQL with `f"SELECT * FROM users WHERE email = '{email}'"`. What are the two problems, and the fix?

<!-- solution -->

SQL injection (a crafted value can change the query) and quoting bugs (emails with apostrophes break it). Use parameterized queries: `cur.execute("... WHERE email = %s", (email,))`.

<!-- takeaways -->

- Sessions, timeouts, retries and pagination for APIs.
- Stream large downloads.
- Parameterize SQL; bulk load with `COPY`.

<!-- unit: Reliable pipeline steps -->

<!-- goals -->

- Make pipeline steps idempotent and validate data before loading.
- Handle encodings and large JSON, and orchestrate Python pipelines.

<!-- concept -->

A pipeline step will be retried, rerun and fed surprising data. Idempotent steps, which give the same result when run twice, make retries safe; validation before loading stops bad data at the door. Encoding and file-size issues are among the most common surprises.

Scheduling, dependencies and alerts belong to an orchestrator rather than cron and hope. Whether Python transforms the data itself (ETL) or mostly moves it for a warehouse to transform (ELT) shapes how much of it you write.

<!-- example -->

```python
def load_day(conn, day: str, rows: list[dict]) -> None:
    validate(rows)                                   # schema, nulls, ranges, duplicates
    with conn.transaction():
        conn.execute("DELETE FROM sales WHERE sale_date = %s", (day,))
        copy_rows(conn, "sales", rows)               # rerun-safe: replaces the day
```

#### How do you make a data pipeline step idempotent?

Running it twice with the same input must give the same result: write to a deterministic location and overwrite it (or merge on keys) instead of appending, use run IDs, and check whether the work was already done.

#### How would you validate a dataset in Python before loading it?

Check the schema (columns and types), nulls in required fields, value ranges, uniqueness of keys and row counts against expectations, with code, pydantic or a library like pandera or Great Expectations. Fail loudly or quarantine bad rows.

#### How do you handle encoding problems when reading files?

Pass the right `encoding` explicitly, use `errors="replace"` only knowingly, detect a BOM with `encoding="utf-8-sig"`, and repair mojibake (`'TravesÃ­a'.encode('latin-1').decode('utf-8')`) with a guard for strings where the round trip fails. Since Python 3.15, `open()` defaults to UTF-8 instead of the locale encoding (PEP 686), which removes many Windows surprises, but naming the encoding stays the portable choice.

#### How do you process a JSON file that is too large to load at once?

Prefer newline-delimited JSON and read it line by line. For one huge JSON array, use a streaming parser such as ijson to iterate over elements without loading everything.

#### How do you schedule and orchestrate Python pipelines?

With an orchestrator such as Airflow, Dagster or Prefect (dependencies, retries, alerts, backfills), or a cloud scheduler triggering serverless functions or containers for simple cases.

#### What is the difference between ETL and ELT from a Python developer's point of view?

In ETL, Python code transforms data before loading it. In ELT, Python mainly extracts and loads raw data, and transformations run as SQL in the warehouse (often with dbt). Python remains for what SQL handles poorly: APIs, files, complex parsing.

<!-- challenge -->

A daily step appends rows to a table, and a retry after a timeout doubled the day's data. Rewrite its write strategy.

<!-- solution -->

Replace the day's slice in one transaction (delete the date then insert, or upsert on the business key), so running it twice leaves the same data.

<!-- takeaways -->

- Idempotent steps make retries safe.
- Validate before loading.
- Orchestrators handle schedules, retries and alerts.

<!-- unit: Python and Spark -->

<!-- goals -->

- Explain how PySpark relates to Python.
- Avoid slow Python UDFs in PySpark.

<!-- concept -->

PySpark lets Python describe distributed computations, but the work runs in Spark's JVM engine. Python code builds the plan; rows rarely touch the Python interpreter, which is why PySpark scales.

The exception is Python UDFs: each row is shipped to a Python process and back, losing speed and optimization. Built-in functions, or vectorized pandas UDFs when Python is unavoidable, keep the work where Spark is fast.

<!-- example -->

```python
from pyspark.sql import functions as F
# slow: Python UDF per row
# clean = F.udf(lambda s: s.strip().lower())
# fast: built-in functions
df = df.withColumn("email", F.lower(F.trim("email")))
```

#### What is PySpark, and how does it relate to Python?

The Python API for Apache Spark. Python code builds a query plan that runs on the JVM across a cluster, so DataFrame operations are distributed and optimized. Python UDFs run in Python workers and are much slower than built-in functions.

#### Why are Python UDFs slow in PySpark, and what are the alternatives?

Each row is serialized between the JVM and Python. Prefer built-in functions in `pyspark.sql.functions`, then pandas UDFs (vectorized with Arrow) if custom Python is unavoidable.

<!-- challenge -->

A PySpark job uses a UDF to compute `price * qty * (1 - discount)`. Why is that wasteful, and what replaces it?

<!-- solution -->

A Python UDF serializes every row to Python for simple arithmetic Spark can do natively. Use a column expression: `F.col("price") * F.col("qty") * (1 - F.col("discount"))`.

<!-- takeaways -->

- PySpark builds plans; the JVM executes them.
- Python UDFs serialize every row.
- Prefer built-ins; use pandas UDFs if needed.
