## Guía de estudio de Python

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Python: unas 200 preguntas](../../images/python_study_guide_title_img.png)

Unas 200 preguntas de Python para entrevistas de ingeniería de datos: el lenguaje, la biblioteca estándar, la programación orientada a objetos, los generadores y decoradores, la concurrencia, los tests y el empaquetado, Python para trabajar con datos, y una serie de problemas de programación con sus soluciones. Los ejemplos usan Python 3.12. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Fundamentos del lenguaje y tipos de datos

#### ¿Cuáles son las características principales de Python?

Un lenguaje interpretado, de tipado dinámico y fuerte, con recolección de basura, que admite los estilos procedural, orientado a objetos y funcional. Prima la legibilidad (la indentación es significativa) y tiene una biblioteca estándar y un ecosistema enormes.

#### ¿Qué significa que Python tenga tipado dinámico y fuerte?

Tipado dinámico: el tipo de una variable se conoce en tiempo de ejecución y un nombre puede volver a asignarse a un objeto de otro tipo. Tipado fuerte: Python no convierte en silencio tipos incompatibles, así que `"1" + 1` lanza `TypeError` en lugar de adivinar.

#### ¿Cuáles son los tipos de datos integrados de Python?

Números (`int`, `float`, `complex`, `bool`), texto (`str`), secuencias (`list`, `tuple`, `range`), binarios (`bytes`, `bytearray`, `memoryview`), conjuntos (`set`, `frozenset`), mapeos (`dict`) y `NoneType`.

#### ¿Qué diferencia hay entre objetos mutables e inmutables?

Los objetos mutables pueden cambiar después de crearse (`list`, `dict`, `set`, `bytearray`, la mayoría de las clases propias). Los inmutables no (`int`, `float`, `str`, `tuple`, `frozenset`, `bytes`): sus operaciones crean objetos nuevos. Solo los objetos hashables (normalmente inmutables) pueden ser claves de diccionario o elementos de un conjunto.

#### ¿Qué diferencia hay entre `is` y `==`?

`==` compara valores (llama a `__eq__`). `is` compara identidad: si los dos nombres se refieren al mismo objeto. Usa `is` solo con singletons como `None`: `if x is None`.

#### ¿Qué significa "todo es un objeto" en Python?

Los números, las funciones, las clases y los módulos son objetos con un tipo, una identidad (`id()`) y atributos. Las variables son nombres ligados a objetos, no cajas que contienen valores.

#### ¿Cómo se pasan los argumentos a las funciones en Python?

Por asignación ("llamada por referencia a objeto"): el parámetro queda ligado al mismo objeto que el argumento. Modificar un argumento mutable se ve desde quien llama, pero reasignar el parámetro no.

#### ¿Qué es `None`?

La única instancia de `NoneType`, que representa la ausencia de valor. Las funciones sin sentencia `return` devuelven `None`.

#### ¿Qué valores son falsos en Python?

`None`, `False`, el cero de cualquier tipo numérico y las colecciones y cadenas vacías (`''`, `[]`, `{}`, `set()`, `range(0)`). Los objetos pueden definir `__bool__` o `__len__` para controlar su valor de verdad.

#### ¿Qué diferencia hay entre `/` y `//`?

`/` es la división real y siempre devuelve un float (`7 / 2 == 3.5`). `//` es la división entera hacia abajo (`7 // 2 == 3`, `-7 // 2 == -4`).

#### ¿Por qué `0.1 + 0.2 != 0.3`?

Los float son números binarios IEEE 754 y 0,1 no tiene una representación binaria exacta. Compara con `math.isclose()` y usa `decimal.Decimal` para importes monetarios.

#### ¿Qué tamaño puede tener un int en Python?

Arbitrariamente grande: los enteros de Python tienen precisión ilimitada, solo limitada por la memoria.

#### ¿Qué es el operador morsa (walrus)?

`:=` asigna un valor dentro de una expresión:

```python
while (line := f.readline()):
    process(line)
```

#### ¿Qué es una sentencia `match`?

La coincidencia estructural de patrones (Python 3.10+), que compara valores con patrones y los desestructura:

```python
match event:
    case {"type": "click", "x": x, "y": y}:
        handle_click(x, y)
    case {"type": "key", "key": k}:
        handle_key(k)
    case _:
        pass
```

#### ¿Qué diferencia hay entre una lista y una tupla?

Las listas son mutables y sirven para colecciones homogéneas que cambian. Las tuplas son inmutables, hashables (si lo son sus elementos), algo más ligeras, y se usan para registros fijos o como claves de diccionario.

#### ¿Qué diferencia hay entre una copia superficial y una profunda?

Una copia superficial (`copy.copy`, `list(x)`, `x[:]`) crea un contenedor nuevo con referencias a los mismos objetos internos. Una copia profunda (`copy.deepcopy`) copia también, de forma recursiva, los objetos internos.

#### ¿Qué es la regla LEGB?

El orden en que Python resuelve los nombres: Local, ámbitos de las funciones contenedoras (Enclosing), Global (módulo) y Built-in (integrados).

#### ¿Qué hacen `global` y `nonlocal`?

`global x` hace que las asignaciones dentro de una función reasignen la `x` del módulo. `nonlocal x` reasigna la `x` del ámbito de la función contenedora más cercana, algo necesario para modificar una variable de un closure.

#### ¿Qué diferencia hay entre un módulo y un paquete?

Un módulo es un único archivo `.py`. Un paquete es un directorio de módulos, normalmente con un `__init__.py`, que se importa con nombres con puntos.

#### ¿Qué hace `if __name__ == "__main__":`?

Su bloque solo se ejecuta cuando el archivo se lanza como script, no cuando se importa como módulo. Se usa para los puntos de entrada de línea de comandos.

### Cadenas, colecciones y comprensiones

#### ¿Cómo funcionan las f-strings?

Se antepone una `f` a la cadena y se ponen expresiones entre llaves, con especificaciones de formato opcionales:

```python
total = 1234.5
print(f"Total: {total:,.2f} EUR, items: {len(items)}")   # Total: 1,234.50 EUR
print(f"{total=}")                                         # total=1234.5 (para depurar)
```

#### ¿Por qué las cadenas son inmutables y cómo se construye una cadena larga de forma eficiente?

La inmutabilidad hace que las cadenas sean hashables y seguras de compartir. Hacer `+=` repetidamente en un bucle crea muchas cadenas intermedias, así que reúne las partes en una lista y usa `"".join(parts)`.

