## Guía de estudio de Python

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Python: unas 200 preguntas](../../images/python_study_guide_title_img.png)

Unas 200 preguntas de Python para entrevistas de ingeniería de datos: el lenguaje, la biblioteca estándar, la programación orientada a objetos, los generadores y decoradores, la concurrencia, los tests y el empaquetado, Python para trabajar con datos, y una serie de problemas de programación con sus soluciones. Los ejemplos usan Python 3.12.

La guía sigue una ruta de aprendizaje en cuatro etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos del lenguaje y tipos de datos

<!-- unit: El modelo de objetos de Python -->

<!-- goals -->

- Explicar el tipado dinámico y fuerte y que "todo es un objeto".
- Distinguir objetos mutables e inmutables, identidad e igualdad, y cómo se pasan los argumentos.

<!-- concept -->

Los nombres en Python son etiquetas pegadas a objetos, no cajas que guardan valores. Un nombre puede apuntar a un objeto de cualquier tipo (tipado dinámico), pero los objetos nunca cambian de tipo en silencio (tipado fuerte). Cada objeto tiene identidad, tipo y valor.
La mutabilidad decide qué pasa cuando dos nombres comparten un objeto. Cambiar un objeto mutable por un nombre se ve por el otro; los inmutables solo se pueden reemplazar. Los argumentos de funciones siguen la misma regla: el parámetro es otra etiqueta sobre el objeto de quien llama.

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

<!-- challenge -->

Una función recibe un dict de ajustes, pone `settings["debug"] = True` para su propio uso, y otras partes del programa empiezan a registrar en modo debug. ¿Por qué y cómo lo arreglas?

<!-- solution -->

La función mutó el dict de quien la llamó, compartido por todos. Cópialo antes de cambiarlo (`local = {**settings, "debug": True}`) o pasa la bandera como argumento aparte.

<!-- takeaways -->

- Los nombres son etiquetas sobre objetos.
- Mutar objetos compartidos afecta a todos los nombres.
- Usa `==` para valores e `is` para identidad (y `None`).

<!-- unit: Números y veracidad -->

<!-- goals -->

- Conocer los tipos incorporados de Python y qué cuenta como falsy.
- Manejar bien la división, la precisión de floats y los enteros grandes.

<!-- concept -->

Los tipos incorporados de Python cubren casi todo sin imports: números, texto, secuencias, mapeos y conjuntos. Cada objeto tiene además un valor de verdad, lo que hace concisas las condiciones pero puede esconder bugs, porque el cero y las colecciones vacías son falsos igual que `None`.
Los números tienen sus trampas. La división verdadera siempre da float; la división entera redondea hacia abajo, aun con negativos. Los floats son aproximaciones binarias, así que el dinero necesita `Decimal`, mientras que los enteros crecen tanto como lo permita la memoria.

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

<!-- challenge -->

`if not discount:` trata un descuento de 0 igual que un descuento faltante, y las órdenes sin descuento reciben el 10 % por defecto. Arregla la condición.

<!-- solution -->

Prueba explícitamente el faltante: `if discount is None: discount = 0.10`, así un valor real de 0 sigue siendo 0.

<!-- takeaways -->

- Cero, vacío y `None` son falsy.
- `//` redondea hacia abajo; `/` devuelve floats.
- Usa `Decimal` para aritmética decimal exacta.

<!-- unit: Sintaxis moderna -->

<!-- goals -->

- Usar el operador walrus y el pattern matching estructural.
- Elegir entre listas y tuplas y hacer copias superficiales o profundas.

<!-- concept -->

Las versiones recientes de Python agregaron sintaxis que elimina boilerplate común. El operador walrus asigna dentro de una expresión, lo que ordena los ciclos de leer y probar. El pattern matching revisa la estructura y extrae valores a la vez, útil para mensajes con formas distintas.
Dos decisiones más viejas siguen importando a diario: listas para colecciones que cambian, tuplas para registros fijos, y copias que duplican solo el contenedor exterior frente a toda la estructura anidada.

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

<!-- challenge -->

Una prueba copia una config anidada con `dict(config)` y modifica una lista anidada, y luego fallan otras pruebas. ¿Qué pasó?

<!-- solution -->

`dict(config)` es una copia superficial: la lista anidada se comparte, así que el cambio se filtró al original. Usa `copy.deepcopy(config)` para estructuras anidadas.

<!-- takeaways -->

- `:=` asigna dentro de expresiones.
- `match` revisa la estructura y extrae valores.
- Las copias superficiales comparten los objetos anidados.

<!-- unit: Nombres, módulos y scripts -->

<!-- goals -->

- Explicar la regla LEGB, global y nonlocal.
- Distinguir módulos y paquetes y usar el guard de `__main__`.

<!-- concept -->

Cuando Python ve un nombre, lo busca en cuatro lugares en orden: la función local, las funciones que la envuelven, el módulo y los built-ins. Asignar un nombre dentro de una función lo vuelve local salvo que se declare otra cosa, y de ahí sale el clásico error "referenced before assignment".
El código se organiza en módulos (archivos) y paquetes (directorios de módulos). El guard de `__main__` permite que un archivo funcione como módulo importable y como script, sin correr el código de script al importarlo.

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

#### ¿Qué es la regla LEGB?

El orden en que Python resuelve los nombres: Local, ámbitos de las funciones contenedoras (Enclosing), Global (módulo) y Built-in (integrados).

#### ¿Qué hacen `global` y `nonlocal`?

`global x` hace que las asignaciones dentro de una función reasignen la `x` del módulo. `nonlocal x` reasigna la `x` del ámbito de la función contenedora más cercana, algo necesario para modificar una variable de un closure.

#### ¿Qué diferencia hay entre un módulo y un paquete?

Un módulo es un único archivo `.py`. Un paquete es un directorio de módulos, normalmente con un `__init__.py`, que se importa con nombres con puntos.

#### ¿Qué hace `if __name__ == "__main__":`?

Su bloque solo se ejecuta cuando el archivo se lanza como script, no cuando se importa como módulo. Se usa para los puntos de entrada de línea de comandos.

<!-- challenge -->

Importar un módulo auxiliar en una prueba arranca una carga de datos de 10 minutos. ¿Por qué y cómo lo arreglas?

<!-- solution -->

El módulo corre su carga a nivel superior, lo que se ejecuta al importar. Pásala a una función `main()` llamada bajo `if __name__ == "__main__":`.

<!-- takeaways -->

- Los nombres se resuelven Local, Enclosing, Global, Built-in.
- Asignar vuelve local un nombre salvo que se declare.
- Protege el código de script con `__main__`.

### Cadenas, colecciones y comprensiones

<!-- unit: Strings y bytes -->

<!-- goals -->

- Formatear, rebanar y construir strings con eficiencia.
- Distinguir texto de bytes y resolver problemas clásicos de strings.

<!-- concept -->

Los strings son secuencias inmutables de caracteres Unicode. La inmutabilidad los hace seguros para compartir y usar como claves de dict, pero cada cambio crea un string nuevo, así que construir texto largo concatenando una y otra vez es lento y el idioma es unir una lista.
El texto se vuelve bytes cuando sale del programa, por archivos o redes, así que la codificación es explícita. Los slices, con su fin excluido e índices negativos, resuelven muchos problemas de entrevista en una línea.

<!-- example -->

```python
name, total = "Ana", 1234.5
print(f"{name:<6}|{total:>10,.2f}|")     # Ana   |  1,234.50|
parts = [f"{i}" for i in range(5)]
print(",".join(parts))                   # efficient building
data = "café".encode("utf-8")            # b'caf\xc3\xa9'
print("racecar"[::-1])                   # reverse with a slice
```

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

