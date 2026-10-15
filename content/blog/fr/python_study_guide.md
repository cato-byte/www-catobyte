## Fiche d'étude Python

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Python : environ 200 questions](../../images/python_study_guide_title_img.png)

Environ 200 questions Python pour les entretiens de data engineer : le langage, la bibliothèque standard, la programmation orientée objet, les générateurs et décorateurs, la concurrence, les tests et le packaging, Python pour le travail sur les données, et une série d'exercices de code avec leurs solutions. Les exemples ciblent Python 3.12. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Bases du langage et types de données

#### Quelles sont les principales caractéristiques de Python ?

Un langage interprété, à typage dynamique et fort, avec ramasse-miettes, qui permet les styles procédural, orienté objet et fonctionnel. Il privilégie la lisibilité (l'indentation est significative) et dispose d'une vaste bibliothèque standard et d'un écosystème très riche.

#### Que signifient « typage dynamique » et « typage fort » pour Python ?

Typage dynamique : le type d'une variable est connu à l'exécution, et un nom peut être réaffecté à un objet d'un autre type. Typage fort : Python ne convertit pas silencieusement des types incompatibles, donc `"1" + 1` lève `TypeError` au lieu de deviner.

#### Quels sont les types de données intégrés de Python ?

Nombres (`int`, `float`, `complex`, `bool`), texte (`str`), séquences (`list`, `tuple`, `range`), binaire (`bytes`, `bytearray`, `memoryview`), ensembles (`set`, `frozenset`), dictionnaires (`dict`) et `NoneType`.

#### Quelle est la différence entre objets mutables et immuables ?

Les objets mutables peuvent être modifiés après leur création (`list`, `dict`, `set`, `bytearray`, la plupart des classes utilisateur). Les objets immuables ne le peuvent pas (`int`, `float`, `str`, `tuple`, `frozenset`, `bytes`) : les opérations créent de nouveaux objets. Seuls les objets hachables (en général immuables) peuvent être clés de dictionnaire ou éléments d'un ensemble.

#### Quelle est la différence entre `is` et `==` ?

`==` compare les valeurs (appelle `__eq__`). `is` compare l'identité : les deux noms désignent-ils le même objet ? N'utilisez `is` que pour les singletons comme `None` : `if x is None`.

#### Que signifie « tout est objet » en Python ?

Les nombres, les fonctions, les classes et les modules sont tous des objets, avec un type, une identité (`id()`) et des attributs. Les variables sont des noms liés à des objets, pas des boîtes qui contiennent des valeurs.

#### Comment les arguments sont-ils passés aux fonctions en Python ?

Par affectation (« appel par référence d'objet ») : le paramètre est lié au même objet que l'argument. Modifier un argument mutable est visible par l'appelant, réaffecter le paramètre ne l'est pas.

#### Qu'est-ce que `None` ?

L'unique instance de `NoneType`, qui représente l'absence de valeur. Les fonctions sans instruction `return` renvoient `None`.

#### Quelles valeurs sont considérées comme fausses en Python ?

`None`, `False`, le zéro de tout type numérique et les collections et chaînes vides (`''`, `[]`, `{}`, `set()`, `range(0)`). Les objets peuvent définir `__bool__` ou `__len__` pour contrôler leur valeur de vérité.

#### Quelle est la différence entre `/` et `//` ?

`/` est la division réelle et renvoie toujours un float (`7 / 2 == 3.5`). `//` est la division entière par défaut (`7 // 2 == 3`, `-7 // 2 == -4`).

#### Pourquoi `0.1 + 0.2 != 0.3` ?

Les float sont des nombres binaires IEEE 754, et 0,1 n'a pas de représentation binaire exacte. Comparez avec `math.isclose()` et utilisez `decimal.Decimal` pour les montants.

#### Quelle taille peut atteindre un int en Python ?

Arbitraire : les entiers Python ont une précision illimitée, bornée seulement par la mémoire.

#### Qu'est-ce que l'opérateur morse (walrus) ?

`:=` affecte une valeur à l'intérieur d'une expression :

```python
while (line := f.readline()):
    process(line)
```

#### Qu'est-ce qu'une instruction `match` ?

Le filtrage par motifs structurel (Python 3.10+), qui compare des valeurs à des motifs et les déstructure :

```python
match event:
    case {"type": "click", "x": x, "y": y}:
        handle_click(x, y)
    case {"type": "key", "key": k}:
        handle_key(k)
    case _:
        pass
```

#### Quelle est la différence entre une liste et un tuple ?

Les listes sont mutables et servent aux collections homogènes qui évoluent. Les tuples sont immuables, hachables (si leurs éléments le sont), un peu plus légers, et servent aux enregistrements fixes ou aux clés de dictionnaire.

#### Quelle est la différence entre copie superficielle et copie profonde ?

Une copie superficielle (`copy.copy`, `list(x)`, `x[:]`) crée un nouveau conteneur qui référence les mêmes objets internes. Une copie profonde (`copy.deepcopy`) copie aussi récursivement les objets internes.

#### Qu'est-ce que la règle LEGB ?

L'ordre dans lequel Python résout les noms : Local, portées des fonctions englobantes (Enclosing), Global (module), Built-in (intégrés).

#### Que font `global` et `nonlocal` ?

`global x` fait que les affectations dans une fonction réaffectent le `x` du module. `nonlocal x` réaffecte le `x` de la portée de fonction englobante la plus proche, ce qui est nécessaire pour modifier une variable de closure.

#### Quelle est la différence entre un module et un package ?

Un module est un fichier `.py` unique. Un package est un répertoire de modules, en général avec un `__init__.py`, importé avec des noms pointés.

#### Que fait `if __name__ == "__main__":` ?

Son bloc ne s'exécute que lorsque le fichier est lancé comme script, pas lorsqu'il est importé comme module. Il sert aux points d'entrée en ligne de commande.

### Chaînes, collections et compréhensions

#### Comment fonctionnent les f-strings ?

On préfixe une chaîne par `f` et on met des expressions entre accolades, avec des spécifications de format facultatives :

```python
total = 1234.5
print(f"Total: {total:,.2f} EUR, items: {len(items)}")   # Total: 1,234.50 EUR
print(f"{total=}")                                         # total=1234.5 (débogage)
```

#### Pourquoi les chaînes sont-elles immuables, et comment construire efficacement une longue chaîne ?

L'immuabilité rend les chaînes hachables et sûres à partager. Des `+=` répétés dans une boucle créent beaucoup de chaînes intermédiaires : rassemblez les morceaux dans une liste et utilisez `"".join(parts)`.

#### Quelle est la différence entre `str` et `bytes` ?

`str` est du texte Unicode. `bytes` est une suite d'octets bruts. On convertit avec `text.encode("utf-8")` et `data.decode("utf-8")`, en précisant toujours l'encodage à la lecture de fichiers.

#### Comment fonctionnent les tranches (slices) ?

`seq[start:stop:step]`, avec `stop` exclu et les indices négatifs comptés depuis la fin. `s[::-1]` inverse une séquence, `s[-3:]` prend les trois derniers éléments.

#### Qu'est-ce qu'une compréhension de liste ?

Une manière concise de construire une liste à partir d'un itérable, avec un filtre facultatif :

```python
squares = [x * x for x in range(10) if x % 2 == 0]
```

#### Que sont les compréhensions de dictionnaire et d'ensemble ?

```python
lengths = {name: len(name) for name in names}
initials = {name[0] for name in names}
```

#### Quelle est la différence entre une compréhension de liste et une expression génératrice ?

Une compréhension de liste construit toute la liste en mémoire. Une expression génératrice (entre parenthèses) produit les éléments paresseusement, un par un : `sum(x * x for x in range(10**8))` utilise une mémoire constante.

#### Comment un dict Python est-il implémenté, et quelles sont ses complexités ?

Comme une table de hachage : recherche, insertion et suppression sont en O(1) en moyenne. Depuis Python 3.7, les dictionnaires conservent l'ordre d'insertion.

#### Quelle est la complexité des opérations courantes sur les listes ?

L'accès par indice et `append` sont en O(1) (amorti pour append), `insert(0, x)` et `pop(0)` en O(n), `x in list` en O(n), le tri en O(n log n). Utilisez `collections.deque` pour des opérations rapides aux deux extrémités et des ensembles pour les tests d'appartenance.

#### Que fait `dict.get()`, et en quoi diffère-t-il de `dict[key]` ?

`d[key]` lève `KeyError` si la clé est absente. `d.get(key, default)` renvoie alors `default` (ou `None`).

#### Qu'est-ce que `collections.defaultdict` ?

Un dictionnaire qui crée une valeur par défaut pour les clés absentes à partir d'une fabrique :

```python
from collections import defaultdict
by_country = defaultdict(list)
for company in companies:
    by_country[company.country].append(company)
```

#### Qu'est-ce que `collections.Counter` ?

Une sous-classe de dictionnaire pour compter des éléments hachables, avec `most_common()` :

```python
from collections import Counter
Counter("mississippi").most_common(2)   # [('i', 4), ('s', 4)]
```

#### Qu'est-ce qu'un `namedtuple`, et comment se compare-t-il à une dataclass ?

`namedtuple` crée une sous-classe de tuple immuable avec des champs nommés. Une `dataclass` génère `__init__`, `__repr__` et `__eq__` pour une classe normale : mutable par défaut, plus souple, avec valeurs par défaut, annotations de type et `frozen=True` en option.

#### Qu'est-ce que `collections.deque` ?

Une file à double extrémité avec ajouts et retraits en O(1) des deux côtés, et un `maxlen` facultatif pour des tampons bornés.

#### Comment trier une liste de dictionnaires selon une clé ?

```python
rows.sort(key=lambda r: (r["country"], -r["revenue"]))
top = sorted(rows, key=operator.itemgetter("revenue"), reverse=True)[:10]
```

Le tri est stable : on peut trier selon plusieurs clés en passes successives.

#### Quelle est la différence entre `sort()` et `sorted()` ?

`list.sort()` trie sur place et renvoie `None`. `sorted()` accepte n'importe quel itérable et renvoie une nouvelle liste.

#### Comment fusionner deux dictionnaires ?

`merged = a | b` (Python 3.9+), ou `{**a, **b}`. Pour les clés en double, les valeurs de `b` l'emportent. `a |= b` met à jour sur place.

#### Que font `zip` et `enumerate` ?

`zip(a, b)` associe les éléments de plusieurs itérables (en s'arrêtant au plus court, ou en levant une erreur avec `strict=True`). `enumerate(seq, start=0)` produit des paires `(indice, élément)`.

#### Comment supprimer les doublons d'une liste en gardant l'ordre ?

```python
unique = list(dict.fromkeys(items))
```

#### Quelles sont les opérations sur les ensembles ?

Union `a | b`, intersection `a & b`, différence `a - b`, différence symétrique `a ^ b` et test d'inclusion `a <= b`. Les tests d'appartenance sont en O(1) en moyenne.

### Fonctions, portées et closures

#### Que sont `*args` et `**kwargs` ?

`*args` regroupe les arguments positionnels supplémentaires dans un tuple, `**kwargs` les arguments nommés supplémentaires dans un dictionnaire. À l'appel, `*` et `**` dépaquettent des séquences et des dictionnaires en arguments.

#### Que sont les paramètres uniquement nommés et uniquement positionnels ?

Les paramètres placés après `*` doivent être passés par nom. Ceux placés avant `/` doivent être passés par position :

```python
def connect(host, /, port=5432, *, timeout=10): ...
```

#### Pourquoi ne pas utiliser d'argument par défaut mutable ?

Les valeurs par défaut sont évaluées une seule fois, à la définition de la fonction : une valeur par défaut mutable est donc partagée entre les appels :

```python
def add(item, bucket=None):     # et non bucket=[]
    bucket = [] if bucket is None else bucket
    bucket.append(item)
    return bucket
```

#### Qu'est-ce qu'une lambda ?

Une fonction anonyme limitée à une seule expression : `lambda x: x * 2`. Surtout utilisée comme argument `key=` court. Pour tout ce qui est plus complexe, utilisez `def`.

#### Qu'est-ce qu'une closure ?

Une fonction qui se souvient de variables de la portée englobante où elle a été définie, même après la fin de cette portée :

```python
def multiplier(n):
    def times(x):
        return x * n
    return times

double = multiplier(2)
double(5)   # 10
```

#### Quel est le piège des closures à liaison tardive ?

Les closures cherchent les variables au moment de l'appel, pas de la définition :

```python
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]                       # [2, 2, 2]
funcs = [lambda i=i: i for i in range(3)]  # fige la valeur courante : [0, 1, 2]
```

#### Que sont les fonctions de première classe ?

Les fonctions sont des objets : on peut les affecter à des variables, les ranger dans des structures de données, les passer en argument et les renvoyer depuis d'autres fonctions.

#### Que sont `map`, `filter` et `functools.reduce` ?

`map(f, xs)` applique `f` à chaque élément, `filter(pred, xs)` garde les éléments pour lesquels `pred` est vrai (tous deux paresseux), et `reduce(f, xs, init)` réduit une séquence à une seule valeur. Les compréhensions sont en général plus lisibles que `map` et `filter`.

#### Que fait `functools.partial` ?

Elle crée une nouvelle fonction dont certains arguments sont fixés : `parse_fr = partial(parse_date, fmt="%d/%m/%Y")`.

#### Que fait `functools.lru_cache` (ou `cache`) ?

Il mémorise les résultats d'une fonction selon ses arguments (qui doivent être hachables) :

```python
from functools import cache

@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

#### Qu'est-ce que la récursivité, et quelle est la limite de récursion de Python ?

Une fonction qui s'appelle elle-même. CPython limite la profondeur (1000 par défaut, `sys.getrecursionlimit()`) et n'optimise pas la récursion terminale : une récursion profonde est généralement réécrite en boucle.

#### Que sont les docstrings ?

Des chaînes littérales placées en première instruction d'un module, d'une classe ou d'une fonction, accessibles via `__doc__` et affichées par `help()`.

#### Qu'est-ce qu'une fonction d'ordre supérieur ?

Une fonction qui prend ou renvoie d'autres fonctions, comme `sorted(key=...)`, les décorateurs ou `map`.

#### Que sont les annotations de type (type hints) ?

Des annotations des types attendus que Python ne vérifie pas à l'exécution, mais que des outils (mypy, pyright, les IDE) contrôlent :

```python
def total(prices: list[float], vat: float = 0.2) -> float:
    return sum(prices) * (1 + vat)
```

#### Qu'est-ce que `typing.Optional[X]` ?

Une annotation qui signifie `X | None`. Depuis Python 3.10, on peut écrire directement `X | None`.

#### Quelle est la différence entre une fonction et une méthode ?

Une méthode est une fonction définie dans une classe et accessible via une instance ou la classe, ce qui lie automatiquement le premier argument (`self` ou `cls`).

#### Comment renvoyer plusieurs valeurs depuis une fonction ?

En renvoyant un tuple et en le dépaquetant : `low, high = bounds(values)`. Au-delà de quelques valeurs, renvoyez une dataclass ou un tuple nommé.

#### Que fait le dépaquetage avec `*` dans les affectations ?

Il récupère les éléments restants : `first, *middle, last = [1, 2, 3, 4]` donne `middle == [2, 3]`.

#### Que sont `any()` et `all()` ?

`any(it)` est vrai si au moins un élément est vrai, `all(it)` si tous le sont (et vrai pour un itérable vide). Les deux s'arrêtent dès que le résultat est connu.

#### Comment Python évalue-t-il `and` et `or` ?

Avec un court-circuit, en renvoyant l'un des opérandes plutôt qu'un booléen : `x or default` renvoie `x` s'il est vrai, sinon `default`.

### Programmation orientée objet

#### Quelle est la différence entre une classe et une instance ?

Une classe est un modèle qui définit attributs et méthodes. Une instance est un objet créé à partir d'elle, avec son propre état : `p = Point(1, 2)`.

#### Qu'est-ce que `self` ?

Le premier paramètre des méthodes d'instance, lié à l'instance sur laquelle la méthode est appelée. Le nom est une convention, pas un mot-clé.

#### Qu'est-ce que `__init__`, et en quoi diffère-t-il de `__new__` ?

`__new__` crée et renvoie l'instance (rarement redéfini, surtout pour les types immuables et les singletons). `__init__` initialise une instance qui existe déjà.

#### Quelle est la différence entre attributs de classe et attributs d'instance ?

Les attributs de classe sont partagés par toutes les instances. Les attributs d'instance appartiennent à un objet. Affecter via `self.x = ...` crée un attribut d'instance qui masque celui de la classe.

#### Que sont `@staticmethod` et `@classmethod` ?

Une méthode statique ne reçoit aucun premier argument implicite : c'est une simple fonction dans l'espace de noms de la classe. Une méthode de classe reçoit la classe (`cls`), ce qui est utile pour des constructeurs alternatifs :

```python
class Company:
    @classmethod
    def from_row(cls, row: dict) -> "Company":
        return cls(row["id"], row["name"])
```

#### Qu'est-ce que `@property` ?

Un décorateur qui expose une méthode comme un attribut, avec setter et deleter facultatifs, pour ajouter validation ou calcul sans changer l'interface.

#### Qu'est-ce que l'héritage, et que fait `super()` ?

Une classe peut en étendre une autre et redéfinir ses méthodes. `super()` appelle l'implémentation du parent selon l'ordre de résolution des méthodes :

```python
class Lakehouse(Warehouse):
    def __init__(self, path):
        super().__init__()
        self.path = path
```

#### Qu'est-ce que l'ordre de résolution des méthodes (MRO) ?

L'ordre dans lequel Python cherche un attribut parmi les classes en cas d'héritage multiple, calculé par la linéarisation C3. On l'inspecte avec `Class.__mro__`.

#### Que sont les méthodes « dunder » (magiques) ?

Des méthodes entourées de doubles tirets bas qui s'insèrent dans le comportement du langage : `__repr__`, `__str__`, `__len__`, `__eq__`, `__hash__`, `__lt__`, `__iter__`, `__getitem__`, `__enter__`, `__call__`, `__add__`.

#### Quelle est la différence entre `__str__` et `__repr__` ?

`__repr__` est une représentation non ambiguë destinée aux développeurs (idéalement du code valide pour recréer l'objet). `__str__` est une représentation lisible destinée aux utilisateurs. `print()` utilise `__str__`, et à défaut `__repr__`.

#### Qu'est-ce qu'une dataclass ?

Une classe décorée par `@dataclass`, qui génère `__init__`, `__repr__` et `__eq__` à partir des champs annotés, avec des options comme `frozen=True`, `order=True` et `slots=True` :

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Snapshot:
    country: str
    rows: int
    files: list[str] = field(default_factory=list)
```

#### Que sont les classes de base abstraites ?

Des classes dérivées de `abc.ABC` dont des méthodes sont marquées `@abstractmethod`. On ne peut pas les instancier tant qu'une sous-classe n'implémente pas toutes les méthodes abstraites, ce qui impose une interface.

#### Qu'est-ce que le duck typing ?

Utiliser un objet selon son comportement plutôt que son type : « si ça marche comme un canard… ». Tout objet doté d'une méthode `read()` peut servir là où l'on attend un fichier.

#### Qu'est-ce qu'un Protocol ?

`typing.Protocol` définit des interfaces structurelles pour les vérificateurs de types statiques : toute classe qui possède les bonnes méthodes le satisfait, sans en hériter.

#### Que sont les `__slots__` ?

Un attribut de classe qui liste les attributs d'instance autorisés. Il supprime le `__dict__` de chaque instance, ce qui réduit la mémoire et accélère l'accès aux attributs pour de nombreux petits objets.

#### Qu'est-ce que la composition, et pourquoi la préfère-t-on souvent à l'héritage ?

Construire des objets à partir d'autres objets (« a un ») plutôt qu'étendre des classes (« est un »). Elle donne un couplage plus faible et évite les hiérarchies de classes profondes et fragiles.

#### Qu'est-ce que l'encapsulation en Python ?

Python n'a pas de membres privés. Par convention, `_name` est interne, et `__name` déclenche le name mangling (`_Class__name`) pour éviter les collisions dans les sous-classes.

#### Qu'est-ce qui rend un objet hachable ?

Un `__hash__` qui ne change pas pendant sa durée de vie et un `__eq__` cohérent avec lui (des objets égaux doivent avoir le même hash). Définir `__eq__` sans `__hash__` rend une classe non hachable.

#### Qu'est-ce qu'une métaclasse ?

La classe d'une classe (par défaut `type`), qui contrôle la création des classes. Rarement nécessaire : les décorateurs de classe et `__init_subclass__` couvrent la plupart des besoins.

#### Qu'est-ce que `__call__` ?

Une méthode qui rend les instances appelables comme des fonctions, utile pour des objets-fonctions configurables.

### Itérateurs, générateurs, décorateurs et gestionnaires de contexte

#### Quelle est la différence entre un itérable et un itérateur ?

Un itérable peut produire un itérateur (`__iter__`) : listes, dictionnaires, fichiers. Un itérateur produit les éléments un par un via `__next__` et lève `StopIteration` à la fin. Un itérateur ne se parcourt qu'une fois.

#### Qu'est-ce qu'un générateur ?

Une fonction qui contient `yield`. L'appeler renvoie un itérateur qui exécute la fonction paresseusement, en s'interrompant à chaque `yield` et en conservant son état entre les appels :

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

#### Pourquoi les générateurs sont-ils utiles en data engineering ?

Ils traitent les données en flux, avec une mémoire constante, quelle que soit la taille de l'entrée : lire des fichiers énormes ligne par ligne, paginer des API, chaîner des transformations paresseusement.

#### Que fait `yield from` ?

Il délègue à un sous-itérateur et en produit tous les éléments : `yield from read_batches(path)`.

#### Qu'est-ce qu'`itertools`, et citez quelques fonctions utiles ?

Un module de briques rapides pour les itérateurs : `chain`, `islice`, `groupby`, `product`, `permutations`, `combinations`, `accumulate`, `count`, `cycle`, `tee`, `zip_longest` et `batched` (Python 3.12).

#### Comment fonctionne `itertools.groupby`, et quel est le piège ?

Il regroupe les éléments consécutifs ayant la même clé : l'entrée doit donc d'abord être triée selon cette clé :

```python
from itertools import groupby
for country, rows in groupby(sorted(data, key=key), key=key):
    print(country, sum(1 for _ in rows))
```

#### Qu'est-ce qu'un décorateur ?

Un appelable qui prend une fonction et renvoie une remplaçante, appliqué avec `@`. Il ajoute un comportement (journalisation, chronométrage, nouvelles tentatives, cache, contrôle d'accès) sans modifier le code de la fonction.

#### Comment écrire un décorateur qui conserve les métadonnées de la fonction d'origine ?

Avec `functools.wraps` :

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

#### Comment écrire un décorateur avec des arguments ?

En ajoutant une fonction extérieure qui reçoit les arguments et renvoie le décorateur :

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

#### Qu'est-ce qu'un gestionnaire de contexte ?

Un objet utilisé avec `with` qui prépare et libère une ressource de façon fiable : `__enter__` s'exécute au début, `__exit__` à la fin, même en cas d'exception. Les fichiers, les verrous et les connexions aux bases de données sont des gestionnaires de contexte.

#### Comment écrire un gestionnaire de contexte avec `contextlib` ?

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

#### Que renvoie `__exit__` ?

Une valeur vraie supprime l'exception levée dans le bloc `with`, une valeur fausse la laisse se propager. Supprimer une exception doit rester rare et délibéré.

#### Qu'est-ce que `contextlib.ExitStack` ?

Un gestionnaire de contexte qui gère un nombre variable d'autres gestionnaires de contexte, par exemple pour ouvrir une liste variable de fichiers.

#### Qu'est-ce que l'évaluation paresseuse ?

Ne calculer les valeurs qu'au moment où l'on en a besoin. Les générateurs, `range`, `map`, `zip` et les vues de dictionnaire sont paresseux, ce qui économise la mémoire et permet des séquences infinies.

#### Comment rendre une classe itérable ?

En implémentant `__iter__`, en général sous forme de méthode génératrice :

```python
class Batch:
    def __init__(self, rows):
        self.rows = rows
    def __iter__(self):
        yield from self.rows
```

#### Que se passe-t-il si l'on parcourt deux fois un générateur ?

La seconde boucle ne produit rien : le générateur est épuisé. Recréez-le, ou stockez les résultats dans une liste si vous en avez besoin deux fois.

#### Qu'est-ce qu'une coroutine en Python ?

Une fonction définie avec `async def`, qui peut s'interrompre aux points `await`. Elle s'exécute dans une boucle d'événements (asyncio) et permet la concurrence pour les tâches limitées par les entrées-sorties.

#### Comment lire seulement les n premiers éléments d'un itérateur ?

`itertools.islice(it, n)`, qui fonctionne avec n'importe quel itérateur, y compris infini.

#### Comment découper un itérable en lots de taille fixe ?

`itertools.batched(iterable, n)` en Python 3.12+, ou avec `islice` dans une boucle pour les versions antérieures.

#### Quelle est la différence entre `return` et `yield` dans une fonction ?

`return` termine la fonction et renvoie une valeur. `yield` transforme la fonction en générateur qui produit une série de valeurs au fil du temps, en reprenant là où il s'était arrêté.

### Erreurs, fichiers et bibliothèque standard

#### Comment fonctionne la gestion des exceptions en Python ?

```python
try:
    value = int(raw)
except ValueError as exc:
    log.warning("bad value %r: %s", raw, exc)
    value = None
else:
    log.debug("parsed")         # s'exécute s'il n'y a pas eu d'exception
finally:
    cleanup()                   # s'exécute toujours
```

#### Pourquoi éviter un `except:` sans type ?

Il attrape aussi `KeyboardInterrupt`, `SystemExit` et les erreurs de programmation, ce qui masque les bugs. Attrapez les exceptions précises que vous savez traiter, ou au plus `Exception`.

#### Comment définir une exception personnalisée ?

En héritant d'`Exception` (ou d'une exception intégrée plus précise), en général avec une classe de base propre au projet :

```python
class PipelineError(Exception):
    """Base class for pipeline failures."""

class SchemaDriftError(PipelineError):
    pass
```

#### Qu'est-ce que le chaînage d'exceptions ?

`raise NewError(...) from exc` conserve l'exception d'origine comme cause, et la trace affiche les deux. `from None` masque l'exception d'origine.

#### Que sont les groupes d'exceptions ?

Python 3.11 a ajouté `ExceptionGroup` pour lever plusieurs exceptions à la fois (par exemple depuis des tâches concurrentes) et `except*` pour les traiter par type.

#### Qu'est-ce qu'EAFP par opposition à LBYL ?

« Il est plus facile de demander pardon que la permission » (tenter l'opération et attraper l'erreur) contre « Regarder avant de sauter » (vérifier d'abord). EAFP est idiomatique en Python et évite les conditions de concurrence entre la vérification et l'action.

#### Comment lire un gros fichier sans le charger en mémoire ?

En parcourant l'objet fichier, qui produit une ligne à la fois :

```python
with open("big.csv", encoding="utf-8") as f:
    for line in f:
        process(line)
```

#### Pourquoi toujours utiliser `with` pour ouvrir des fichiers ?

Il garantit la fermeture du fichier, même en cas d'exception, ce qui libère le descripteur et vide les écritures en attente.

#### Qu'est-ce que `pathlib` ?

Une API orientée objet pour les chemins de fichiers : `Path("data") / "raw" / "file.csv"`, `.exists()`, `.glob("*.csv")`, `.read_text()`, `.suffix`, `.stem`, `.mkdir(parents=True, exist_ok=True)`.

#### Comment lire et écrire des fichiers CSV avec la bibliothèque standard ?

```python
import csv

with open("in.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name"])
    writer.writeheader()
    writer.writerows(rows)
```

#### Comment travailler avec du JSON ?

`json.loads`/`json.dumps` pour les chaînes, `json.load`/`json.dump` pour les fichiers. Passez `default=` pour sérialiser les types non pris en charge comme les dates, et `ensure_ascii=False` pour garder les caractères accentués lisibles.

#### Comment analyser et formater des dates ?

Avec `datetime` :

```python
from datetime import datetime, timezone
d = datetime.strptime("15/10/2026", "%d/%m/%Y")
d.isoformat()                                  # '2026-10-15T00:00:00'
datetime.now(timezone.utc)                     # avec fuseau horaire
```

`zoneinfo.ZoneInfo("Europe/Paris")` donne les fuseaux horaires IANA.

#### Quelle est la différence entre datetimes naïfs et conscients ?

Un datetime naïf n'a pas de fuseau horaire, un datetime conscient a un `tzinfo`. Les mélanger provoque des erreurs. Stockez et calculez en UTC avec des datetimes conscients, et ne convertissez que pour l'affichage.

#### Comment bien utiliser le module `logging` ?

Créer un logger par module avec `logging.getLogger(__name__)`, journaliser avec un formatage paresseux (`log.info("loaded %d rows", n)`), configurer handlers et niveaux une seule fois au point d'entrée de l'application, et utiliser `log.exception()` dans les blocs `except` pour inclure la trace.

#### À quoi sert `argparse` ?

À construire des interfaces en ligne de commande avec arguments, options, types, valeurs par défaut et un `--help` automatique.

#### Qu'offre le module `re` ?

Les expressions régulières : `re.search`, `re.match`, `re.fullmatch`, `re.findall`, `re.sub`, `re.split`, les motifs compilés et les groupes nommés :

```python
m = re.fullmatch(r"(?P<code>\d{2})\.(?P<sub>\d{2})", "03.11")
m["code"]   # '03'
```

#### Comment lancer une commande externe depuis Python ?

Avec `subprocess.run`, en passant une liste d'arguments (sans shell) et en vérifiant le résultat :

```python
result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
```

#### Comment calculer l'empreinte de données ou de fichiers en Python ?

Avec `hashlib` : `hashlib.sha256(data).hexdigest()`. Pour les fichiers, lisez par blocs et appelez `update()` pour garder une mémoire constante.

#### À quoi sert `tempfile` ?

À créer des fichiers et des répertoires temporaires nettoyés automatiquement : `with tempfile.TemporaryDirectory() as tmp: ...`.

#### Comment compresser ou décompresser des fichiers en Python ?

Avec les modules `gzip`, `bz2`, `lzma` et `zipfile`. `gzip.open(path, "rt", encoding="utf-8")` lit un fichier texte compressé ligne par ligne.

### Concurrence et performances

#### Qu'est-ce que le GIL ?

Le Global Interpreter Lock de CPython ne laisse qu'un seul thread exécuter du bytecode Python à la fois. Les threads restent utiles pour le travail limité par les entrées-sorties, car le GIL est relâché pendant les attentes, mais pas pour du code Python pur limité par le CPU. Python 3.13 a introduit une version facultative sans GIL (free-threaded).

#### Quelle est la différence entre threading, multiprocessing et asyncio ?

- **threading :** plusieurs threads dans un processus. Bon pour les tâches limitées par les entrées-sorties (réseau, disque), limité par le GIL pour le calcul.
- **multiprocessing :** plusieurs processus, chacun avec son interpréteur. Bon pour le travail limité par le CPU, avec un surcoût plus élevé et des données transmises par pickle.
- **asyncio :** une concurrence coopérative dans un seul thread avec une boucle d'événements, pour un très grand nombre d'entrées-sorties concurrentes.

#### Qu'est-ce que `concurrent.futures` ?

Une interface de haut niveau avec `ThreadPoolExecutor` et `ProcessPoolExecutor` :

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=8) as pool:
    pages = list(pool.map(fetch, urls))
```

#### Comment fonctionne asyncio ?

Une boucle d'événements exécute des coroutines. À chaque `await` sur une entrée-sortie, la coroutine rend la main pour que d'autres puissent s'exécuter. `asyncio.gather` en lance plusieurs à la fois :

```python
import asyncio

async def main(urls):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(fetch(session, u) for u in urls))

asyncio.run(main(urls))
```

#### Qu'est-ce qu'une condition de concurrence, et comment l'éviter avec des threads ?

Deux threads qui accèdent à des données partagées et produisent un résultat qui dépend du hasard de l'ordonnancement. On l'évite avec des verrous (`threading.Lock`), des files thread-safe (`queue.Queue`) ou en évitant l'état mutable partagé.

#### Comment limiter la concurrence quand on appelle une API à débit limité ?

En bornant la taille du pool de workers, ou avec `asyncio.Semaphore`, et en ajoutant des nouvelles tentatives avec temporisation croissante sur les réponses 429.

#### Comment profiler du code Python ?

`cProfile` (`python -m cProfile -s cumtime script.py`) pour le temps par fonction, `timeit` pour de petits extraits, `tracemalloc` pour la mémoire, et des profileurs par échantillonnage comme py-spy pour un processus en cours.

#### Qu'est-ce qui rend vraiment le code Python plus rapide ?

De meilleurs algorithmes et structures de données (ensembles et dictionnaires pour les recherches), les fonctions intégrées et les compréhensions plutôt que des boucles manuelles, des bibliothèques vectorisées (NumPy, pandas, Polars) pour les calculs en masse, éviter les calculs répétés (cache), et déporter le travail lourd vers du code compilé ou un moteur distribué.

#### Pourquoi parcourir un DataFrame pandas ligne par ligne est-il lent ?

Chaque ligne devient un objet Python et le travail se fait dans l'interpréteur. Les opérations vectorisées s'exécutent en code C optimisé sur des colonnes entières à la fois.

#### Qu'est-ce qu'un comportement de type fuite mémoire en Python, et comment le trouver ?

Une mémoire qui ne cesse de croître parce que des références sont conservées (caches globaux, listes qui grandissent, cycles de références avec `__del__`). On l'étudie avec `tracemalloc`, `gc` et `objgraph`.

#### Comment Python gère-t-il la mémoire ?

Le comptage de références libère la plupart des objets dès que leur compteur tombe à zéro, et un ramasse-miettes cyclique (`gc`) nettoie les cycles de références.

#### Qu'est-ce que `__pycache__` ?

Le dossier où Python met en cache le bytecode compilé (fichiers `.pyc`) des modules importés, pour accélérer les imports suivants.

#### Quelle est la différence entre CPython et PyPy ?

CPython est l'interpréteur de référence, écrit en C. PyPy est une implémentation alternative avec un compilateur JIT qui accélère le code Python pur de longue durée, mais qui est moins compatible avec les extensions C.

#### Quand utiliser multiprocessing plutôt que Spark ?

Pour du travail limité par le CPU qui tient sur une machine et en mémoire. Utilisez Spark quand les données ou les calculs dépassent une machine, ou quand la plateforme tourne déjà sous Spark.

#### Qu'est-ce que pickle, et quels en sont les risques ?

La sérialisation d'objets Python en octets avec `pickle`. Ne désérialisez jamais des données non fiables : cela peut exécuter du code arbitraire. Utilisez JSON ou Parquet pour l'échange de données.

#### Pourquoi ne peut-on pas envoyer une lambda à un pool de processus ?

`ProcessPoolExecutor` sérialise la fonction avec pickle pour l'envoyer aux workers, et les lambdas et fonctions imbriquées ne peuvent pas être sérialisées par référence. Utilisez des fonctions de niveau module.

#### Qu'est-ce qu'un thread démon (daemon) ?

Un thread d'arrière-plan qui n'empêche pas le programme de se terminer. Il est tué brutalement à la sortie : il ne doit donc pas détenir de ressources à nettoyer.

#### Comment fixer un délai d'expiration sur un appel réseau bloquant ?

En passant un timeout à la bibliothèque (`requests.get(url, timeout=30)`). N'appelez jamais un service externe sans : une connexion bloquée attendrait indéfiniment.

#### En quoi `asyncio.run` diffère-t-il d'un appel direct à une coroutine ?

Appeler une fonction `async def` crée seulement un objet coroutine. `asyncio.run(coro)` crée une boucle d'événements, exécute la coroutine jusqu'au bout et ferme la boucle.

#### Qu'est-ce que la contre-pression (backpressure), et comment la gérer dans des pipelines Python ?

Quand les producteurs vont plus vite que les consommateurs, la mémoire grossit jusqu'à la panne. Utilisez des files bornées (`queue.Queue(maxsize=...)`, `asyncio.Queue(maxsize=...)`) pour que les producteurs attendent.

### Typage, packaging, environnements et tests

#### Qu'est-ce qu'un environnement virtuel, et pourquoi en utiliser un ?

Une installation Python isolée avec ses propres paquets (`python -m venv .venv`), pour que chaque projet ait ses propres versions de dépendances sans casser le Python du système ni les autres projets.

#### Qu'est-ce que `pyproject.toml` ?

Le fichier de configuration standard des projets Python : système de build, métadonnées, dépendances, points d'entrée et réglages des outils (pytest, ruff, mypy).

#### Comment rendre l'installation des dépendances reproductible ?

Figer les versions exactes dans un fichier de verrouillage (`uv lock`, `pip-tools`, Poetry), installer à partir de lui en CI et en production, et mettre à jour les dépendances délibérément.

#### Qu'est-ce que `uv` ?

Un gestionnaire de paquets et de projets Python très rapide, écrit en Rust, qui remplace les flux pip, pip-tools et virtualenv (`uv add`, `uv sync`, `uv run`) et sait installer des versions de Python.

#### Qu'est-ce qu'un wheel ?

Un format de distribution précompilé (`.whl`) qui s'installe sans étape de build. Les jobs Databricks, par exemple, exécutent du code empaqueté en wheels.

#### Qu'est-ce qu'un point d'entrée (entry point) ?

Un script console déclaré dans `pyproject.toml` qui installe une commande appelant une fonction Python :

```toml
[project.scripts]
registry-lakehouse = "registry_lakehouse.cli:main"
```

#### Qu'est-ce que pytest, et pourquoi le préfère-t-on à unittest ?

Un framework de tests où les tests sont de simples fonctions avec de simples `assert`, avec des messages d'échec détaillés, des fixtures, la paramétrisation et un large écosystème de plugins.

#### Que sont les fixtures pytest ?

Des fonctions qui fournissent les dépendances des tests (données, connexions, une session Spark), injectées par nom d'argument, avec des portées (fonction, module, session) et un nettoyage après le `yield` :

```python
@pytest.fixture(scope="session")
def spark():
    session = SparkSession.builder.master("local[2]").getOrCreate()
    yield session
    session.stop()
```

#### Qu'est-ce que la paramétrisation dans pytest ?

Exécuter un même test avec plusieurs entrées :

```python
@pytest.mark.parametrize("raw, expected", [("311.0", "03.11"), ("4782", "47.82")])
def test_nace(raw, expected):
    assert nace_from_numeric(raw) == expected
```

#### Qu'est-ce que le mocking, et comment le pratiquer ?

Remplacer une dépendance par un faux objet dans un test, pour isoler le code et éviter les appels réseau ou base de données : `unittest.mock.patch`, `MagicMock`, ou le `monkeypatch` de pytest.

#### Qu'est-ce que le test par propriétés ?

Générer de nombreuses entrées aléatoires pour vérifier qu'une propriété est toujours vraie, au lieu d'écrire des exemples à la main. Hypothesis est la bibliothèque Python dédiée, et elle réduit les échecs à un exemple minimal.

#### Qu'est-ce que la couverture de tests, et viser 100 % est-il un bon objectif ?

La part du code exécutée par les tests (`pytest-cov`). Elle montre les zones non testées, mais une forte couverture ne prouve pas que les tests vérifient les bonnes choses. Visez des tests utiles sur la logique risquée.

#### Quelle est la différence entre tests unitaires, d'intégration et de bout en bout ?

Les tests unitaires vérifient une fonction ou une classe isolément. Les tests d'intégration vérifient des composants qui fonctionnent ensemble (le code et une base de données). Les tests de bout en bout exécutent tout le système sur des entrées réalistes.

#### Quels outils maintiennent la qualité du code Python ?

Un formateur et un linter (ruff, ou black et flake8), un vérificateur de types (mypy, pyright), des hooks pre-commit, des tests en CI et la revue de code.

#### Comment vérifier les types avec mypy ?

Ajouter des annotations de type et lancer `mypy src/`. Il signale les incohérences de types de façon statique, avant l'exécution. On l'adopte progressivement avec des réglages par module.

#### Qu'est-ce que `TypedDict` ?

Une construction de typage qui décrit des dictionnaires avec un ensemble fixe de clés et de types de valeurs, utile pour des enregistrements de type JSON.

#### Que sont les génériques dans les annotations de type ?

Des types paramétrés comme `list[int]` ou `dict[str, float]`, ainsi que vos propres classes et fonctions génériques. Python 3.12 a une syntaxe compacte : `def first[T](xs: list[T]) -> T: ...`.

#### Comment gérer la configuration et les secrets dans une application Python ?

Les lire depuis des variables d'environnement ou un gestionnaire de secrets au démarrage, les valider (par exemple avec pydantic-settings), garder les fichiers `.env` hors de la gestion de versions, et ne jamais écrire d'identifiants en dur.

#### Qu'est-ce que pydantic ?

Une bibliothèque de validation de données qui transforme les données en modèles typés et lève des erreurs claires sur les entrées invalides. Utilisée pour les charges utiles d'API, la configuration et les contrats.

#### Comment structurer un projet Python pour un pipeline de données ?

Une organisation `src/` avec un package découpé par responsabilité (ingestion, transformations, qualité, entrées-sorties), un point d'entrée CLI léger, une configuration séparée du code, des tests qui reflètent le package, et `pyproject.toml` pour les dépendances et les outils.

### Python pour le data engineering

#### Comment lire un gros CSV avec pandas sans manquer de mémoire ?

Lire par blocs, ne sélectionner que les colonnes utiles, fixer des types compacts, ou utiliser un format en colonnes et un moteur paresseux :

```python
for chunk in pd.read_csv("big.csv", usecols=["id", "amount"], dtype={"id": "int64"}, chunksize=500_000):
    process(chunk)
```

#### Quelle est la différence entre `loc` et `iloc` dans pandas ?

`loc` sélectionne par étiquettes (valeurs de l'index et noms de colonnes, borne de fin incluse). `iloc` sélectionne par position entière (borne de fin exclue).

#### Comment éviter le `SettingWithCopyWarning` dans pandas ?

Utiliser `.loc[row_selector, column] = value` sur le DataFrame d'origine, ou faire un `.copy()` explicite quand on veut travailler sur un sous-ensemble. Avec le copy-on-write (par défaut dans pandas 3), une affectation chaînée ne modifie tout simplement pas l'original.

#### Comment regrouper et agréger dans pandas ?

```python
summary = (df.groupby(["country", "industry"], as_index=False)
             .agg(companies=("id", "count"), employees=("employees", "sum")))
```

#### Quels types de jointure propose `pandas.merge` ?

`how="inner"`, `"left"`, `"right"`, `"outer"` et `"cross"`, sur des colonnes `on=` ou `left_on`/`right_on`. `validate="one_to_one"` ou `"many_to_one"` détecte des clés en double inattendues, et `indicator=True` montre l'origine de chaque ligne.

#### Comment gérer les valeurs manquantes dans pandas ?

Les détecter avec `isna()`, les supprimer avec `dropna()`, les remplir avec `fillna()` ou `ffill()`, et utiliser les types nullables (`Int64`, `string`, `boolean`) pour que des entiers avec valeurs manquantes ne deviennent pas des float.

#### Qu'est-ce qu'Apache Parquet, et pourquoi le préférer au CSV ?

Un format de fichier en colonnes, compressé et typé. Les requêtes ne lisent que les colonnes nécessaires, les fichiers sont bien plus petits, les types sont conservés et des statistiques permettent de sauter des données. Le CSV est du texte en lignes, sans types.

#### Qu'est-ce qu'Apache Arrow ?

Un format standard en mémoire orienté colonnes. Il permet à pandas, Polars, DuckDB, Spark et d'autres d'échanger des données sans les copier ni les convertir. PyArrow est sa bibliothèque Python.

#### Qu'est-ce que Polars, et quand l'utiliser plutôt que pandas ?

Une bibliothèque de DataFrames écrite en Rust, multithread, avec un optimiseur de requêtes paresseux. Elle est souvent bien plus rapide et plus économe en mémoire que pandas pour les gros traitements sur une seule machine.

#### Qu'est-ce que DuckDB ?

Une base de données analytique SQL embarquée. Elle interroge directement et très vite des fichiers Parquet, CSV et des DataFrames, sans serveur : `duckdb.sql("select country, count(*) from 'data/*.parquet' group by 1")`.

#### Comment appeler une API REST de façon robuste depuis Python ?

Utiliser une session, fixer des timeouts, relancer les erreurs transitoires avec une temporisation exponentielle, gérer la pagination, respecter les limites de débit et valider les réponses :

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

#### Comment télécharger un gros fichier sans le charger en mémoire ?

En flux, par blocs :

```python
with requests.get(url, stream=True, timeout=60) as r:
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
```

#### Comment se connecter à une base de données depuis Python en toute sécurité ?

Avec un pilote (psycopg pour PostgreSQL) ou SQLAlchemy, en utilisant des requêtes paramétrées et jamais du formatage de chaînes, pour éviter l'injection SQL :

```python
cur.execute("select * from companies where country = %s", (country,))
```

#### Comment charger rapidement beaucoup de lignes dans PostgreSQL depuis Python ?

Utiliser `COPY` (le `cursor.copy()` de psycopg) plutôt que des insertions ligne à ligne, ou des insertions par lots avec `executemany` et des tailles de page. Faire le chargement dans une seule transaction.

#### Qu'est-ce que SQLAlchemy ?

Une boîte à outils pour bases de données avec une couche Core (langage d'expressions SQL, pool de connexions, engines) et un ORM. pandas utilise des engines SQLAlchemy pour `read_sql` et `to_sql`.

#### Comment lire des fichiers depuis Amazon S3 en Python ?

Avec boto3 (`s3.get_object`, `download_file`, paginateurs pour lister), ou via fsspec et s3fs pour que pandas, Polars et PyArrow lisent directement des chemins `s3://`. Les identifiants doivent venir de rôles ou de l'environnement, jamais du code.

#### Comment rendre une étape de pipeline idempotente ?

L'exécuter deux fois sur la même entrée doit donner le même résultat : écrire à un emplacement déterministe et l'écraser (ou fusionner sur des clés) plutôt qu'ajouter, utiliser des identifiants d'exécution, et vérifier si le travail a déjà été fait.

#### Comment valider un jeu de données en Python avant de le charger ?

Vérifier le schéma (colonnes et types), les valeurs nulles dans les champs obligatoires, les plages de valeurs, l'unicité des clés et le nombre de lignes par rapport aux attentes, avec du code, pydantic ou une bibliothèque comme pandera ou Great Expectations. Échouer visiblement ou mettre en quarantaine les lignes invalides.

#### Qu'est-ce que PySpark, et quel est son lien avec Python ?

L'API Python d'Apache Spark. Le code Python construit un plan de requête qui s'exécute dans la JVM sur un cluster : les opérations sur DataFrames sont distribuées et optimisées. Les UDF Python s'exécutent dans des workers Python et sont bien plus lentes que les fonctions intégrées.

#### Pourquoi les UDF Python sont-elles lentes dans PySpark, et quelles sont les alternatives ?

Chaque ligne est sérialisée entre la JVM et Python. Préférez les fonctions intégrées de `pyspark.sql.functions`, puis les pandas UDF (vectorisées avec Arrow) si un code Python sur mesure est inévitable.

#### Comment traiter les problèmes d'encodage à la lecture de fichiers ?

Indiquer explicitement le bon `encoding`, n'utiliser `errors="replace"` qu'en connaissance de cause, détecter un BOM avec `encoding="utf-8-sig"`, et réparer le mojibake (`'TravesÃ­a'.encode('latin-1').decode('utf-8')`) avec une garde pour les chaînes où la conversion échoue.

#### Comment planifier et orchestrer des pipelines Python ?

Avec un orchestrateur comme Airflow, Dagster ou Prefect (dépendances, relances, alertes, recalculs d'historique), ou un planificateur cloud qui déclenche des fonctions serverless ou des conteneurs dans les cas simples.

#### Comment traiter un fichier JSON trop gros pour être chargé d'un coup ?

Privilégier le JSON délimité par des sauts de ligne et le lire ligne par ligne. Pour un unique tableau JSON énorme, utiliser un analyseur en flux comme ijson pour parcourir les éléments sans tout charger.

#### Quelle est la différence entre ETL et ELT du point de vue d'un développeur Python ?

En ETL, le code Python transforme les données avant de les charger. En ELT, Python sert surtout à extraire et charger des données brutes, et les transformations s'exécutent en SQL dans l'entrepôt (souvent avec dbt). Python garde ce que SQL fait mal : les API, les fichiers, les analyses complexes.

#### Comment écrire un fichier Parquet partitionné par une colonne ?

```python
import pyarrow as pa, pyarrow.parquet as pq
pq.write_to_dataset(pa.Table.from_pandas(df), root_path="out/", partition_cols=["country"])
```

Cela crée des dossiers comme `out/country=FR/`, que les moteurs de requête peuvent élaguer.

### Exercices de code

#### Analyser un fichier de journal et indiquer combien de temps un appareil est resté allumé et quand les erreurs se sont produites.

Chaque ligne a la forme `Jul 11 16:11:51:490 [139681125603136] dut: Device State: ON`. Seuls les messages `ON`, `ERR` et `OFF` comptent. Le rapport doit indiquer la durée pendant laquelle l'appareil est resté allumé et lister les horodatages des erreurs.

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

L'horodatage correspond aux trois premiers champs de la ligne (mois, jour, heure), pas au seul troisième champ. L'analyser avec `strptime` (`%f` accepte les millisecondes) donne un datetime, et la différence de deux datetimes donne un `timedelta`. Notez aussi `errors.append()` (les listes n'ont pas de `add`), le parcours direct de l'objet fichier, et le contrôle de l'état en fin de ligne pour que `ON` ne soit pas trouvé à l'intérieur d'un autre mot.

#### Inverser une chaîne et vérifier si c'est un palindrome, sans tenir compte de la casse ni de la ponctuation.

```python
def is_palindrome(text: str) -> bool:
    letters = [c.lower() for c in text if c.isalnum()]
    return letters == letters[::-1]
```

#### Trouver les deux nombres d'une liste dont la somme vaut une cible (two-sum).

Utiliser un dictionnaire des valeurs déjà vues pour obtenir du O(n) :

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i
    return None
```

#### Compter la fréquence des mots d'un texte et renvoyer les dix premiers.

```python
import re
from collections import Counter

def top_words(text: str, n: int = 10) -> list[tuple[str, int]]:
    return Counter(re.findall(r"\w+", text.lower())).most_common(n)
```

#### Aplatir une liste imbriquée de profondeur quelconque.

```python
def flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

list(flatten([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]
```

#### Regrouper une liste d'anagrammes.

```python
from collections import defaultdict

def group_anagrams(words: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())
```

#### Dédoublonner des enregistrements en gardant la version la plus récente de chaque clé.

```python
def latest_by_key(rows: list[dict], key: str, ts: str) -> list[dict]:
    latest = {}
    for row in rows:
        current = latest.get(row[key])
        if current is None or row[ts] > current[ts]:
            latest[row[key]] = row
    return list(latest.values())
```

#### Fusionner des intervalles qui se chevauchent.

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

#### Vérifier qu'une chaîne de parenthèses est équilibrée.

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

#### Écrire une fonction qui découpe une liste en morceaux de taille n.

```python
def chunks(items: list, n: int) -> list[list]:
    return [items[i:i + n] for i in range(0, len(items), n)]
```

#### Trouver le premier caractère non répété d'une chaîne.

```python
from collections import Counter

def first_unique(s: str) -> str | None:
    counts = Counter(s)
    return next((c for c in s if counts[c] == 1), None)
```

#### Valider un numéro SIREN avec l'algorithme de Luhn.

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

#### Calculer un total cumulé et une moyenne mobile sur 3 éléments.

```python
from itertools import accumulate

values = [3, 5, 2, 8, 6]
running = list(accumulate(values))                                         # [3, 8, 10, 18, 24]
moving = [sum(values[i - 2:i + 1]) / 3 for i in range(2, len(values))]     # [3.33, 5.0, 5.33]
```

#### Lire un CSV de transactions, calculer le montant total par utilisateur et les villes dont la moyenne dépasse 8 000.

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

#### Écrire un générateur qui produit indéfiniment les nombres de Fibonacci, et prendre les dix premiers.

```python
from itertools import islice

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

list(islice(fibonacci(), 10))   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```