#### ¿Qué diferencia hay entre `str` y `bytes`?

`str` es texto Unicode. `bytes` es una secuencia de bytes en bruto. Se convierte con `text.encode("utf-8")` y `data.decode("utf-8")`, indicando siempre la codificación al leer archivos.

#### ¿Cómo funcionan las rebanadas (slices)?

`seq[start:stop:step]`, con `stop` excluido y los índices negativos contando desde el final. `s[::-1]` invierte una secuencia y `s[-3:]` toma los tres últimos elementos.

#### ¿Qué es una comprensión de listas?

Una forma concisa de construir una lista a partir de un iterable, con un filtro opcional:

```python
squares = [x * x for x in range(10) if x % 2 == 0]
```

#### ¿Qué son las comprensiones de diccionarios y de conjuntos?

```python
lengths = {name: len(name) for name in names}
initials = {name[0] for name in names}
```

#### ¿Qué diferencia hay entre una comprensión de listas y una expresión generadora?

Una comprensión de listas construye toda la lista en memoria. Una expresión generadora (entre paréntesis) produce los elementos de forma perezosa, uno a uno: `sum(x * x for x in range(10**8))` usa memoria constante.

#### ¿Cómo está implementado un dict de Python y cuál es su complejidad?

Como una tabla hash: la búsqueda, la inserción y el borrado son O(1) de media. Desde Python 3.7, los diccionarios conservan el orden de inserción.

#### ¿Cuál es la complejidad temporal de las operaciones habituales de las listas?

El acceso por índice y `append` son O(1) (amortizado en el caso de append), `insert(0, x)` y `pop(0)` son O(n), `x in list` es O(n) y ordenar es O(n log n). Usa `collections.deque` para operaciones rápidas en los dos extremos y conjuntos para comprobar pertenencia.

#### ¿Qué hace `dict.get()` y en qué se diferencia de `dict[key]`?

`d[key]` lanza `KeyError` si la clave no existe. `d.get(key, default)` devuelve `default` (o `None`) en ese caso.

#### ¿Qué es `collections.defaultdict`?

Un diccionario que crea un valor por defecto para las claves que faltan a partir de una fábrica:

```python
from collections import defaultdict
by_country = defaultdict(list)
for company in companies:
    by_country[company.country].append(company)
```

#### ¿Qué es `collections.Counter`?

Una subclase de diccionario para contar elementos hashables, con `most_common()`:

```python
from collections import Counter
Counter("mississippi").most_common(2)   # [('i', 4), ('s', 4)]
```

#### ¿Qué es una `namedtuple` y cómo se compara con una dataclass?

`namedtuple` crea una subclase de tupla inmutable con campos con nombre. Una `dataclass` genera `__init__`, `__repr__` y `__eq__` para una clase normal: mutable por defecto, más flexible, con valores por defecto, anotaciones de tipo y `frozen=True` opcional.

#### ¿Qué es `collections.deque`?

Una cola doble con añadidos y extracciones O(1) en ambos extremos, y un `maxlen` opcional para búferes acotados.

#### ¿Cómo se ordena una lista de diccionarios por una clave?

```python
rows.sort(key=lambda r: (r["country"], -r["revenue"]))
top = sorted(rows, key=operator.itemgetter("revenue"), reverse=True)[:10]
```

La ordenación es estable, así que se puede ordenar por varias claves en pasadas sucesivas.

#### ¿Qué diferencia hay entre `sort()` y `sorted()`?

`list.sort()` ordena en el sitio y devuelve `None`. `sorted()` acepta cualquier iterable y devuelve una lista nueva.

#### ¿Cómo se fusionan dos diccionarios?

`merged = a | b` (Python 3.9+), o `{**a, **b}`. En las claves repetidas ganan los valores de `b`. `a |= b` actualiza en el sitio.

#### ¿Qué hacen `zip` y `enumerate`?

`zip(a, b)` empareja elementos de varios iterables (se detiene en el más corto, o lanza un error con `strict=True`). `enumerate(seq, start=0)` produce pares `(índice, elemento)`.

#### ¿Cómo se eliminan los duplicados de una lista conservando el orden?

```python
unique = list(dict.fromkeys(items))
```

#### ¿Cuáles son las operaciones de conjuntos?

Unión `a | b`, intersección `a & b`, diferencia `a - b`, diferencia simétrica `a ^ b` y la comprobación de subconjunto `a <= b`. Comprobar la pertenencia es O(1) de media.

### Funciones, ámbitos y closures

#### ¿Qué son `*args` y `**kwargs`?

`*args` recoge los argumentos posicionales adicionales en una tupla, y `**kwargs` los argumentos con nombre adicionales en un diccionario. En una llamada, `*` y `**` desempaquetan secuencias y mapeos como argumentos.

#### ¿Qué son los parámetros solo con nombre y solo posicionales?

Los parámetros después de `*` deben pasarse por nombre. Los que van antes de `/` deben pasarse por posición:

```python
def connect(host, /, port=5432, *, timeout=10): ...
```

#### ¿Por qué no se debe usar un argumento por defecto mutable?

Los valores por defecto se evalúan una sola vez, al definir la función, así que un valor por defecto mutable se comparte entre llamadas:

```python
def add(item, bucket=None):     # y no bucket=[]
    bucket = [] if bucket is None else bucket
    bucket.append(item)
    return bucket
```

#### ¿Qué es una lambda?

Una función anónima limitada a una expresión: `lambda x: x * 2`. Se usa sobre todo como argumento `key=` corto. Para cualquier cosa más compleja, usa `def`.

#### ¿Qué es un closure?

Una función que recuerda variables del ámbito donde se definió, incluso después de que ese ámbito haya terminado:

```python
def multiplier(n):
    def times(x):
        return x * n
    return times

double = multiplier(2)
double(5)   # 10
```

#### ¿Qué es la trampa de los closures de enlace tardío?

Los closures buscan las variables al llamarse, no al definirse:

```python
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]                       # [2, 2, 2]
funcs = [lambda i=i: i for i in range(3)]  # fija el valor actual: [0, 1, 2]
```

#### ¿Qué son las funciones de primera clase?

Las funciones son objetos: se pueden asignar a variables, guardar en estructuras de datos, pasar como argumentos y devolver desde otras funciones.

#### ¿Qué son `map`, `filter` y `functools.reduce`?

`map(f, xs)` aplica `f` a cada elemento, `filter(pred, xs)` conserva los elementos para los que `pred` es verdadero (ambos perezosos), y `reduce(f, xs, init)` reduce una secuencia a un solo valor. Las comprensiones suelen ser más legibles que `map` y `filter`.