<!-- challenge -->

Un ciclo construye un reporte de 50 MB con `report += line` y tarda minutos. ¿Qué cambias?

<!-- solution -->

Junta las líneas en una lista y haz `"".join(lines)` una vez al final (o escribe las líneas directamente a un archivo). Cada `+=` copia todo el string que va creciendo.

<!-- takeaways -->

- Los strings son inmutables; une en vez de concatenar.
- Codifica el texto a bytes explícitamente.
- Slices: `[start:stop:step]`, sin incluir stop.

<!-- unit: Comprehensions y ayudas de iteración -->

<!-- goals -->

- Escribir comprehensions de listas, dicts y sets.
- Elegir expresiones generadoras y usar zip y enumerate.

<!-- concept -->

Las comprehensions construyen colecciones a partir de iterables en una expresión legible, con filtro opcional. Vienen en forma de lista, dict y set. Cambiar los corchetes por paréntesis da una expresión generadora, que produce elementos de forma perezosa en lugar de construirlo todo en memoria, ideal cuando solo recorres una vez.
Dos ayudas encajan con ellas: `enumerate` da posiciones sin contadores manuales y `zip` recorre varias secuencias juntas.

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

#### ¿Qué diferencia hay entre una comprensión de listas y una expresión generadora?

Una comprensión de listas construye toda la lista en memoria. Una expresión generadora (entre paréntesis) produce los elementos de forma perezosa, uno a uno: `sum(x * x for x in range(10**8))` usa memoria constante.

#### ¿Cómo está implementado un dict de Python y cuál es su complejidad?

Como una tabla hash: la búsqueda, la inserción y el borrado son O(1) de media. Desde Python 3.7, los diccionarios conservan el orden de inserción.

#### ¿Cuál es la complejidad temporal de las operaciones habituales de las listas?

El acceso por índice y `append` son O(1) (amortizado en el caso de append), `insert(0, x)` y `pop(0)` son O(n), `x in list` es O(n) y ordenar es O(n log n). Usa `collections.deque` para operaciones rápidas en los dos extremos y conjuntos para comprobar pertenencia.

#### ¿Qué hace `dict.get()` y en qué se diferencia de `dict[key]`?

`d[key]` lanza `KeyError` si la clave no existe. `d.get(key, default)` devuelve `default` (o `None`) en ese caso.

<!-- challenge -->

`sum([row["amount"] for row in read_rows(path)])` se queda sin memoria con un archivo de 40 GB. ¿Cuál es el arreglo de un carácter y por qué?

<!-- solution -->

Quita los corchetes: `sum(row["amount"] for row in read_rows(path))`. La expresión generadora entrega un valor a la vez en lugar de construir una lista completa.

<!-- takeaways -->

- Las comprehensions construyen colecciones de forma concisa.
- Las expresiones generadoras son perezosas y livianas en memoria.
- `enumerate` y `zip` reemplazan el manejo manual de índices.

<!-- unit: Dicts y listas -->

<!-- goals -->

- Explicar las características de rendimiento de dicts y listas.
- Usar get, combinación de dicts, operaciones de conjuntos y deduplicación que conserva el orden.

<!-- concept -->

Elegir el contenedor correcto es la mayor decisión de rendimiento en el Python de todos los días. Dicts y sets son tablas hash, así que la pertenencia y la búsqueda toman tiempo constante; las listas son arrays, rápidas al final pero lentas para buscar o cambiar al inicio. Muchos ciclos lentos se vuelven rápidos al reemplazar una búsqueda en lista por un set o un dict.
Los dicts además conservan el orden de inserción, lo que simplifica la deduplicación que conserva el orden y los problemas de "último por clave".

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

<!-- challenge -->

Un job revisa `if customer_id in processed_ids` donde `processed_ids` es una lista de 2 millones de IDs, y tarda horas. ¿Qué cambias?

<!-- solution -->

Vuelve `processed_ids` un set: la pertenencia pasa a O(1) en lugar de recorrer la lista, y las horas se vuelven segundos.

<!-- takeaways -->

- Dicts y sets dan búsquedas O(1).
- Las listas son lentas para buscar y para cambiar al inicio.
- Los dicts conservan el orden de inserción.

<!-- unit: El módulo collections -->

<!-- goals -->

- Usar defaultdict, Counter, namedtuple y deque.
- Resolver con ellos problemas de conteo, agrupación y pilas.

<!-- concept -->

El módulo `collections` empaqueta patrones que de otro modo escribirías a mano. `defaultdict` crea automáticamente los valores faltantes, perfecto para agrupar. `Counter` cuenta y ordena. `namedtuple` da a las tuplas nombres de campo legibles. `deque` agrega y quita en ambos extremos en tiempo constante, así que sirve de cola, pila o ventana deslizante.
Muchos problemas de entrevista son uno de estos patrones disfrazado.

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

#### ¿Cómo se eliminan los duplicados de una lista conservando el orden?

```python
unique = list(dict.fromkeys(items))
```

#### ¿Cuáles son las operaciones de conjuntos?

Unión `a | b`, intersección `a & b`, diferencia `a - b`, diferencia simétrica `a ^ b` y la comprobación de subconjunto `a <= b`. Comprobar la pertenencia es O(1) de media.

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

<!-- challenge -->

Una función guarda las últimas 1.000 líneas de log con `lines.append(x)` seguido de `lines.pop(0)`, y se vuelve lenta a medida que crece el tráfico. ¿Qué usas?

<!-- solution -->

Un `deque(maxlen=1000)`: al agregar se descarta automáticamente el elemento más viejo en O(1), mientras que `list.pop(0)` corre todos los elementos.

<!-- takeaways -->

- `defaultdict` agrupa; `Counter` cuenta.
- `deque` es O(1) en ambos extremos.
- Muchos problemas son estos patrones disfrazados.

<!-- unit: Ordenamiento -->

<!-- goals -->

- Ordenar listas y registros por una o varias claves.
- Elegir entre sort y sorted y aplicar el ordenamiento a problemas de intervalos.

<!-- concept -->

Python ordena con una función de clave: le dices qué comparar y se encarga del resto, de forma estable y eficiente. Las tuplas como clave ordenan por varios campos a la vez; negar un número invierte un campo. `sort()` cambia una lista en sitio y devuelve `None`, un bug frecuente cuando se asigna; `sorted()` devuelve una lista nueva desde cualquier iterable.
Ordenar también es un paso para resolver problemas: una vez ordenados los intervalos por inicio, los solapamientos quedan como vecinos.

<!-- example -->

```python
from operator import itemgetter
rows = [{"country": "CO", "revenue": 50}, {"country": "AR", "revenue": 80}, {"country": "CO", "revenue": 90}]
rows.sort(key=lambda r: (r["country"], -r["revenue"]))     # country asc, revenue desc
top = sorted(rows, key=itemgetter("revenue"), reverse=True)[:2]
```

#### ¿Qué son las funciones de primera clase?

Las funciones son objetos: se pueden asignar a variables, guardar en estructuras de datos, pasar como argumentos y devolver desde otras funciones.

#### ¿Qué son `map`, `filter` y `functools.reduce`?

`map(f, xs)` aplica `f` a cada elemento, `filter(pred, xs)` conserva los elementos para los que `pred` es verdadero (ambos perezosos), y `reduce(f, xs, init)` reduce una secuencia a un solo valor. Las comprensiones suelen ser más legibles que `map` y `filter`.