#### ¿Qué hace `functools.partial`?

Crea una función nueva con algunos argumentos fijados: `parse_fr = partial(parse_date, fmt="%d/%m/%Y")`.

#### ¿Qué hace `functools.lru_cache` (o `cache`)?

Memoriza los resultados de una función según sus argumentos (que deben ser hashables):

```python
from functools import cache

@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

#### ¿Qué es la recursividad y cuál es el límite de recursión de Python?

Una función que se llama a sí misma. CPython limita la profundidad (1000 por defecto, `sys.getrecursionlimit()`) y no optimiza la recursión de cola, así que la recursividad profunda suele reescribirse como un bucle.

#### ¿Qué son las docstrings?

Cadenas literales que son la primera instrucción de un módulo, clase o función, accesibles como `__doc__` y mostradas por `help()`.

#### ¿Qué es una función de orden superior?

Una función que recibe o devuelve otras funciones, como `sorted(key=...)`, los decoradores o `map`.

#### ¿Qué son las anotaciones de tipo (type hints)?

Anotaciones de los tipos esperados que Python no comprueba en ejecución, pero que sí comprueban las herramientas (mypy, pyright, los IDE):

```python
def total(prices: list[float], vat: float = 0.2) -> float:
    return sum(prices) * (1 + vat)
```

#### ¿Qué es `typing.Optional[X]`?

Una anotación que significa `X | None`. Desde Python 3.10 se puede escribir directamente `X | None`.

#### ¿Qué diferencia hay entre una función y un método?

Un método es una función definida en una clase y a la que se accede a través de una instancia o de la clase, lo que liga automáticamente el primer argumento (`self` o `cls`).

#### ¿Cómo se devuelven varios valores desde una función?

Devolviendo una tupla y desempaquetándola: `low, high = bounds(values)`. Si son más de unos pocos valores, devuelve una dataclass o una tupla con nombre.

#### ¿Qué hace el desempaquetado con `*` en las asignaciones?

Recoge los elementos restantes: `first, *middle, last = [1, 2, 3, 4]` da `middle == [2, 3]`.

#### ¿Qué son `any()` y `all()`?

`any(it)` es verdadero si al menos un elemento es verdadero, y `all(it)` si todos lo son (y es verdadero con un iterable vacío). Ambos cortocircuitan.

#### ¿Cómo evalúa Python `and` y `or`?

Con cortocircuito, y devolviendo uno de los operandos en lugar de un booleano: `x or default` devuelve `x` si es verdadero y `default` si no.

### Programación orientada a objetos

#### ¿Qué diferencia hay entre una clase y una instancia?

Una clase es un modelo que define atributos y métodos. Una instancia es un objeto creado a partir de ella con su propio estado: `p = Point(1, 2)`.

#### ¿Qué es `self`?

El primer parámetro de los métodos de instancia, ligado a la instancia sobre la que se llama el método. El nombre es una convención, no una palabra clave.

#### ¿Qué es `__init__` y en qué se diferencia de `__new__`?

`__new__` crea y devuelve la instancia (casi nunca se sobrescribe, salvo para tipos inmutables y singletons). `__init__` inicializa una instancia que ya existe.

#### ¿Qué diferencia hay entre atributos de clase y atributos de instancia?

Los atributos de clase los comparten todas las instancias. Los atributos de instancia pertenecen a un objeto. Asignar con `self.x = ...` crea un atributo de instancia que oculta al de la clase.

#### ¿Qué son `@staticmethod` y `@classmethod`?

Un método estático no recibe ningún primer argumento implícito y es una función normal en el espacio de nombres de la clase. Un método de clase recibe la clase (`cls`), lo que es útil para constructores alternativos:

```python
class Company:
    @classmethod
    def from_row(cls, row: dict) -> "Company":
        return cls(row["id"], row["name"])
```

#### ¿Qué es `@property`?

Un decorador que expone un método como atributo, con setter y deleter opcionales, para añadir validación o cálculo sin cambiar la interfaz.

#### ¿Qué es la herencia y qué hace `super()`?

Una clase puede extender otra y sobrescribir sus métodos. `super()` llama a la implementación del padre según el orden de resolución de métodos:

```python
class Lakehouse(Warehouse):
    def __init__(self, path):
        super().__init__()
        self.path = path
```

#### ¿Qué es el orden de resolución de métodos (MRO)?

El orden en que Python busca un atributo en las clases con herencia múltiple, calculado con la linealización C3. Se puede ver con `Class.__mro__`.

#### ¿Qué son los métodos dunder (mágicos)?

Métodos con doble guion bajo que se enganchan al comportamiento del lenguaje: `__repr__`, `__str__`, `__len__`, `__eq__`, `__hash__`, `__lt__`, `__iter__`, `__getitem__`, `__enter__`, `__call__`, `__add__`.

#### ¿Qué diferencia hay entre `__str__` y `__repr__`?

`__repr__` es una representación sin ambigüedad para desarrolladores (idealmente código válido para recrear el objeto). `__str__` es una representación legible para usuarios. `print()` usa `__str__` y, si no existe, `__repr__`.

#### ¿Qué es una dataclass?

Una clase decorada con `@dataclass`, que genera `__init__`, `__repr__` y `__eq__` a partir de los campos anotados, con opciones como `frozen=True`, `order=True` y `slots=True`:

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Snapshot:
    country: str
    rows: int
    files: list[str] = field(default_factory=list)
```

#### ¿Qué son las clases base abstractas?

Clases que derivan de `abc.ABC` con métodos marcados con `@abstractmethod`. No se pueden instanciar hasta que una subclase implemente todos los métodos abstractos, lo que impone una interfaz.

#### ¿Qué es el duck typing?

Usar un objeto según su comportamiento y no según su tipo: "si camina como un pato…". Cualquier objeto con un método `read()` puede usarse donde se espera un archivo.

#### ¿Qué es un Protocol?

`typing.Protocol` define interfaces estructurales para los comprobadores de tipos estáticos: cualquier clase con los métodos correspondientes lo cumple, sin heredar de él.

#### ¿Qué son los `__slots__`?

Un atributo de clase que lista los atributos de instancia permitidos. Elimina el `__dict__` de cada instancia, lo que reduce el uso de memoria y acelera el acceso a atributos cuando hay muchos objetos pequeños.

#### ¿Qué es la composición y por qué suele preferirse a la herencia?

Construir objetos a partir de otros objetos ("tiene un") en lugar de extender clases ("es un"). Da un acoplamiento más débil y evita jerarquías de clases profundas y frágiles.

#### ¿Qué es la encapsulación en Python?

Python no tiene miembros privados. Por convención, `_name` es interno, y `__name` activa el name mangling (`_Class__name`) para evitar colisiones en las subclases.

#### ¿Qué hace que un objeto sea hashable?

Un `__hash__` que no cambie durante su vida y un `__eq__` coherente con él (objetos iguales deben tener el mismo hash). Definir `__eq__` sin `__hash__` hace que una clase no sea hashable.

#### ¿Qué es una metaclase?

La clase de una clase (por defecto `type`), que controla cómo se crean las clases. Rara vez hace falta: los decoradores de clase y `__init_subclass__` cubren la mayoría de los casos.

#### ¿Qué es `__call__`?

Un método que hace que las instancias se puedan llamar como funciones, útil para objetos función configurables.

### Iteradores, generadores, decoradores y gestores de contexto

#### ¿Qué diferencia hay entre un iterable y un iterador?

Un iterable puede producir un iterador (`__iter__`): listas, diccionarios, archivos. Un iterador produce los elementos uno a uno mediante `__next__` y lanza `StopIteration` al final. Un iterador solo se puede recorrer una vez.

#### ¿Qué es un generador?

Una función que contiene `yield`. Al llamarla devuelve un iterador que ejecuta la función de forma perezosa, pausándose en cada `yield` y conservando su estado entre llamadas:

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

#### ¿Por qué son útiles los generadores en ingeniería de datos?

Procesan los datos como flujos, con memoria constante, sea cual sea el tamaño de la entrada: leer archivos enormes línea a línea, paginar API, encadenar transformaciones de forma perezosa.

#### ¿Qué hace `yield from`?

Delega en un subiterador y produce todos sus elementos: `yield from read_batches(path)`.

#### ¿Qué es `itertools` y qué funciones útiles tiene?

Un módulo de bloques rápidos para iteradores: `chain`, `islice`, `groupby`, `product`, `permutations`, `combinations`, `accumulate`, `count`, `cycle`, `tee`, `zip_longest` y `batched` (Python 3.12).

#### ¿Cómo funciona `itertools.groupby` y cuál es la trampa?

Agrupa elementos consecutivos con la misma clave, así que la entrada debe estar ordenada antes por esa clave:

```python
from itertools import groupby
for country, rows in groupby(sorted(data, key=key), key=key):
    print(country, sum(1 for _ in rows))
```

#### ¿Qué es un decorador?

Un invocable que recibe una función y devuelve una sustituta, aplicado con `@`. Añade comportamiento (registro, medición de tiempos, reintentos, caché, control de acceso) sin cambiar el código de la función.

#### ¿Cómo se escribe un decorador que conserve los metadatos de la función original?

Con `functools.wraps`:

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

#### ¿Cómo se escribe un decorador con argumentos?

Añadiendo una función exterior que recibe los argumentos y devuelve el decorador:

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

#### ¿Qué es un gestor de contexto?

Un objeto que se usa con `with` y que prepara y libera un recurso de forma fiable: `__enter__` se ejecuta al principio y `__exit__` al final, aunque se produzca una excepción. Los archivos, los bloqueos y las conexiones a bases de datos son gestores de contexto.

#### ¿Cómo se escribe un gestor de contexto con `contextlib`?

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

#### ¿Qué devuelve `__exit__`?

Un valor verdadero suprime la excepción lanzada en el bloque `with`, y uno falso la deja propagarse. Suprimir excepciones debería ser raro y deliberado.

#### ¿Qué es `contextlib.ExitStack`?

Un gestor de contexto que gestiona un número variable de otros gestores de contexto, por ejemplo para abrir una lista variable de archivos.

#### ¿Qué es la evaluación perezosa?

Calcular los valores solo cuando se necesitan. Los generadores, `range`, `map`, `zip` y las vistas de diccionarios son perezosos, lo que ahorra memoria y permite secuencias infinitas.

#### ¿Cómo se hace iterable una clase?

Implementando `__iter__`, normalmente como un método generador:

```python
class Batch:
    def __init__(self, rows):
        self.rows = rows
    def __iter__(self):
        yield from self.rows
```

#### ¿Qué pasa si se recorre dos veces un generador?

El segundo bucle no produce nada: el generador se ha agotado. Vuelve a crearlo, o guarda los resultados en una lista si los necesitas dos veces.

#### ¿Qué es una corrutina en Python?

Una función definida con `async def`, que puede pausarse en los puntos `await`. Se ejecuta en un bucle de eventos (asyncio) y permite la concurrencia en tareas limitadas por E/S.

#### ¿Cómo se leen solo los n primeros elementos de un iterador?

`itertools.islice(it, n)`, que funciona con cualquier iterador, incluidos los infinitos.

#### ¿Cómo se divide un iterable en lotes de tamaño fijo?

`itertools.batched(iterable, n)` en Python 3.12+, o con `islice` en un bucle en versiones anteriores.

#### ¿Qué diferencia hay entre `return` y `yield` en una función?

`return` termina la función y devuelve un valor. `yield` convierte la función en un generador que produce una serie de valores a lo largo del tiempo, reanudándose donde se quedó.

### Errores, archivos y biblioteca estándar

#### ¿Cómo funciona la gestión de excepciones en Python?

```python
try:
    value = int(raw)
except ValueError as exc:
    log.warning("bad value %r: %s", raw, exc)
    value = None
else:
    log.debug("parsed")         # se ejecuta si no hubo excepción
finally:
    cleanup()                   # se ejecuta siempre
```

#### ¿Por qué hay que evitar un `except:` sin tipo?

También captura `KeyboardInterrupt`, `SystemExit` y los errores de programación, y esconde los fallos. Captura las excepciones concretas que puedes gestionar, o como mucho `Exception`.

#### ¿Cómo se define una excepción propia?

Heredando de `Exception` (o de una integrada más concreta), normalmente con una clase base para todo el proyecto:

```python
class PipelineError(Exception):
    """Base class for pipeline failures."""

class SchemaDriftError(PipelineError):
    pass
```

#### ¿Qué es el encadenamiento de excepciones?

`raise NewError(...) from exc` conserva la excepción original como causa, de modo que la traza muestra las dos. `from None` oculta la original.

#### ¿Qué son los grupos de excepciones?

Python 3.11 añadió `ExceptionGroup` para lanzar varias excepciones a la vez (por ejemplo de tareas concurrentes) y `except*` para gestionarlas por tipo.