#### ¿Qué hace `functools.partial`?

Crea una función nueva con algunos argumentos fijados: `parse_fr = partial(parse_date, fmt="%d/%m/%Y")`.

<!-- challenge -->

`result = rows.sort(key=...)` y luego `result[0]` falla con `TypeError: 'NoneType' object is not subscriptable`. ¿Por qué?

<!-- solution -->

`list.sort()` ordena en sitio y devuelve `None`. O llamas `rows.sort(...)` y usas `rows`, o haces `result = sorted(rows, key=...)`.

<!-- takeaways -->

- Ordena con funciones de clave; tuplas para varios campos.
- `sort()` devuelve None; `sorted()` devuelve una lista.
- Ordenar convierte los problemas de solapamiento en revisiones de vecinos.

<!-- stage: Escribir Python -->

### Funciones, ámbitos y closures

<!-- unit: Parámetros y argumentos -->

<!-- goals -->

- Usar *args, **kwargs y parámetros keyword-only y positional-only.
- Evitar defaults mutables y devolver o desempacar varios valores.

<!-- concept -->

Las firmas de funciones son una interfaz, y Python da un control fino sobre ella: recoger argumentos extra, obligar a nombrar algunos por legibilidad u obligar a que otros sean posicionales para poder renombrarlos después. El desempaquetado devuelve varios valores de forma natural.
Una trampa le pasa a todo el mundo una vez: los valores por defecto se crean al definir la función, no al llamarla, así que un default mutable lo comparten todas las llamadas.

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

<!-- challenge -->

`def add_item(item, basket=[])` devuelve canastas que contienen ítems de llamadas anteriores. Arréglalo.

<!-- solution -->

Usa `basket=None` y crea la lista adentro: `if basket is None: basket = []`. La lista por defecto se creó una vez y se compartía entre llamadas.

<!-- takeaways -->

- `*args` y `**kwargs` recogen argumentos extra.
- `*` obliga a usar keywords; `/` obliga a posiciones.
- Usa `None` en lugar de defaults mutables.

<!-- unit: Funciones como valores -->

<!-- goals -->

- Usar lambdas, funciones de orden superior, map, filter, reduce y partial.
- Entender any, all y la evaluación en cortocircuito.

<!-- concept -->

Las funciones son objetos, así que se pueden pasar, devolver y guardar como cualquier valor. Eso hace posibles el ordenamiento por clave, los callbacks y los decoradores. Las funciones pequeñas y desechables pueden ser lambdas; la aplicación parcial fija algunos argumentos para construir versiones especializadas.
Los operadores lógicos comparten esa flexibilidad: `and` y `or` devuelven uno de sus operandos en lugar de un booleano, y `any`/`all` paran en cuanto conocen la respuesta.

<!-- example -->

```python
from functools import partial, reduce
from datetime import datetime
parse_fr = partial(datetime.strptime, format="%d/%m/%Y")   # wraps keyword use
total = reduce(lambda acc, x: acc + x, [1, 2, 3], 0)
has_errors = any(r["status"] == "error" for r in results)  # stops at the first error
name = user_input or "anonymous"                           # returns an operand
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

#### ¿Qué diferencia hay entre una clase y una instancia?

Una clase es un modelo que define atributos y métodos. Una instancia es un objeto creado a partir de ella con su propio estado: `p = Point(1, 2)`.

<!-- challenge -->

`timeout = config.get("timeout") or 30` pone 30 cuando la config dice explícitamente `0` (sin timeout). ¿Cómo lo arreglas?

<!-- solution -->

`or` trata el 0 como falso. Prueba explícitamente los valores faltantes: `timeout = config.get("timeout"); timeout = 30 if timeout is None else timeout`.

<!-- takeaways -->

- Las funciones son valores que puedes pasar y devolver.
- `partial` fija argumentos; las lambdas son de una línea.
- `and`/`or` devuelven operandos y hacen cortocircuito.

<!-- unit: Closures y alcance -->

<!-- goals -->

- Escribir closures y evitar la trampa del late binding.
- Usar con criterio la recursión y la memoización.

<!-- concept -->

Una función definida dentro de otra recuerda las variables a su alrededor, incluso después de que la exterior retorna. Eso es un closure, el mecanismo detrás de los decoradores y las funciones fábrica. Busca esas variables al ser llamada, no al ser definida, lo que sorprende en los ciclos.
La recursión encaja con estructuras naturalmente recursivas, pero tiene un límite de profundidad y trabajo repetido. Cachear los resultados por argumento elimina las repeticiones.

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

<!-- challenge -->

Una función recursiva que recorre un JSON muy anidado falla con `RecursionError` en un archivo. ¿Qué haces?

<!-- solution -->

Reescríbela de forma iterativa con una pila explícita (una lista o un deque) de elementos por visitar, que no tiene límite de profundidad; subir el límite de recursión solo pospone la caída.

<!-- takeaways -->

- Los closures recuerdan las variables que los envuelven.
- Leen las variables al llamarse; átalas con defaults.
- La recursión tiene límites; el caché evita trabajo repetido.

<!-- unit: Documentar y tipar funciones -->

<!-- goals -->

- Escribir docstrings y type hints, incluidos los valores opcionales.
- Distinguir funciones de métodos.

<!-- concept -->

La firma de una función le dice a quien la llama cómo usarla; los docstrings y los type hints le dicen qué significa. Los hints no se imponen en ejecución, pero los editores y los chequeadores de tipos los usan para atrapar errores antes de correr el código, y documentan la intención mejor que los nombres solos.
Los métodos son funciones atadas a clases, con la instancia pasada automáticamente. Saberlo ayuda cuando pasas métodos como callbacks.

<!-- example -->

```python
def parse_amount(raw: str, default: float | None = None) -> float | None:
    """Parse '1.234,56' or '1234.56' into a float.

    Returns `default` when the value is empty or invalid.
    """
    ...
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

<!-- challenge -->

Una función está anotada `-> float` pero devuelve `None` con entradas malas, y quienes la llaman fallan con `None + 1`. ¿Cómo ayudan los hints a evitarlo?

<!-- solution -->

Anótala con honestidad como `-> float | None` y corre un chequeador de tipos (mypy, pyright), que entonces marca a quienes usan el resultado sin manejar `None`.

<!-- takeaways -->

- Los docstrings explican el comportamiento; los hints, los tipos.
- Los hints no se imponen pero alimentan los chequeadores de tipos.
- `X | None` marca valores opcionales.

### Programación orientada a objetos

<!-- unit: Clases e instancias -->

<!-- goals -->

- Definir clases con __init__, atributos de instancia y de clase.
- Usar staticmethod, classmethod y property.

<!-- concept -->

Una clase agrupa datos y el comportamiento que trabaja sobre ellos. Las instancias reciben sus propios atributos en `__init__`, mientras que los atributos de clase los comparten todas las instancias, útil para constantes y peligroso para datos mutables.
Los decoradores dan forma a la interfaz: los class methods construyen constructores alternativos, los static methods agrupan ayudas y las properties exponen valores calculados o validación detrás de la sintaxis de un atributo simple.

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

<!-- challenge -->

Una clase define `items = []` a nivel de clase, y todas las instancias terminan compartiendo los mismos ítems. Arréglalo.

<!-- solution -->

Crea la lista por instancia en `__init__` (`self.items = []`). Los atributos mutables a nivel de clase los comparten todas las instancias.

<!-- takeaways -->

- Los atributos de instancia van en `__init__`; los de clase se comparten.
- Los classmethods son constructores alternativos.
- Las properties esconden cálculos detrás de atributos.

<!-- unit: Herencia y composición -->

<!-- goals -->

- Usar herencia, super() y clases base abstractas.
- Explicar el MRO y cuándo es mejor la composición.

<!-- concept -->

La herencia permite que una clase reutilice y especialice el comportamiento de otra, con `super()` llamando a la versión del padre. Con herencia múltiple, el orden de resolución de métodos decide qué implementación gana. Las clases base abstractas definen métodos que las subclases deben implementar.
Las jerarquías profundas se vuelven rígidas, eso sí. La composición, construir objetos a partir de otros objetos, suele dar la misma reutilización con menos acoplamiento: un pipeline que tiene un lector y un escritor es más fácil de cambiar que uno que es un tipo especial de ambos.

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

#### ¿Qué es la composición y por qué suele preferirse a la herencia?

Construir objetos a partir de otros objetos ("tiene un") en lugar de extender clases ("es un"). Da un acoplamiento más débil y evita jerarquías de clases profundas y frágiles.

#### ¿Qué es la encapsulación en Python?

Python no tiene miembros privados. Por convención, `_name` es interno, y `__name` activa el name mangling (`_Class__name`) para evitar colisiones en las subclases.

#### ¿Qué hace que un objeto sea hashable?

Un `__hash__` que no cambie durante su vida y un `__eq__` coherente con él (objetos iguales deben tener el mismo hash). Definir `__eq__` sin `__hash__` hace que una clase no sea hashable.

#### ¿Qué es una metaclase?

La clase de una clase (por defecto `type`), que controla cómo se crean las clases. Rara vez hace falta: los decoradores de clase y `__init_subclass__` cubren la mayoría de los casos.

<!-- challenge -->

Un equipo tiene `CsvS3Pipeline`, `CsvLocalPipeline`, `JsonS3Pipeline`, `JsonLocalPipeline`… y cada formato o destino nuevo duplica las clases. ¿Cómo lo reestructuras?

<!-- solution -->

Compón: un `Pipeline` que recibe un `Reader` (CSV, JSON) y un `Sink` (S3, local) como parámetros. Los formatos o destinos nuevos agregan una clase cada uno en lugar de multiplicar combinaciones.

<!-- takeaways -->

- `super()` llama a la implementación del padre.
- Las ABCs definen métodos obligatorios.
- Prefiere la composición a las jerarquías profundas.

<!-- unit: El data model y los métodos dunder -->

<!-- goals -->

- Implementar métodos dunder como __repr__, __eq__, __hash__ y __call__.
- Usar dataclasses y __slots__.

<!-- concept -->

La sintaxis de Python funciona con métodos especiales. Definir `__repr__` da una salida de depuración legible; `__eq__` y `__hash__` deciden la igualdad y si los objetos pueden ser claves de dict; `__call__` hace que las instancias se comporten como funciones. Implementarlos hace que tus clases se sientan incorporadas.
Las dataclasses generan los más comunes a partir de las declaraciones de campos, y `__slots__` recorta memoria en clases con millones de instancias.

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

#### ¿Qué es `__call__`?

Un método que hace que las instancias se puedan llamar como funciones, útil para objetos función configurables.

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

<!-- challenge -->

Objetos de una dataclass mutable se usan como claves de dict, luego cambia un campo y las búsquedas dejan de encontrarlos. ¿Por qué y cómo se arregla?

<!-- solution -->

El hash depende de los campos; cambiar un campo cambia el hash, así que el dict busca en el lugar equivocado. Usa `frozen=True` para los objetos clave (o no los mutes).

<!-- takeaways -->

- Los métodos dunder conectan las clases con la sintaxis.
- Los objetos hashables no deben cambiar su hash.
- Las dataclasses generan el boilerplate.

<!-- unit: Interfaces por comportamiento -->

<!-- goals -->

- Aplicar duck typing y Protocols.
- Entender las convenciones de encapsulamiento de Python y las metaclases.

<!-- concept -->

A Python le importa lo que un objeto puede hacer, no lo que es. Cualquier objeto con un método `read` se puede tratar como archivo; eso es duck typing. Los Protocols permiten que los chequeadores de tipos lo verifiquen estructuralmente, sin herencia.
La privacidad es por convención: un guion bajo inicial significa "interno" y dos guiones bajos alteran el nombre para evitar choques. Las metaclases, que personalizan cómo se crean las clases mismas, existen pero rara vez son la herramienta correcta en código de aplicación.

<!-- example -->

```python
from typing import Protocol

class SupportsRead(Protocol):
    def read(self, n: int = -1) -> bytes: ...

def checksum(src: SupportsRead) -> str:     # works with files, BytesIO, S3 streams...
    import hashlib
    return hashlib.sha256(src.read()).hexdigest()
```

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

<!-- challenge -->

Una función exige `isinstance(f, io.FileIO)` y rechaza streams de S3 y objetos `BytesIO` que funcionarían bien. ¿Cómo haces que los acepte?

<!-- solution -->

Quita el chequeo `isinstance` y confía en el comportamiento (llama `read()`), tipando el parámetro como un `Protocol` con `read`, así se acepta cualquier objeto legible y los chequeadores lo siguen verificando.

<!-- takeaways -->

- Duck typing: comportamiento por encima del tipo.
- Los Protocols chequean el comportamiento estructuralmente.
- Los nombres con guion bajo son internos por convención.

### Iteradores, generadores, decoradores y gestores de contexto

<!-- unit: Iteradores y generadores -->

<!-- goals -->

- Distinguir iterables de iteradores y escribir generadores.
- Hacer iterables las clases y delegar con yield from.

<!-- concept -->

Todo lo que puedes recorrer es un iterable; recorrerlo le pide un iterador, que entrega los elementos uno a uno hasta agotarse. Los generadores son la forma fácil de escribir iteradores: una función con `yield` se pausa tras cada elemento y se reanuda en la siguiente petición.
Como los iteradores se consumen al recorrerlos, un generador solo se puede recorrer una vez. Ese es el precio de su ventaja: pueden producir secuencias infinitas o enormes casi sin memoria.

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

<!-- challenge -->

Una función pasa un generador a dos consumidores: uno valida filas y el otro las carga. El cargador no recibe nada. ¿Por qué y cuáles son dos soluciones?

<!-- solution -->

El validador agotó el generador. O llamas dos veces la función generadora (iteradores nuevos), o validas y cargas en una sola pasada; `itertools.tee` funciona pero guarda datos en buffer.

<!-- takeaways -->

- Los iterables producen iteradores; los iteradores se consumen.
- Los generadores se pausan en `yield` y usan poca memoria.
- Un generador se puede recorrer una sola vez.

<!-- unit: Pipelines perezosos con itertools -->

<!-- goals -->

- Construir pipelines livianos en memoria con generadores e itertools.
- Usar bien groupby, islice y batched.

<!-- concept -->

Encadenar generadores crea pipelines que procesan los datos como un flujo: leer una línea, parsearla, filtrarla y escribirla, sin tener nunca el archivo completo. `itertools` aporta las piezas: concatenar, rebanar, agrupar, hacer lotes y acumular cualquier iterador.
Una pieza sorprende: `groupby` solo agrupa elementos consecutivos con la misma clave, así que la entrada ya debe estar ordenada por esa clave.

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

#### ¿Cómo se leen solo los n primeros elementos de un iterador?

`itertools.islice(it, n)`, que funciona con cualquier iterador, incluidos los infinitos.

#### ¿Cómo se divide un iterable en lotes de tamaño fijo?

`itertools.batched(iterable, n)` en Python 3.12+, o con `islice` en un bucle en versiones anteriores.