#### ¿Qué es EAFP frente a LBYL?

"Es más fácil pedir perdón que permiso" (intentar la operación y capturar el error) frente a "mira antes de saltar" (comprobar antes). EAFP es lo idiomático en Python y evita las condiciones de carrera entre la comprobación y la acción.

#### ¿Cómo se lee un archivo grande sin cargarlo en memoria?

Recorriendo el objeto archivo, que produce una línea cada vez:

```python
with open("big.csv", encoding="utf-8") as f:
    for line in f:
        process(line)
```

#### ¿Por qué hay que usar siempre `with` al abrir archivos?

Garantiza que el archivo se cierra aunque se produzca una excepción, liberando el descriptor y volcando las escrituras pendientes.

#### ¿Qué es `pathlib`?

Una API orientada a objetos para rutas de archivos: `Path("data") / "raw" / "file.csv"`, `.exists()`, `.glob("*.csv")`, `.read_text()`, `.suffix`, `.stem`, `.mkdir(parents=True, exist_ok=True)`.

#### ¿Cómo se leen y escriben archivos CSV con la biblioteca estándar?

```python
import csv

with open("in.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name"])
    writer.writeheader()
    writer.writerows(rows)
```

#### ¿Cómo se trabaja con JSON?

`json.loads`/`json.dumps` para cadenas y `json.load`/`json.dump` para archivos. Pasa `default=` para serializar tipos no admitidos como las fechas, y `ensure_ascii=False` para que los caracteres acentuados sigan siendo legibles.

#### ¿Cómo se analizan y formatean las fechas?

Con `datetime`:

```python
from datetime import datetime, timezone
d = datetime.strptime("15/10/2026", "%d/%m/%Y")
d.isoformat()                                  # '2026-10-15T00:00:00'
datetime.now(timezone.utc)                     # con zona horaria
```

`zoneinfo.ZoneInfo("Europe/Paris")` da las zonas horarias IANA.

#### ¿Qué diferencia hay entre datetimes ingenuos y conscientes?

Un datetime ingenuo no tiene zona horaria, uno consciente tiene `tzinfo`. Mezclarlos produce errores. Guarda y calcula en UTC con datetimes conscientes, y convierte solo para mostrar.

#### ¿Cómo se usa correctamente el módulo `logging`?

Crea un logger por módulo con `logging.getLogger(__name__)`, registra con formato perezoso (`log.info("loaded %d rows", n)`), configura los handlers y niveles una sola vez en el punto de entrada de la aplicación, y usa `log.exception()` dentro de los bloques `except` para incluir la traza.

#### ¿Para qué sirve `argparse`?

Para construir interfaces de línea de comandos con argumentos, opciones, tipos, valores por defecto y un `--help` automático.

#### ¿Qué ofrece el módulo `re`?

Expresiones regulares: `re.search`, `re.match`, `re.fullmatch`, `re.findall`, `re.sub`, `re.split`, patrones compilados y grupos con nombre:

```python
m = re.fullmatch(r"(?P<code>\d{2})\.(?P<sub>\d{2})", "03.11")
m["code"]   # '03'
```

#### ¿Cómo se ejecuta un comando externo desde Python?

Con `subprocess.run`, pasando una lista de argumentos (sin shell) y comprobando el resultado:

```python
result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
```

#### ¿Cómo se calcula el hash de datos o archivos en Python?

Con `hashlib`: `hashlib.sha256(data).hexdigest()`. Para archivos, lee por bloques y llama a `update()` para mantener la memoria constante.

#### ¿Para qué sirve `tempfile`?

Para crear archivos y directorios temporales que se limpian automáticamente: `with tempfile.TemporaryDirectory() as tmp: ...`.

#### ¿Cómo se comprimen o descomprimen archivos en Python?

Con los módulos `gzip`, `bz2`, `lzma` y `zipfile`. `gzip.open(path, "rt", encoding="utf-8")` lee un archivo de texto comprimido línea a línea.

### Concurrencia y rendimiento

#### ¿Qué es el GIL?

El Global Interpreter Lock de CPython permite que solo un hilo ejecute bytecode de Python a la vez. Los hilos siguen siendo útiles para el trabajo limitado por E/S, porque el GIL se libera durante las esperas, pero no para el código Python puro limitado por CPU. Python 3.13 introdujo una compilación opcional sin GIL (free-threaded).

#### ¿Qué diferencia hay entre threading, multiprocessing y asyncio?

- **threading:** varios hilos en un proceso. Bueno para tareas limitadas por E/S (red, disco), limitado por el GIL para trabajo de CPU.
- **multiprocessing:** varios procesos, cada uno con su intérprete. Bueno para trabajo limitado por CPU, con más sobrecosto y datos pasados mediante pickle.
- **asyncio:** concurrencia cooperativa en un solo hilo con un bucle de eventos, para muchísimas operaciones de E/S concurrentes.

#### ¿Qué es `concurrent.futures`?

Una interfaz de alto nivel con `ThreadPoolExecutor` y `ProcessPoolExecutor`:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=8) as pool:
    pages = list(pool.map(fetch, urls))
```

#### ¿Cómo funciona asyncio?

Un bucle de eventos ejecuta corrutinas. En cada `await` sobre una operación de E/S, la corrutina cede el control para que otras puedan ejecutarse. `asyncio.gather` lanza varias a la vez:

```python
import asyncio

async def main(urls):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(fetch(session, u) for u in urls))