#### ¿Qué diferencia hay entre `return` y `yield` en una función?

`return` termina la función y devuelve un valor. `yield` convierte la función en un generador que produce una serie de valores a lo largo del tiempo, reanudándose donde se quedó.

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

<!-- challenge -->

`groupby(rows, key=lambda r: r["country"])` devuelve "CO" tres veces como grupos separados. ¿Qué está mal?

<!-- solution -->

`groupby` agrupa solo elementos consecutivos; las filas no están ordenadas por país. Ordena primero (`sorted(rows, key=...)`) o usa un `defaultdict(list)` para agrupar sin ordenar.

<!-- takeaways -->

- Los pipelines de generadores procesan datos en memoria constante.
- `itertools` da rebanado, lotes y agrupación.
- `groupby` necesita la entrada ordenada por la clave.

<!-- unit: Decoradores -->

<!-- goals -->

- Escribir decoradores que conserven los metadatos de la función.
- Escribir decoradores que reciban argumentos.

<!-- concept -->

Un decorador envuelve una función para agregarle comportamiento alrededor, como medición de tiempo, reintentos, caché o logs, sin cambiar su código. La sintaxis `@` es un atajo para reemplazar la función por su versión envuelta.
Dos detalles vuelven los decoradores aptos para producción: copiar el nombre y el docstring de la función original con `functools.wraps`, y un nivel extra de anidamiento cuando el decorador mismo necesita parámetros.

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

<!-- challenge -->

Tras decorar funciones con un `@timed` casero, todas aparecen en los logs y tracebacks con el nombre "wrapper". ¿Qué falta?

<!-- solution -->

`@functools.wraps(func)` sobre el wrapper interno, que copia el nombre, el docstring y otros metadatos de la función original.

<!-- takeaways -->

- Los decoradores envuelven funciones para agregar comportamiento.
- Usa siempre `functools.wraps`.
- Los decoradores con parámetros agregan un nivel de anidamiento.

<!-- unit: Context managers -->

<!-- goals -->

- Usar y escribir context managers, también con contextlib.
- Controlar el manejo de excepciones en __exit__ y manejar muchos recursos con ExitStack.

<!-- concept -->

Recursos como archivos, conexiones, locks y transacciones necesitan limpieza incluso cuando hay errores. Los context managers la garantizan: la preparación corre al entrar al bloque `with` y el cierre al salir, sin importar cómo se salga.
`contextlib` convierte un generador en context manager en pocas líneas. `__exit__` decide si una excepción se propaga, y `ExitStack` maneja a la vez una cantidad variable de recursos.

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

<!-- challenge -->

El `__exit__` de un context manager casero devuelve `True` "por seguridad", y los errores dentro de los bloques `with` desaparecen. ¿Qué pasa?

<!-- solution -->

Devolver un valor verdadero desde `__exit__` suprime la excepción. Devuelve `None`/`False` (o vuelve a lanzarla) para que los errores se propaguen tras la limpieza.

<!-- takeaways -->

- Los context managers garantizan la limpieza.
- `@contextmanager` los construye desde generadores.
- Un `__exit__` que devuelve verdadero se traga las excepciones.

<!-- stage: Trabajar con el mundo exterior -->

### Errores, archivos y biblioteca estándar

<!-- unit: Excepciones -->

<!-- goals -->

- Manejar, lanzar y encadenar excepciones correctamente.
- Definir excepciones propias y elegir entre EAFP y LBYL.

<!-- concept -->

Un buen manejo de errores atrapa solo lo que puede manejar y deja que todo lo demás salga a la superficie. Cláusulas `except` específicas, limpieza en `finally` y un `else` para el código que solo debe correr si todo salió bien mantienen clara la intención. Un `except` desnudo esconde bugs y hasta bloquea Ctrl+C.
Las excepciones propias dan a quien llama tipos con sentido para atrapar, el encadenamiento conserva la causa original en los tracebacks y los exception groups reportan varias fallas a la vez.

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

<!-- challenge -->

Un cargador envuelve todo en `try: ... except: pass`, y durante semanas nadie nota que faltan datos. ¿Cómo lo reescribes?

<!-- solution -->

Atrapa solo los errores esperados (por ejemplo `ValueError` para registros malos), regístralos con contexto y cuéntalos, y deja que las excepciones inesperadas se propaguen para que el job falle de forma visible.

<!-- takeaways -->

- Atrapa solo excepciones específicas.
- Encadena con `raise ... from exc`.
- Los tipos de excepción propios ayudan a quien llama.

<!-- unit: Archivos y rutas -->

<!-- goals -->

- Leer archivos grandes con seguridad con `with` e iterando por líneas.
- Usar pathlib, compresión y archivos temporales.

<!-- concept -->

Los archivos son la entrada más común en el trabajo con datos, y dos hábitos evitan la mayoría de problemas. Ábrelos con `with`, para que se cierren incluso con errores. Recórrelos línea por línea, para que la memoria se mantenga constante sin importar el tamaño.
`pathlib` vuelve las rutas objetos que puedes unir, inspeccionar y buscar con glob; los módulos de compresión leen y escriben archivos comprimidos como si fueran planos; y los archivos temporales se limpian solos.

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

#### ¿Para qué sirve `tempfile`?

Para crear archivos y directorios temporales que se limpian automáticamente: `with tempfile.TemporaryDirectory() as tmp: ...`.

#### ¿Cómo se comprimen o descomprimen archivos en Python?

Con los módulos `gzip`, `bz2`, `lzma` y `zipfile`. `gzip.open(path, "rt", encoding="utf-8")` lee un archivo de texto comprimido línea a línea.

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

<!-- challenge -->

Un script llama `open(path).read().splitlines()` sobre archivos de log de 30 GB y se cae. Reescribe la parte de lectura.

<!-- solution -->

`with open(path, encoding="utf-8") as f: for line in f: process(line)`, que lee una línea a la vez y cierra el archivo con seguridad.

<!-- takeaways -->

- Abre los archivos con `with`.
- Itera por líneas para mantener constante la memoria.
- `pathlib` para rutas; `gzip` para archivos comprimidos.

<!-- unit: Formatos de datos y fechas -->

<!-- goals -->

- Leer y escribir CSV y JSON con la librería estándar.
- Parsear fechas y usar datetimes con zona horaria.

<!-- concept -->

La librería estándar maneja los formatos de todos los días. El módulo `csv` resuelve las comillas y los delimitadores que una división ingenua hace mal; `json` convierte entre texto y dicts, con ganchos para los tipos que no conoce.
Las fechas requieren cuidado: parsea con formatos explícitos y mantén los tiempos conscientes de su zona horaria, de preferencia en UTC, porque mezclar datetimes naive y aware causa errores y corrimientos silenciosos.

<!-- example -->