asyncio.run(main(urls))
```

#### ¿Qué es una condición de carrera y cómo se evita con hilos?

Dos hilos que acceden a datos compartidos y producen un resultado que depende del orden de ejecución. Se evita con bloqueos (`threading.Lock`), colas seguras para hilos (`queue.Queue`) o evitando el estado mutable compartido.

#### ¿Cómo se limita la concurrencia al llamar a una API con límite de solicitudes?

Limitando el tamaño del pool de trabajadores, o con `asyncio.Semaphore`, y añadiendo reintentos con espera creciente ante las respuestas 429.

#### ¿Cómo se perfila código Python?

`cProfile` (`python -m cProfile -s cumtime script.py`) para el tiempo por función, `timeit` para fragmentos pequeños, `tracemalloc` para la memoria y perfiladores por muestreo como py-spy para procesos en marcha.

#### ¿Qué hace realmente más rápido el código Python?

Mejores algoritmos y estructuras de datos (conjuntos y diccionarios para búsquedas), funciones integradas y comprensiones en lugar de bucles manuales, bibliotecas vectorizadas (NumPy, pandas, Polars) para trabajo numérico masivo, evitar trabajo repetido (caché) y llevar el trabajo pesado a código compilado o a un motor distribuido.

#### ¿Por qué es lento recorrer un DataFrame de pandas fila a fila?

Cada fila se convierte en un objeto Python y el trabajo lo hace el intérprete. Las operaciones vectorizadas se ejecutan en código C optimizado sobre columnas enteras a la vez.

#### ¿Qué es un comportamiento parecido a una fuga de memoria en Python y cómo se encuentra?

Memoria que no deja de crecer porque se conservan referencias (cachés globales, listas que crecen, ciclos de referencias con `__del__`). Se investiga con `tracemalloc`, `gc` y `objgraph`.

#### ¿Cómo gestiona Python la memoria?

El recuento de referencias libera la mayoría de los objetos en cuanto su contador llega a cero, y un recolector de ciclos (`gc`) limpia los ciclos de referencias.

#### ¿Qué es `__pycache__`?

La carpeta donde Python guarda en caché el bytecode compilado (archivos `.pyc`) de los módulos importados, para acelerar las importaciones posteriores.

#### ¿Qué diferencia hay entre CPython y PyPy?

CPython es el intérprete de referencia, escrito en C. PyPy es una implementación alternativa con un compilador JIT que acelera el código Python puro de larga duración, pero es menos compatible con las extensiones en C.

#### ¿Cuándo usarías multiprocessing en lugar de Spark?

Para trabajo limitado por CPU que cabe en una máquina y en memoria. Usa Spark cuando los datos o el cálculo superan una máquina, o cuando la plataforma ya funciona con Spark.

#### ¿Qué es pickle y qué riesgos tiene?

Serializar objetos Python a bytes con `pickle`. No deserialices nunca datos no fiables: puede ejecutar código arbitrario. Usa JSON o Parquet para intercambiar datos.

#### ¿Por qué no se puede enviar una lambda a un pool de procesos?

`ProcessPoolExecutor` serializa la función con pickle para enviarla a los trabajadores, y las lambdas y las funciones anidadas no se pueden serializar por referencia. Usa funciones de nivel de módulo.

#### ¿Qué es un hilo demonio (daemon)?

Un hilo en segundo plano que no impide que el programa termine. Se mata bruscamente al salir, así que no debe tener recursos que haya que limpiar.

#### ¿Cómo se fija un timeout en una llamada de red bloqueante?

Pasando un timeout a la biblioteca (`requests.get(url, timeout=30)`). No llames nunca a servicios externos sin él: una conexión colgada bloquearía para siempre.

#### ¿En qué se diferencia `asyncio.run` de llamar directamente a una corrutina?

Llamar a una función `async def` solo crea un objeto corrutina. `asyncio.run(coro)` crea un bucle de eventos, ejecuta la corrutina hasta terminar y cierra el bucle.

#### ¿Qué es la contrapresión (backpressure) y cómo se gestiona en pipelines de Python?

Cuando los productores son más rápidos que los consumidores, la memoria crece hasta que algo se rompe. Usa colas acotadas (`queue.Queue(maxsize=...)`, `asyncio.Queue(maxsize=...)`) para que los productores esperen.

### Tipado, empaquetado, entornos y tests

#### ¿Qué es un entorno virtual y por qué usarlo?

Una instalación de Python aislada con sus propios paquetes (`python -m venv .venv`), para que cada proyecto tenga sus versiones de dependencias y no rompa el Python del sistema ni otros proyectos.

#### ¿Qué es `pyproject.toml`?

El archivo de configuración estándar de los proyectos Python: sistema de construcción, metadatos, dependencias, puntos de entrada y configuración de herramientas (pytest, ruff, mypy).

#### ¿Cómo se hace reproducible la instalación de dependencias?

Fijando versiones exactas en un archivo de bloqueo (`uv lock`, `pip-tools`, Poetry), instalando a partir de él en CI y producción, y actualizando las dependencias de forma deliberada.

#### ¿Qué es `uv`?

Un gestor de paquetes y proyectos Python muy rápido, escrito en Rust, que sustituye los flujos de pip, pip-tools y virtualenv (`uv add`, `uv sync`, `uv run`) y puede instalar versiones de Python.

#### ¿Qué es un wheel?

Un formato de distribución compilado (`.whl`) que se instala sin paso de construcción. Los trabajos de Databricks, por ejemplo, ejecutan código empaquetado como wheels.

#### ¿Qué es un punto de entrada (entry point)?

Un script de consola declarado en `pyproject.toml` que instala un comando que llama a una función de Python:

```toml
[project.scripts]
registry-lakehouse = "registry_lakehouse.cli:main"
```

#### ¿Qué es pytest y por qué se prefiere a unittest?

Un framework de tests en el que los tests son funciones normales con `assert` normales, con mensajes de fallo detallados, fixtures, parametrización y un gran ecosistema de plugins.

#### ¿Qué son las fixtures de pytest?

Funciones que proporcionan las dependencias de los tests (datos, conexiones, una sesión de Spark), inyectadas por nombre de argumento, con ámbitos (función, módulo, sesión) y limpieza después del `yield`:

```python
@pytest.fixture(scope="session")
def spark():
    session = SparkSession.builder.master("local[2]").getOrCreate()
    yield session
    session.stop()
```

#### ¿Qué es la parametrización en pytest?

Ejecutar un mismo test con varias entradas:

```python
@pytest.mark.parametrize("raw, expected", [("311.0", "03.11"), ("4782", "47.82")])
def test_nace(raw, expected):
    assert nace_from_numeric(raw) == expected