```python
import csv, json
from datetime import datetime, timezone

with open("in.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))
ts = datetime.strptime("17/10/2026 09:41", "%d/%m/%Y %H:%M").replace(tzinfo=timezone.utc)
print(json.dumps({"rows": len(rows), "loaded_at": ts}, default=str))
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

<!-- challenge -->

Un script divide líneas CSV con `line.split(",")`, y algunas filas salen con campos de más. ¿Por qué y cómo se arregla?

<!-- solution -->

Campos como `"Pérez, Ana"` contienen comas dentro de comillas. Usa `csv.reader`/`DictReader`, que manejan bien las comillas y los escapes.

<!-- takeaways -->

- Usa `csv` en vez de dividir líneas.
- `json` maneja texto ↔ dicts; `default=` para tipos propios.
- Mantén los datetimes con zona, idealmente en UTC.

<!-- unit: Módulos estándar útiles -->

<!-- goals -->

- Registrar logs bien y construir interfaces de línea de comandos.
- Usar expresiones regulares, subprocesos y hashing.

<!-- concept -->

"Baterías incluidas" significa que casi todas las utilidades ya están ahí. `logging` da niveles, formato y handlers, así los mensajes pueden ir a la consola en desarrollo y a archivos o colectores en producción. `argparse` convierte los scripts en herramientas de línea de comandos de verdad.
Las expresiones regulares extraen estructura del texto; `subprocess` corre comandos externos con seguridad sin un shell; `hashlib` calcula checksums de archivos y llaves seudonimizadas.

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

<!-- challenge -->

Un script corre `subprocess.run(f"rm -rf {folder}", shell=True)` con un nombre de carpeta que llega del usuario. ¿Cuál es el riesgo y la solución?

<!-- solution -->

Inyección de shell: un nombre preparado podría correr comandos arbitrarios. Pasa una lista de argumentos sin `shell=True`, valida la ruta y prefiere `shutil.rmtree` en lugar de llamar al shell.

<!-- takeaways -->

- Usa `logging` con loggers por módulo y formato perezoso.
- `argparse` construye interfaces de línea de comandos.
- Corre subprocesos con listas de argumentos, sin shell.

### Concurrencia y rendimiento

<!-- unit: El GIL y los modelos de concurrencia -->

<!-- goals -->

- Explicar el GIL y comparar threading, multiprocessing y asyncio.
- Usar concurrent.futures y evitar condiciones de carrera y problemas de pickling.

<!-- concept -->

En CPython, solo un hilo corre bytecode de Python a la vez. Los hilos igual ayudan cuando el trabajo espera redes o discos, porque esperar libera el lock; el trabajo pesado en CPU necesita procesos, cada uno con su propio intérprete. Asyncio maneja muchas esperas en un solo hilo.
Cada modelo tiene sus trampas: los hilos que comparten datos necesitan locks para evitar condiciones de carrera; los procesos necesitan funciones y datos serializables con pickle; los hilos daemon mueren de golpe al salir.

<!-- example -->

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=16) as pool:          # I/O-bound: downloads
    pages = list(pool.map(fetch, urls))

def heavy(chunk): ...                                     # module-level: picklable
with ProcessPoolExecutor() as pool:                       # CPU-bound: parsing
    results = list(pool.map(heavy, chunks))
```

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

#### ¿Qué es un entorno virtual y por qué usarlo?

Una instalación de Python aislada con sus propios paquetes (`python -m venv .venv`), para que cada proyecto tenga sus versiones de dependencias y no rompa el Python del sistema ni otros proyectos.

<!-- challenge -->

Un equipo acelera un job de parseo pesado en CPU con 16 hilos y no ve mejora. ¿Por qué y qué sugieres?

<!-- solution -->

El GIL deja correr código Python a un solo hilo a la vez, así que los hilos limitados por CPU no corren en paralelo. Usa un `ProcessPoolExecutor` (o una librería vectorizada) para aprovechar varios cores.

<!-- takeaways -->

- Hilos para I/O; procesos para CPU.
- Los datos compartidos entre hilos necesitan locks.
- Los pools de procesos necesitan funciones serializables a nivel de módulo.

<!-- unit: asyncio -->

<!-- goals -->

- Explicar las corrutinas, el event loop y asyncio.run.
- Limitar la concurrencia, fijar timeouts y manejar backpressure.

<!-- concept -->

El código async corre muchas tareas de I/O en un solo hilo. Las corrutinas se pausan en cada `await`, dejando que el event loop corra otras mientras esperan. Llamar a una función async solo crea una corrutina; el loop debe correrla, y eso hace `asyncio.run` en el nivel superior.
La concurrencia necesita límites. Las APIs con límite de tasa necesitan semáforos y backoff, cada llamada de red necesita un timeout y los productores rápidos necesitan colas acotadas para que la memoria no crezca sin fin.

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

<!-- challenge -->

Un scraper async dispara 50.000 solicitudes con `gather` de una vez y la API bloquea al cliente. ¿Cómo lo arreglas?

<!-- solution -->

Limita la concurrencia con un `asyncio.Semaphore` (o un pool de workers acotado), respeta `Retry-After`, reintenta los 429 con backoff exponencial y fija timeouts en cada solicitud.

<!-- takeaways -->

- Las corrutinas se pausan en `await`; el loop corre otras.
- `asyncio.run` arranca el event loop.
- Acota la concurrencia; fija siempre timeouts.

<!-- unit: Hacer el código más rápido -->

<!-- goals -->

- Perfilar antes de optimizar y saber qué hace rápido a Python.
- Evitar el pandas fila por fila y elegir entre PyPy, multiprocessing y Spark.

<!-- concept -->

La velocidad viene de medir y luego cambiar la parte más lenta. Los profilers muestran a dónde va el tiempo, a menudo a un lugar inesperado. La mayoría de ganancias vienen de mejores algoritmos y estructuras de datos, y de llevar los ciclos a C: built-ins, NumPy, operaciones vectorizadas de pandas o Polars.
Otros intérpretes y el paralelismo ayudan en casos puntuales. Spark es para datos que superan una máquina, no para acelerar jobs pequeños.

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

<!-- challenge -->

Una transformación de pandas usa `df.apply(func, axis=1)` sobre 20 millones de filas y tarda 40 minutos. ¿Qué pruebas primero?

<!-- solution -->

Reescribe `func` con operaciones vectorizadas de columnas (aritmética, `np.where`, accesores `str` y `dt`) para que el trabajo corra en C; perfila para confirmarlo y considera Polars si sigue lento.

<!-- takeaways -->

- Perfila primero.
- Mejores estructuras de datos y vectorización ganan casi siempre.
- Spark es para escala, no para acelerar jobs pequeños.

<!-- unit: Memoria -->

<!-- goals -->

- Explicar cómo maneja Python la memoria.
- Encontrar crecimientos de memoria tipo fuga y entender las cachés de bytecode.

<!-- concept -->

CPython libera la mayoría de objetos en el momento en que nada los referencia, mediante conteo de referencias, y un recolector de ciclos limpia los grupos de objetos que solo se referencian entre sí. Los problemas de memoria en programas de larga vida son entonces casi siempre referencias que siguen vivas: cachés globales, listas que crecen, closures que retienen objetos grandes.
Encontrarlas implica medir las asignaciones en el tiempo. Las cachés de bytecode no tienen que ver, aunque a menudo se confunden con memoria: solo aceleran los imports.

<!-- example -->

```python
import tracemalloc
tracemalloc.start()
run_batch()
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("lineno")[:5]:
    print(stat)          # top allocation sites
```

#### ¿Qué diferencia hay entre tests unitarios, de integración y de extremo a extremo?

Los tests unitarios comprueban una función o clase de forma aislada. Los de integración comprueban componentes trabajando juntos (código y una base de datos). Los de extremo a extremo ejecutan todo el sistema con entradas realistas.

#### ¿Qué herramientas mantienen alta la calidad del código Python?

Un formateador y un linter (ruff, o black y flake8), un comprobador de tipos (mypy, pyright), hooks de pre-commit, tests en CI y revisión de código.

#### ¿Cómo se comprueban los tipos con mypy?

Añadiendo anotaciones de tipo y ejecutando `mypy src/`. Informa de las incoherencias de tipos de forma estática, antes de la ejecución. Se adopta poco a poco con configuración por módulo.