```

#### ¿Qué es el mocking y cómo se hace?

Sustituir una dependencia por un objeto falso en un test, para aislar el código y evitar llamadas a la red o a la base de datos: `unittest.mock.patch`, `MagicMock` o el `monkeypatch` de pytest.

#### ¿Qué son los tests basados en propiedades?

Generar muchas entradas aleatorias para comprobar que una propiedad se cumple siempre, en lugar de escribir ejemplos a mano. Hypothesis es la biblioteca de Python para ello, y reduce los fallos a un ejemplo mínimo.

#### ¿Qué es la cobertura de tests y es un buen objetivo llegar al 100 %?

La proporción de código ejecutada por los tests (`pytest-cov`). Muestra las zonas sin probar, pero una cobertura alta no demuestra que los tests comprueben lo correcto. Apunta a tests significativos de la lógica arriesgada.

#### ¿Qué diferencia hay entre tests unitarios, de integración y de extremo a extremo?

Los tests unitarios comprueban una función o clase de forma aislada. Los de integración comprueban componentes trabajando juntos (código y una base de datos). Los de extremo a extremo ejecutan todo el sistema con entradas realistas.

#### ¿Qué herramientas mantienen alta la calidad del código Python?

Un formateador y un linter (ruff, o black y flake8), un comprobador de tipos (mypy, pyright), hooks de pre-commit, tests en CI y revisión de código.

#### ¿Cómo se comprueban los tipos con mypy?

Añadiendo anotaciones de tipo y ejecutando `mypy src/`. Informa de las incoherencias de tipos de forma estática, antes de la ejecución. Se adopta poco a poco con configuración por módulo.

#### ¿Qué es `TypedDict`?

Una construcción de tipado que describe diccionarios con un conjunto fijo de claves y tipos de valor, útil para registros con forma de JSON.

#### ¿Qué son los genéricos en las anotaciones de tipo?

Tipos parametrizados como `list[int]` o `dict[str, float]`, y tus propias clases y funciones genéricas. Python 3.12 tiene una sintaxis compacta: `def first[T](xs: list[T]) -> T: ...`.

#### ¿Cómo se gestionan la configuración y los secretos en una aplicación Python?

Leyéndolos de variables de entorno o de un gestor de secretos al arrancar, validándolos (por ejemplo con pydantic-settings), dejando los archivos `.env` fuera del control de versiones y sin escribir nunca credenciales en el código.

#### ¿Qué es pydantic?

Una biblioteca de validación de datos que convierte los datos en modelos tipados y lanza errores claros ante entradas no válidas. Se usa para cargas útiles de API, configuración y contratos.

#### ¿Cómo se estructura un proyecto Python para un pipeline de datos?

Con una organización `src/` y un paquete dividido por responsabilidades (ingesta, transformaciones, calidad, E/S), un punto de entrada CLI fino, la configuración separada del código, los tests reflejando el paquete y `pyproject.toml` para las dependencias y las herramientas.

### Python para ingeniería de datos

#### ¿Cómo se lee un CSV grande con pandas sin quedarse sin memoria?

Leyendo por bloques, seleccionando solo las columnas necesarias, fijando tipos compactos, o usando un formato en columnas y un motor perezoso:

```python
for chunk in pd.read_csv("big.csv", usecols=["id", "amount"], dtype={"id": "int64"}, chunksize=500_000):
    process(chunk)
```

#### ¿Qué diferencia hay entre `loc` e `iloc` en pandas?

`loc` selecciona por etiquetas (valores del índice y nombres de columna, con el final incluido). `iloc` selecciona por posición entera (con el final excluido).

#### ¿Cómo se evita el `SettingWithCopyWarning` en pandas?

Usando `.loc[row_selector, column] = value` sobre el DataFrame original, o haciendo un `.copy()` explícito cuando quieres trabajar con un subconjunto. Con copy-on-write (por defecto en pandas 3), la asignación encadenada simplemente no modifica el original.

#### ¿Cómo se agrupa y agrega en pandas?

```python
summary = (df.groupby(["country", "industry"], as_index=False)
             .agg(companies=("id", "count"), employees=("employees", "sum")))
```

#### ¿Qué tipos de join tiene `pandas.merge`?

`how="inner"`, `"left"`, `"right"`, `"outer"` y `"cross"`, sobre columnas `on=` o `left_on`/`right_on`. `validate="one_to_one"` o `"many_to_one"` detecta claves duplicadas inesperadas, e `indicator=True` muestra el origen de cada fila.

#### ¿Cómo se tratan los valores ausentes en pandas?

Se detectan con `isna()`, se eliminan con `dropna()`, se rellenan con `fillna()` o `ffill()`, y se usan tipos que admiten nulos (`Int64`, `string`, `boolean`) para que los enteros con valores ausentes no se conviertan en float.

#### ¿Qué es Apache Parquet y por qué se prefiere a CSV?

Un formato de archivo en columnas, comprimido y tipado. Las consultas leen solo las columnas que necesitan, los archivos son mucho más pequeños, los tipos se conservan y las estadísticas permiten saltarse datos. CSV es texto por filas sin tipos.

#### ¿Qué es Apache Arrow?

Un formato estándar en memoria orientado a columnas. Permite que pandas, Polars, DuckDB, Spark y otros intercambien datos sin copiarlos ni convertirlos. PyArrow es su biblioteca de Python.

#### ¿Qué es Polars y cuándo usarlo en lugar de pandas?

Una biblioteca de DataFrames escrita en Rust, multihilo, con un optimizador de consultas perezoso. Suele ser mucho más rápida y eficiente en memoria que pandas para cargas grandes en una sola máquina.

#### ¿Qué es DuckDB?

Una base de datos analítica SQL embebida. Consulta Parquet, CSV y DataFrames directamente y muy rápido, sin servidor: `duckdb.sql("select country, count(*) from 'data/*.parquet' group by 1")`.

#### ¿Cómo se llama a una API REST de forma robusta desde Python?

Usando una sesión, fijando timeouts, reintentando los errores transitorios con espera exponencial, gestionando la paginación, respetando los límites de solicitudes y validando las respuestas:

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

#### ¿Cómo se descarga un archivo grande sin cargarlo en memoria?

En streaming, por bloques:

```python
with requests.get(url, stream=True, timeout=60) as r:
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
```

#### ¿Cómo se conecta uno a una base de datos desde Python de forma segura?

Con un driver (psycopg para PostgreSQL) o SQLAlchemy, usando consultas parametrizadas y nunca formateo de cadenas, para evitar la inyección SQL:

```python
cur.execute("select * from companies where country = %s", (country,))
```

#### ¿Cómo se cargan muchas filas en PostgreSQL rápidamente desde Python?

Con `COPY` (el `cursor.copy()` de psycopg) en lugar de inserciones fila a fila, o con inserciones por lotes mediante `executemany` y tamaños de página. Haz la carga en una sola transacción.

#### ¿Qué es SQLAlchemy?

Un conjunto de herramientas para bases de datos con una capa Core (lenguaje de expresiones SQL, pool de conexiones, engines) y un ORM. pandas usa engines de SQLAlchemy para `read_sql` y `to_sql`.

#### ¿Cómo se leen archivos de Amazon S3 en Python?

Con boto3 (`s3.get_object`, `download_file`, paginadores para listar), o mediante fsspec y s3fs para que pandas, Polars y PyArrow lean rutas `s3://` directamente. Las credenciales deben venir de roles o del entorno, nunca del código.

#### ¿Cómo se hace idempotente un paso de un pipeline de datos?

Ejecutarlo dos veces con la misma entrada debe dar el mismo resultado: escribe en una ubicación determinista y sobrescríbela (o fusiona por claves) en lugar de añadir, usa identificadores de ejecución y comprueba si el trabajo ya estaba hecho.

#### ¿Cómo validarías un conjunto de datos en Python antes de cargarlo?

Comprobando el esquema (columnas y tipos), los nulos en los campos obligatorios, los rangos de valores, la unicidad de las claves y el número de filas frente a lo esperado, con código, pydantic o una biblioteca como pandera o Great Expectations. Falla de forma visible o pon en cuarentena las filas erróneas.

#### ¿Qué es PySpark y qué relación tiene con Python?

La API de Python de Apache Spark. El código Python construye un plan de consulta que se ejecuta en la JVM a través de un clúster, así que las operaciones con DataFrames se distribuyen y se optimizan. Las UDF de Python se ejecutan en trabajadores Python y son mucho más lentas que las funciones integradas.

#### ¿Por qué son lentas las UDF de Python en PySpark y qué alternativas hay?

Cada fila se serializa entre la JVM y Python. Prefiere las funciones integradas de `pyspark.sql.functions`, y después las pandas UDF (vectorizadas con Arrow) si el código Python a medida es inevitable.

#### ¿Cómo se resuelven los problemas de codificación al leer archivos?

Indicando explícitamente la `encoding` correcta, usando `errors="replace"` solo a sabiendas, detectando un BOM con `encoding="utf-8-sig"` y reparando el mojibake (`'TravesÃ­a'.encode('latin-1').decode('utf-8')`) con una protección para las cadenas en las que la conversión falla.

#### ¿Cómo se programan y orquestan los pipelines de Python?

Con un orquestador como Airflow, Dagster o Prefect (dependencias, reintentos, alertas, backfills), o con un planificador en la nube que lanza funciones serverless o contenedores en los casos sencillos.

#### ¿Cómo se procesa un archivo JSON demasiado grande para cargarlo de una vez?

Mejor en JSON delimitado por saltos de línea, leído línea a línea. Para un único array JSON enorme, usa un analizador en streaming como ijson para recorrer los elementos sin cargarlo todo.

#### ¿Qué diferencia hay entre ETL y ELT desde el punto de vista de un desarrollador Python?

En ETL, el código Python transforma los datos antes de cargarlos. En ELT, Python sobre todo extrae y carga datos en bruto, y las transformaciones se ejecutan como SQL en el almacén (a menudo con dbt). Python se queda con lo que SQL hace mal: API, archivos, análisis complejos.

#### ¿Cómo se escribe un archivo Parquet particionado por una columna?

```python
import pyarrow as pa, pyarrow.parquet as pq
pq.write_to_dataset(pa.Table.from_pandas(df), root_path="out/", partition_cols=["country"])
```

Esto crea carpetas como `out/country=FR/`, que los motores de consulta pueden podar.

### Problemas de programación

#### Analiza un archivo de registro e informa de cuánto tiempo estuvo encendido un dispositivo y cuándo hubo errores.

Cada línea tiene la forma `Jul 11 16:11:51:490 [139681125603136] dut: Device State: ON`. Solo importan los mensajes `ON`, `ERR` y `OFF`. El informe debe decir cuánto tiempo estuvo encendido el dispositivo y listar las marcas de tiempo de los errores.

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

La marca de tiempo son los tres primeros campos de la línea (mes, día, hora), no solo el tercer campo. Analizarla con `strptime` (`%f` acepta los milisegundos) da un datetime, y restar dos datetimes da un `timedelta`. Fíjate también en `errors.append()` (las listas no tienen `add`), en recorrer directamente el objeto archivo y en comprobar el estado al final de la línea para que `ON` no coincida dentro de otra palabra.

#### Invierte una cadena y comprueba si es un palíndromo sin tener en cuenta mayúsculas ni signos de puntuación.

```python
def is_palindrome(text: str) -> bool:
    letters = [c.lower() for c in text if c.isalnum()]
    return letters == letters[::-1]
```

#### Encuentra los dos números de una lista que suman un objetivo (two-sum).

Usa un diccionario de los valores ya vistos para conseguir O(n):

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i
    return None
```

#### Cuenta la frecuencia de las palabras de un texto y devuelve las diez primeras.

```python
import re
from collections import Counter

def top_words(text: str, n: int = 10) -> list[tuple[str, int]]:
    return Counter(re.findall(r"\w+", text.lower())).most_common(n)
```

#### Aplana una lista anidada de forma arbitraria.

```python
def flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

list(flatten([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]
```

#### Agrupa una lista de anagramas.

```python
from collections import defaultdict

def group_anagrams(words: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())
```

#### Deduplica registros conservando la versión más reciente de cada clave.

```python
def latest_by_key(rows: list[dict], key: str, ts: str) -> list[dict]:
    latest = {}
    for row in rows:
        current = latest.get(row[key])
        if current is None or row[ts] > current[ts]:
            latest[row[key]] = row
    return list(latest.values())
```

#### Fusiona intervalos solapados.

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

#### Comprueba si una cadena de paréntesis está equilibrada.

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

#### Escribe una función que divida una lista en trozos de tamaño n.

```python
def chunks(items: list, n: int) -> list[list]:
    return [items[i:i + n] for i in range(0, len(items), n)]
```

#### Encuentra el primer carácter que no se repite de una cadena.

```python
from collections import Counter

def first_unique(s: str) -> str | None:
    counts = Counter(s)
    return next((c for c in s if counts[c] == 1), None)
```

#### Valida un número SIREN francés con el algoritmo de Luhn.

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

#### Calcula un total acumulado y un promedio móvil de 3 elementos.

```python
from itertools import accumulate

values = [3, 5, 2, 8, 6]
running = list(accumulate(values))                                         # [3, 8, 10, 18, 24]
moving = [sum(values[i - 2:i + 1]) / 3 for i in range(2, len(values))]     # [3.33, 5.0, 5.33]
```

#### Lee un CSV de transacciones y calcula el importe total por usuario y las ciudades cuya media supera 8.000.

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

#### Escribe un generador que produzca números de Fibonacci indefinidamente y toma los diez primeros.

```python
from itertools import islice

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

list(islice(fibonacci(), 10))   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```