<!-- challenge -->

La memoria de un worker de larga vida crece 100 MB por hora hasta que lo matan. El código tiene un `CACHE = {}` a nivel de módulo que se llena en cada solicitud. ¿Qué cambias?

<!-- solution -->

Acota la caché: usa `functools.lru_cache(maxsize=...)` o una caché limitada por tamaño o tiempo, o límpiala periódicamente; confirma con `tracemalloc` que era el origen.

<!-- takeaways -->

- El conteo de referencias libera objetos de inmediato.
- Las fugas suelen ser referencias que siguen vivas.
- Mide las asignaciones con `tracemalloc`.

<!-- stage: Práctica de ingeniería -->

### Tipado, empaquetado, entornos y tests

<!-- unit: Entornos y empaquetado -->

<!-- goals -->

- Aislar proyectos con entornos virtuales y pyproject.toml.
- Hacer reproducibles las instalaciones y construir wheels con entry points.

<!-- concept -->

Cada proyecto necesita su propio conjunto de paquetes, o las actualizaciones de uno rompen otro. Los entornos virtuales los aíslan; `pyproject.toml` declara el proyecto, sus dependencias y sus herramientas en un solo lugar.
La reproducibilidad viene de lock files que fijan la versión de cada paquete, instalados igual en desarrollo, CI y producción. Los wheels empaquetan tu código para desplegarlo, y los entry points convierten funciones en comandos.

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

#### ¿Cómo se lee un CSV grande con pandas sin quedarse sin memoria?

Leyendo por bloques, seleccionando solo las columnas necesarias, fijando tipos compactos, o usando un formato en columnas y un motor perezoso:

```python
for chunk in pd.read_csv("big.csv", usecols=["id", "amount"], dtype={"id": "int64"}, chunksize=500_000):
    process(chunk)
```

<!-- challenge -->

Un job funciona en el portátil de un desarrollador pero falla en producción después de que una librería sacó una versión major nueva. ¿Qué implementas?

<!-- solution -->

Un lock file (uv, pip-tools o Poetry) que fije todas las versiones, instalado con `--frozen` en CI y producción, con las actualizaciones de dependencias hechas a propósito mediante pull requests.

<!-- takeaways -->

- Un entorno virtual por proyecto.
- `pyproject.toml` declara el proyecto.
- Los lock files hacen reproducibles las instalaciones.

<!-- unit: Pruebas con pytest -->

<!-- goals -->

- Escribir pruebas con pytest usando fixtures, parametrización y mocks.
- Elegir niveles de prueba y usar con criterio la cobertura y las pruebas basadas en propiedades.

<!-- concept -->

pytest mantiene simples las pruebas: funciones comunes con `assert` común y mensajes de falla útiles. Los fixtures dan lo que necesitan las pruebas, desde datos de ejemplo hasta directorios temporales; la parametrización corre una prueba sobre muchas entradas; los mocks reemplazan dependencias lentas o externas.
Una suite equilibrada tiene muchas pruebas unitarias rápidas, algunas de integración y unas pocas de punta a punta. La cobertura muestra las zonas sin probar; las pruebas basadas en propiedades encuentran casos borde que no pensaste.

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

<!-- challenge -->

Las pruebas de un cliente de API llaman a la API real, así que son lentas y fallan cuando está caída. ¿Cómo las arreglas?

<!-- solution -->

Simula la capa HTTP en las pruebas unitarias (pytest-mock, respx o responses) con respuestas grabadas, y deja una o dos pruebas de integración contra un sandbox, corridas por separado.

<!-- takeaways -->

- pytest: asserts simples, fixtures, parametrización.
- Simula las dependencias externas en las pruebas unitarias.
- La cobertura es una señal, no una meta.

<!-- unit: Chequeos estáticos y tipos -->

<!-- goals -->

- Mantener alta la calidad del código con formateadores, linters y chequeadores de tipos.
- Usar mypy, TypedDict y genéricos.

<!-- concept -->

Los chequeos automáticos atrapan errores antes de que corran las pruebas. Un formateador acaba los debates de estilo, un linter marca bugs y malos patrones, y un chequeador de tipos encuentra argumentos equivocados y `None`s sin manejar usando tus hints. Correrlos en pre-commit y CI los vuelve rutina.
Los type hints rinden más con tipos más ricos: `TypedDict` describe registros con forma de dict, y los genéricos describen contenedores y funciones que trabajan con cualquier tipo de forma consistente.

<!-- example -->

```python
from typing import TypedDict, TypeVar

class OrderRow(TypedDict):
    order_id: int
    amount: float
    country: str

T = TypeVar("T")
def first_or_none(items: list[T]) -> T | None:
    return items[0] if items else None
```
```bash
ruff check . && ruff format --check . && mypy src/
```

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

<!-- challenge -->

Una función recibe filas como dicts, y errores de tipeo como `row["ammount"]` llegan a producción. ¿Cómo puede atraparlos el tipado?

<!-- solution -->

Describe las filas con un `TypedDict` (o una dataclass o un modelo pydantic) y anota la función; mypy marca entonces claves desconocidas como `"ammount"` antes de que corra el código.

<!-- takeaways -->

- Formatea, haz lint y chequea tipos automáticamente.
- `TypedDict` tipa registros en forma de dict.
- Los genéricos mantienen consistentes los tipos de los contenedores.

<!-- unit: Configuración y estructura del proyecto -->

<!-- goals -->

- Manejar la configuración y los secretos con seguridad.
- Validar los ajustes con pydantic y estructurar un proyecto de pipeline.

<!-- concept -->

El mismo código debe correr en desarrollo, CI y producción con ajustes distintos, así que la configuración sale del ambiente, nunca de valores fijos en el código, y los secretos de un gestor de secretos. Validarla al arrancar, con errores claros, es mejor que descubrir una variable faltante a mitad de un job.
La estructura del proyecto sigue las responsabilidades: un paquete `src` dividido en ingesta, transformaciones y salidas, entry points delgados y pruebas junto al código que cubren.

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

#### ¿Cómo se conecta uno a una base de datos desde Python de forma segura?

Con un driver (psycopg para PostgreSQL) o SQLAlchemy, usando consultas parametrizadas y nunca formateo de cadenas, para evitar la inyección SQL:

```python
cur.execute("select * from companies where country = %s", (country,))
```

#### ¿Cómo se cargan muchas filas en PostgreSQL rápidamente desde Python?

Con `COPY` (el `cursor.copy()` de psycopg) en lugar de inserciones fila a fila, o con inserciones por lotes mediante `executemany` y tamaños de página. Haz la carga en una sola transacción.

#### ¿Qué es SQLAlchemy?

Un conjunto de herramientas para bases de datos con una capa Core (lenguaje de expresiones SQL, pool de conexiones, engines) y un ORM. pandas usa engines de SQLAlchemy para `read_sql` y `to_sql`.

<!-- challenge -->

Un job lee `os.environ["BATCH_SIZE"]` en lo profundo de un ciclo y se cae tras dos horas cuando falta en producción. ¿Cómo lo evitas?

<!-- solution -->

Carga y valida toda la configuración una vez al arrancar (settings de pydantic o una función de validación), con tipos y valores por defecto, para que los valores faltantes o inválidos fallen de inmediato.

<!-- takeaways -->

- Configuración desde el ambiente; secretos desde un gestor.
- Valida los ajustes al arrancar.
- Estructura los proyectos por responsabilidad.

### Python para ingeniería de datos

<!-- unit: Lo esencial de pandas -->

<!-- goals -->

- Leer archivos grandes con pandas y seleccionar datos con loc e iloc.
- Agrupar, combinar y manejar valores faltantes sin advertencias.

<!-- concept -->

pandas es la herramienta diaria para datos que caben en memoria. Sus movimientos básicos son seleccionar (por etiqueta o posición), agrupar con agregaciones con nombre, combinar como los joins de SQL y manejar los valores faltantes a propósito.
La memoria es el límite usual: leer solo las columnas necesarias con tipos compactos, o por partes, la estira bastante. La indexación encadenada dispara la famosa advertencia porque pandas no puede saber si estás cambiando una copia o el original.

<!-- example -->

```python
import pandas as pd
df = pd.read_csv("companies.csv", usecols=["country", "industry", "revenue"],
                 dtype={"country": "category", "industry": "category"})
summary = (df.groupby(["country", "industry"], as_index=False, observed=True)
             .agg(companies=("revenue", "size"), revenue=("revenue", "sum")))
df.loc[df["revenue"] < 0, "revenue"] = pd.NA       # assign on the original, no warning
```

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

<!-- challenge -->

`pd.merge(orders, customers, on="customer_id")` devuelve más filas que `orders`. ¿Qué pasó y cómo lo atrapas?

<!-- solution -->

`customers` tiene `customer_id` duplicados, así que las órdenes se multiplican. Deduplica primero los clientes y usa `validate="many_to_one"` en `merge`, que falla si el lado derecho no es único.

<!-- takeaways -->

- Lee solo las columnas necesarias con dtypes compactos.
- Usa `.loc` para las asignaciones.
- `merge(validate=...)` atrapa el fan-out.

<!-- unit: Formatos columnares y motores rápidos -->

<!-- goals -->

- Explicar Parquet y Arrow y escribir Parquet particionado.
- Saber cuándo Polars o DuckDB le ganan a pandas.

<!-- concept -->

CSV es un mal formato para analítica: sin tipos, sin comprimir, se lee completo. Parquet guarda los datos por columna con tipos y estadísticas, así las herramientas leen solo lo que necesitan. Arrow es el formato en memoria equivalente, que permite a pandas, Polars, DuckDB y Spark intercambiar datos sin copiarlos.
Sobre ellos, motores más nuevos cambian lo que puede hacer una máquina: Polars corre multihilo con un optimizador de consultas, y DuckDB corre SQL directamente sobre archivos Parquet y DataFrames.

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

<!-- challenge -->

Un analista carga 8 GB de CSVs en pandas para calcular un agregado y se queda sin memoria. ¿Qué le sugerirías?

<!-- solution -->

Convierte los archivos a Parquet una vez y luego consúltalos con DuckDB (o con escaneos perezosos de Polars), que leen solo las columnas necesarias, procesan los datos en flujo y usan todos los cores.

<!-- takeaways -->

- Parquet es tipado, columnar y comprimido.
- Arrow permite que las herramientas compartan datos sin copias.
- Polars y DuckDB estiran los límites de una sola máquina.

<!-- unit: APIs, archivos y bases de datos -->

<!-- goals -->

- Llamar APIs REST de forma robusta y descargar archivos grandes en flujo.
- Conectarse a bases con seguridad, cargar filas en bloque y leer desde S3.

<!-- concept -->

Los pipelines pasan buena parte de su tiempo hablando con otros sistemas, y cada conversación puede fallar. Las llamadas a APIs necesitan sesiones, timeouts, reintentos con backoff y paginación. Las descargas grandes deben ir en flujo a disco en lugar de llenar la memoria.
Las bases de datos necesitan consultas parametrizadas por seguridad y caminos masivos como `COPY` por velocidad; SQLAlchemy agrega pooling y portabilidad. El almacenamiento de objetos tiene sus propios clientes, o acceso tipo archivo con fsspec.

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

<!-- challenge -->

Un job arma SQL con `f"SELECT * FROM users WHERE email = '{email}'"`. ¿Cuáles son los dos problemas y la solución?

<!-- solution -->

Inyección SQL (un valor preparado puede cambiar la consulta) y errores de comillas (los correos con apóstrofo la rompen). Usa consultas parametrizadas: `cur.execute("... WHERE email = %s", (email,))`.

<!-- takeaways -->

- Sesiones, timeouts, reintentos y paginación para las APIs.
- Descarga en flujo los archivos grandes.
- Parametriza el SQL; carga en bloque con `COPY`.

<!-- unit: Pasos de pipeline confiables -->

<!-- goals -->

- Hacer idempotentes los pasos de un pipeline y validar los datos antes de cargarlos.
- Manejar codificaciones y JSON grandes, y orquestar pipelines en Python.

<!-- concept -->

Un paso de pipeline se va a reintentar, volver a correr y alimentar con datos sorprendentes. Los pasos idempotentes, que dan el mismo resultado si corren dos veces, hacen seguros los reintentos; validar antes de cargar frena los datos malos en la puerta. Codificación y tamaño de archivos son sorpresas comunes.
La programación, las dependencias y las alertas le corresponden a un orquestador y no a cron y la esperanza. Si Python transforma los datos él mismo (ETL) o sobre todo los mueve para que un warehouse los transforme (ELT) define cuánto de eso escribes.

<!-- example -->

```python
def load_day(conn, day: str, rows: list[dict]) -> None:
    validate(rows)                                   # schema, nulls, ranges, duplicates
    with conn.transaction():
        conn.execute("DELETE FROM sales WHERE sale_date = %s", (day,))
        copy_rows(conn, "sales", rows)               # rerun-safe: replaces the day
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

<!-- challenge -->

Un paso diario anexa filas a una tabla, y un reintento tras un timeout duplicó los datos del día. Reescribe su estrategia de escritura.

<!-- solution -->

Reemplaza la porción del día en una transacción (borra la fecha y luego inserta, o haz upsert sobre la clave de negocio), para que correrlo dos veces deje los mismos datos.

<!-- takeaways -->

- Los pasos idempotentes hacen seguros los reintentos.
- Valida antes de cargar.
- Los orquestadores manejan horarios, reintentos y alertas.

<!-- unit: Python y Spark -->

<!-- goals -->

- Explicar cómo se relaciona PySpark con Python.
- Evitar las UDFs de Python lentas en PySpark.

<!-- concept -->

PySpark deja que Python describa cálculos distribuidos, pero el trabajo corre en el motor JVM de Spark. El código Python construye el plan; las filas rara vez tocan el intérprete de Python, y por eso PySpark escala.
La excepción son las UDFs de Python: cada fila se envía a un proceso Python y de vuelta, perdiendo velocidad y optimización. Las funciones incorporadas, o las pandas UDFs vectorizadas cuando Python es inevitable, mantienen el trabajo donde Spark es rápido.

<!-- example -->

```python
from pyspark.sql import functions as F
# slow: Python UDF per row
# clean = F.udf(lambda s: s.strip().lower())
# fast: built-in functions
df = df.withColumn("email", F.lower(F.trim("email")))
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

<!-- challenge -->

Un job de PySpark usa una UDF para calcular `price * qty * (1 - discount)`. ¿Por qué es un desperdicio y qué la reemplaza?

<!-- solution -->

Una UDF de Python serializa cada fila hacia Python para una aritmética simple que Spark hace de forma nativa. Usa una expresión de columna: `F.col("price") * F.col("qty") * (1 - F.col("discount"))`.

<!-- takeaways -->

- PySpark construye planes; la JVM los ejecuta.
- Las UDFs de Python serializan cada fila.
- Prefiere los built-ins; usa pandas UDFs si hace falta.
