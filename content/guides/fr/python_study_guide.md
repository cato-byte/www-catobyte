## Fiche d'étude Python

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Python : environ 220 questions](../../images/python_study_guide_title_img.png)

Environ 220 questions Python pour les entretiens de data engineer : le langage, la bibliothèque standard, la programmation orientée objet, les générateurs et décorateurs, la concurrence, les tests et le packaging, Python pour le travail sur les données, et une série d'exercices de code avec leurs solutions. Les exemples ciblent Python 3.12 et versions ultérieures, et les réponses couvrent ce qui a changé jusqu'à Python 3.15 (octobre 2026).

La fiche suit un parcours d'apprentissage en quatre étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Bases du langage et types de données

<!-- unit: Le modèle objet de Python -->

<!-- goals -->

- Expliquer le typage dynamique et fort, et le principe « tout est objet ».
- Distinguer objets mutables et immuables, identité et égalité, et le passage des arguments.

<!-- concept -->

En Python, les noms sont des étiquettes sur des objets, pas des boîtes à valeurs. Un nom peut être réassigné à un objet de n'importe quel type (typage dynamique), mais un objet ne change jamais de type en silence (typage fort). Chaque objet a une identité, un type et une valeur.

La mutabilité décide de ce qui se passe quand deux noms partagent un objet. Modifier un objet mutable par un nom se voit par l'autre ; un objet immuable ne peut qu'être remplacé. Les arguments suivent la même règle : le paramètre est une étiquette de plus sur l'objet de l'appelant.

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

<!-- challenge -->

Une fonction reçoit un dict de réglages, fait `settings["debug"] = True` pour son propre usage, et d'autres parties du programme se mettent à journaliser en mode debug. Pourquoi, et comment corriger ?

<!-- solution -->

La fonction a modifié le dict de l'appelant, partagé par tous. Le copier avant de le modifier (`local = {**settings, "debug": True}`) ou passer l'indicateur comme argument séparé.

<!-- takeaways -->

- Les noms sont des étiquettes sur des objets.
- Modifier un objet partagé affecte tous les noms.
- `==` pour les valeurs, `is` pour l'identité (et `None`).

<!-- unit: Nombres et valeur de vérité -->

<!-- goals -->

- Connaître les types intégrés de Python et ce qui est considéré comme faux.
- Gérer correctement division, précision des flottants et grands entiers.

<!-- concept -->

Les types intégrés de Python couvrent l'essentiel des besoins sans import : nombres, texte, séquences, dictionnaires et ensembles. Chaque objet a aussi une valeur de vérité, ce qui rend les conditions concises mais peut cacher des bugs, car zéro et les collections vides sont faux tout comme `None`.

Les nombres ont leurs pièges. La division vraie donne toujours un flottant ; la division entière arrondit vers le bas, même pour les négatifs. Les flottants sont des approximations binaires : l'argent exige `Decimal`, tandis que les entiers grandissent autant que la mémoire le permet.

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

<!-- challenge -->

`if not discount:` traite une remise de 0 comme une remise absente, et les commandes sans remise reçoivent les 10 % par défaut. Corrigez la condition.

<!-- solution -->

Tester explicitement l'absence : `if discount is None: discount = 0.10`, pour qu'une vraie valeur de 0 reste 0.

<!-- takeaways -->

- Zéro, le vide et `None` sont tous faux.
- `//` arrondit vers le bas ; `/` renvoie des flottants.
- Utilisez `Decimal` pour l'arithmétique décimale exacte.

<!-- unit: Syntaxe moderne -->

<!-- goals -->

- Utiliser l'opérateur walrus et le pattern matching structurel.
- Choisir entre listes et tuples, et faire des copies superficielles ou profondes.

<!-- concept -->

Les versions récentes de Python ont ajouté une syntaxe qui supprime du code répétitif courant. L'opérateur walrus assigne dans une expression, ce qui allège les boucles « lire et tester ». Le pattern matching vérifie une structure et en extrait des valeurs en même temps, utile pour des messages de formes différentes.

Deux choix plus anciens comptent toujours au quotidien : listes pour les collections qui changent, tuples pour les enregistrements fixes, et copies qui dupliquent seulement le conteneur extérieur ou toute la structure imbriquée.

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

<!-- challenge -->

Un test copie une config imbriquée avec `dict(config)` et modifie une liste imbriquée, puis d'autres tests échouent. Que s'est-il passé ?

<!-- solution -->

`dict(config)` est une copie superficielle : la liste imbriquée est partagée, et la modification a fui dans l'original. Utiliser `copy.deepcopy(config)` pour les structures imbriquées.

<!-- takeaways -->

- `:=` assigne dans une expression.
- `match` vérifie la structure et extrait des valeurs.
- Les copies superficielles partagent les objets imbriqués.

<!-- unit: Noms, modules et scripts -->

<!-- goals -->

- Expliquer la règle LEGB, global et nonlocal.
- Distinguer modules et paquets et utiliser la garde `__main__`.

<!-- concept -->

Quand Python rencontre un nom, il le cherche à quatre endroits dans l'ordre : la fonction locale, les fonctions englobantes, le module, puis les built-ins. Assigner un nom dans une fonction le rend local sauf déclaration contraire, d'où la classique erreur « referenced before assignment ».

Le code s'organise en modules (fichiers) et paquets (répertoires de modules). La garde `__main__` permet à un fichier de servir à la fois de module importable et de script, sans exécuter le code du script à l'import.

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

#### Qu'est-ce que la règle LEGB ?

L'ordre dans lequel Python résout les noms : Local, portées des fonctions englobantes (Enclosing), Global (module), Built-in (intégrés).

#### Que font `global` et `nonlocal` ?

`global x` fait que les affectations dans une fonction réaffectent le `x` du module. `nonlocal x` réaffecte le `x` de la portée de fonction englobante la plus proche, ce qui est nécessaire pour modifier une variable de closure.

#### Quelle est la différence entre un module et un package ?

Un module est un fichier `.py` unique. Un package est un répertoire de modules, en général avec un `__init__.py`, importé avec des noms pointés.

#### Que fait `if __name__ == "__main__":` ?

Son bloc ne s'exécute que lorsque le fichier est lancé comme script, pas lorsqu'il est importé comme module. Il sert aux points d'entrée en ligne de commande.

#### Comment Python trouve-t-il un module lors d'un import ?

Il consulte d'abord `sys.modules` : un module déjà importé est réutilisé, si bien que son code de premier niveau ne s'exécute qu'une fois par processus. Sinon, il cherche dans les répertoires de `sys.path` : celui du script (ou le répertoire courant), `PYTHONPATH`, la bibliothèque standard et site-packages. Un fichier local nommé `json.py` ou `pandas.py` masque le vrai module, et depuis 3.13 le message d'erreur le signale.

#### Que sont les imports paresseux (lazy imports) ?

Python 3.15 ajoute `lazy import json` et `lazy from pathlib import Path` (PEP 810) : le module n'est chargé qu'à la première utilisation du nom, ce qui raccourcit le démarrage des outils en ligne de commande et des grosses applications. `lazy` n'est autorisé qu'au niveau du module, pas dans une fonction, une classe ou un bloc `try`. Dans les versions antérieures, on contourne le problème en important dans la fonction qui a besoin du module.

<!-- challenge -->

Importer un module utilitaire dans un test lance un chargement de données de 10 minutes. Pourquoi, et comment corriger ?

<!-- solution -->

Le module lance son chargement au niveau supérieur, exécuté à l'import. Le déplacer dans une fonction `main()` appelée sous `if __name__ == "__main__":`.

<!-- takeaways -->

- Résolution des noms : Local, Enclosing, Global, Built-in.
- Une assignation rend un nom local sauf déclaration.
- Protégez le code de script avec `__main__`.

### Chaînes, collections et compréhensions

<!-- unit: Chaînes et octets -->

<!-- goals -->

- Formater, découper et construire des chaînes efficacement.
- Distinguer texte et octets et résoudre des problèmes classiques sur les chaînes.

<!-- concept -->

Les chaînes sont des séquences immuables de caractères Unicode. L'immuabilité les rend sûres à partager et utilisables comme clés de dict, mais chaque modification crée une nouvelle chaîne : construire un long texte par concaténations répétées est lent, et l'idiome est de joindre une liste.

Le texte devient des octets quand il quitte le programme, par fichiers ou réseau : l'encodage est donc explicite. Le slicing, avec sa borne de fin exclue et ses indices négatifs, résout beaucoup de problèmes d'entretien en une ligne.

<!-- example -->

```python
name, total = "Ana", 1234.5
print(f"{name:<6}|{total:>10,.2f}|")     # Ana   |  1,234.50|
parts = [f"{i}" for i in range(5)]
print(",".join(parts))                   # efficient building
data = "café".encode("utf-8")            # b'caf\xc3\xa9'
print("racecar"[::-1])                   # reverse with a slice
```

#### Comment fonctionnent les f-strings ?

On préfixe une chaîne par `f` et on met des expressions entre accolades, avec des spécifications de format facultatives :

```python
total = 1234.5
print(f"Total: {total:,.2f} EUR, items: {len(items)}")   # Total: 1,234.50 EUR
print(f"{total=}")                                         # total=1234.5 (débogage)
```

#### Que sont les chaînes de gabarit (t-strings) ?

Python 3.14 a ajouté les littéraux `t"..."` (PEP 750). Ils ressemblent aux f-strings mais produisent un objet `string.templatelib.Template`, pas un `str` : les parties fixes et les valeurs interpolées restent séparées, si bien qu'une bibliothèque peut échapper ou paramétrer les valeurs avant de les combiner, par exemple pour construire du SQL ou du HTML sûrs.

```python
name = "O'Brien"
query = t"SELECT * FROM users WHERE name = {name}"
query.strings   # ('SELECT * FROM users WHERE name = ', '')
query.values    # ("O'Brien",)
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

<!-- challenge -->

Une boucle construit un rapport de 50 Mo avec `report += line` et prend plusieurs minutes. Que changez-vous ?

<!-- solution -->

Accumuler les lignes dans une liste et faire `"".join(lines)` une fois à la fin (ou écrire les lignes directement dans un fichier). Chaque `+=` recopie toute la chaîne qui grandit.

<!-- takeaways -->

- Les chaînes sont immuables ; joignez au lieu de concaténer.
- Encodez explicitement le texte en octets.
- Slices : `[start:stop:step]`, stop exclu.

<!-- unit: Compréhensions et outils d'itération -->

<!-- goals -->

- Écrire des compréhensions de listes, de dicts et d'ensembles.
- Choisir les expressions génératrices et utiliser zip et enumerate.

<!-- concept -->

Les compréhensions construisent des collections à partir d'itérables en une expression lisible, avec filtre optionnel. Elles existent pour listes, dicts et ensembles. Remplacer les crochets par des parenthèses donne une expression génératrice, qui produit les éléments paresseusement au lieu de tout construire en mémoire, idéal quand on ne parcourt qu'une fois.

Deux outils les accompagnent naturellement : `enumerate` donne les positions sans compteur manuel, et `zip` parcourt plusieurs séquences ensemble.

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

#### Quelle est la différence entre une compréhension de liste et une expression génératrice ?

Une compréhension de liste construit toute la liste en mémoire. Une expression génératrice (entre parenthèses) produit les éléments paresseusement, un par un : `sum(x * x for x in range(10**8))` utilise une mémoire constante.

#### Comment un dict Python est-il implémenté, et quelles sont ses complexités ?

Comme une table de hachage : recherche, insertion et suppression sont en O(1) en moyenne. Depuis Python 3.7, les dictionnaires conservent l'ordre d'insertion.

#### Quelle est la complexité des opérations courantes sur les listes ?

L'accès par indice et `append` sont en O(1) (amorti pour append), `insert(0, x)` et `pop(0)` en O(n), `x in list` en O(n), le tri en O(n log n). Utilisez `collections.deque` pour des opérations rapides aux deux extrémités et des ensembles pour les tests d'appartenance.

#### Que fait `dict.get()`, et en quoi diffère-t-il de `dict[key]` ?

`d[key]` lève `KeyError` si la clé est absente. `d.get(key, default)` renvoie alors `default` (ou `None`).

#### Comment aplatir une liste de listes dans une compréhension ?

`[x for row in rows for x in row]`, avec les clauses `for` dans le même ordre que des boucles imbriquées. Python 3.15 ajoute le dépaquetage dans les compréhensions (PEP 798) : `[*row for row in rows]` fait la même chose, et `{**d for d in dicts}` fusionne une liste de dicts, les dernières clés l'emportant.

<!-- challenge -->

`sum([row["amount"] for row in read_rows(path)])` manque de mémoire sur un fichier de 40 Go. Quelle est la correction d'un seul caractère, et pourquoi ?

<!-- solution -->

Supprimer les crochets : `sum(row["amount"] for row in read_rows(path))`. L'expression génératrice produit une valeur à la fois au lieu de construire une liste complète.

<!-- takeaways -->

- Les compréhensions construisent des collections de façon concise.
- Les expressions génératrices sont paresseuses et légères en mémoire.
- `enumerate` et `zip` remplacent l'indexation manuelle.

<!-- unit: Dicts et listes -->

<!-- goals -->

- Expliquer les caractéristiques de performance des dicts et des listes.
- Utiliser get, la fusion de dicts, les opérations ensemblistes et la déduplication qui préserve l'ordre.

<!-- concept -->

Choisir le bon conteneur est la principale décision de performance en Python courant. Dicts et ensembles sont des tables de hachage : appartenance et recherche se font en temps constant ; les listes sont des tableaux, rapides en fin mais lentes à parcourir ou à modifier en tête. Beaucoup de boucles lentes deviennent rapides en remplaçant une recherche dans une liste par un ensemble ou un dict.

Les dicts conservent aussi l'ordre d'insertion, ce qui simplifie la déduplication qui préserve l'ordre et les problèmes « dernier par clé ».

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

#### Qu'est-ce que `frozendict` ?

Un mapping immuable intégré, ajouté dans Python 3.15 (PEP 814). Il ne peut plus changer après sa création et il est hachable quand ses clés et valeurs le sont : il peut servir de clé de dict, d'élément de set ou de valeur par défaut sûre. Ce n'est pas une sous-classe de `dict`. Dans les versions antérieures, `types.MappingProxyType` offre une vue en lecture seule d'un dict.

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

<!-- challenge -->

Un job vérifie `if customer_id in processed_ids` où `processed_ids` est une liste de 2 millions d'ID, et cela prend des heures. Que changez-vous ?

<!-- solution -->

Faire de `processed_ids` un ensemble : l'appartenance passe en O(1) au lieu de parcourir la liste, et les heures deviennent des secondes.

<!-- takeaways -->

- Dicts et ensembles offrent des recherches en O(1).
- Les listes sont lentes à parcourir et à modifier en tête.
- Les dicts conservent l'ordre d'insertion.

<!-- unit: Le module collections -->

<!-- goals -->

- Utiliser defaultdict, Counter, namedtuple et deque.
- Résoudre avec eux des problèmes de comptage, de regroupement et de pile.

<!-- concept -->

Le module `collections` fournit des motifs qu'on écrirait sinon à la main. `defaultdict` crée automatiquement les valeurs manquantes, parfait pour regrouper. `Counter` compte et classe. `namedtuple` donne aux tuples des noms de champs lisibles. `deque` ajoute et retire aux deux extrémités en temps constant : file, pile ou fenêtre glissante.

Beaucoup de problèmes d'entretien sont l'un de ces motifs déguisé.

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

#### Comment supprimer les doublons d'une liste en gardant l'ordre ?

```python
unique = list(dict.fromkeys(items))
```

#### Quelles sont les opérations sur les ensembles ?

Union `a | b`, intersection `a & b`, différence `a - b`, différence symétrique `a ^ b` et test d'inclusion `a <= b`. Les tests d'appartenance sont en O(1) en moyenne.

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

<!-- challenge -->

Une fonction garde les 1 000 dernières lignes de log avec `lines.append(x)` suivi de `lines.pop(0)`, et ralentit quand le trafic augmente. Qu'utilisez-vous ?

<!-- solution -->

Un `deque(maxlen=1000)` : l'ajout supprime automatiquement l'élément le plus ancien en O(1), alors que `list.pop(0)` décale tous les éléments.

<!-- takeaways -->

- `defaultdict` regroupe ; `Counter` compte.
- `deque` est en O(1) aux deux extrémités.
- Beaucoup de problèmes sont ces motifs déguisés.

<!-- unit: Tri -->

<!-- goals -->

- Trier listes et enregistrements selon une ou plusieurs clés.
- Choisir entre sort et sorted et appliquer le tri aux problèmes d'intervalles.

<!-- concept -->

Python trie avec une fonction clé : on lui dit quoi comparer, il gère le reste, de façon stable et efficace. Des tuples comme clés trient sur plusieurs champs à la fois ; nier un nombre inverse un champ. `sort()` modifie une liste sur place et renvoie `None`, un bug fréquent quand on l'assigne ; `sorted()` renvoie une nouvelle liste depuis n'importe quel itérable.

Le tri est aussi une étape de résolution : une fois les intervalles triés par début, les chevauchements deviennent des voisins.

<!-- example -->

```python
from operator import itemgetter
rows = [{"country": "CO", "revenue": 50}, {"country": "AR", "revenue": 80}, {"country": "CO", "revenue": 90}]
rows.sort(key=lambda r: (r["country"], -r["revenue"]))     # country asc, revenue desc
top = sorted(rows, key=itemgetter("revenue"), reverse=True)[:2]
```

#### Que sont les fonctions de première classe ?

Les fonctions sont des objets : on peut les affecter à des variables, les ranger dans des structures de données, les passer en argument et les renvoyer depuis d'autres fonctions.

#### Que sont `map`, `filter` et `functools.reduce` ?

`map(f, xs)` applique `f` à chaque élément, `filter(pred, xs)` garde les éléments pour lesquels `pred` est vrai (tous deux paresseux), et `reduce(f, xs, init)` réduit une séquence à une seule valeur. Les compréhensions sont en général plus lisibles que `map` et `filter`.

#### Que fait `functools.partial` ?

Elle crée une nouvelle fonction dont certains arguments sont fixés : `parse_fr = partial(parse_date, fmt="%d/%m/%Y")`.

<!-- challenge -->

`result = rows.sort(key=...)` puis `result[0]` échoue avec `TypeError: 'NoneType' object is not subscriptable`. Pourquoi ?

<!-- solution -->

`list.sort()` trie sur place et renvoie `None`. Soit appeler `rows.sort(...)` puis utiliser `rows`, soit `result = sorted(rows, key=...)`.

<!-- takeaways -->

- Triez avec des fonctions clés ; des tuples pour plusieurs champs.
- `sort()` renvoie None ; `sorted()` renvoie une liste.
- Le tri ramène les chevauchements à des comparaisons de voisins.

<!-- stage: Écrire du Python -->

### Fonctions, portées et closures

<!-- unit: Paramètres et arguments -->

<!-- goals -->

- Utiliser *args, **kwargs et les paramètres keyword-only et positional-only.
- Éviter les valeurs par défaut mutables et renvoyer ou dépaqueter plusieurs valeurs.

<!-- concept -->

Les signatures de fonctions sont une interface, et Python offre un contrôle fin : collecter des arguments supplémentaires, imposer que certains soient nommés pour la lisibilité, ou que d'autres soient positionnels pour pouvoir les renommer plus tard. Le dépaquetage renvoie naturellement plusieurs valeurs.

Un piège attrape tout le monde une fois : les valeurs par défaut sont créées à la définition de la fonction, pas à l'appel, donc une valeur par défaut mutable est partagée par tous les appels.

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

<!-- challenge -->

`def add_item(item, basket=[])` renvoie des paniers contenant des articles d'appels précédents. Corrigez.

<!-- solution -->

Utiliser `basket=None` et créer la liste à l'intérieur : `if basket is None: basket = []`. La liste par défaut avait été créée une fois et partagée entre les appels.

<!-- takeaways -->

- `*args` et `**kwargs` collectent les arguments supplémentaires.
- `*` impose des mots-clés ; `/` impose des positions.
- Utilisez `None` au lieu de valeurs par défaut mutables.

<!-- unit: Les fonctions comme valeurs -->

<!-- goals -->

- Utiliser lambdas, fonctions d'ordre supérieur, map, filter, reduce et partial.
- Comprendre any, all et l'évaluation en court-circuit.

<!-- concept -->

Les fonctions sont des objets : on peut les passer, les renvoyer et les stocker comme n'importe quelle valeur. C'est ce qui rend possibles le tri par clé, les callbacks et les décorateurs. Les petites fonctions jetables peuvent être des lambdas ; l'application partielle fixe certains arguments pour construire des versions spécialisées.

Les opérateurs logiques partagent cette souplesse : `and` et `or` renvoient l'un de leurs opérandes plutôt qu'un booléen, et `any`/`all` s'arrêtent dès que la réponse est connue.

<!-- example -->

```python
from functools import partial, reduce
parse_bin = partial(int, base=2)                           # parse_bin("1010") == 10
total = reduce(lambda acc, x: acc + x, [1, 2, 3], 0)
has_errors = any(r["status"] == "error" for r in results)  # stops at the first error
name = user_input or "anonymous"                           # returns an operand
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

#### Quelle est la différence entre une classe et une instance ?

Une classe est un modèle qui définit attributs et méthodes. Une instance est un objet créé à partir d'elle, avec son propre état : `p = Point(1, 2)`.

<!-- challenge -->

`timeout = config.get("timeout") or 30` met 30 quand la config indique explicitement `0` (pas de timeout). Comment corriger ?

<!-- solution -->

`or` traite 0 comme faux. Tester explicitement l'absence de valeur : `timeout = config.get("timeout"); timeout = 30 if timeout is None else timeout`.

<!-- takeaways -->

- Les fonctions sont des valeurs qu'on passe et renvoie.
- `partial` fixe des arguments ; les lambdas tiennent en une ligne.
- `and`/`or` renvoient des opérandes et court-circuitent.

<!-- unit: Closures et portée -->

<!-- goals -->

- Écrire des closures et éviter le piège de la liaison tardive.
- Utiliser judicieusement récursion et mémoïsation.

<!-- concept -->

Une fonction définie dans une autre se souvient des variables qui l'entourent, même après le retour de la fonction externe. C'est une closure, le mécanisme derrière les décorateurs et les fonctions fabriques. Elle lit ces variables à l'appel, pas à la définition, ce qui surprend dans les boucles.

La récursion convient aux structures naturellement récursives, mais elle a une limite de profondeur et refait du travail. Mettre en cache les résultats par argument supprime les répétitions.

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

<!-- challenge -->

Une fonction récursive qui parcourt un JSON très imbriqué échoue avec `RecursionError` sur un fichier. Que faites-vous ?

<!-- solution -->

La réécrire de façon itérative avec une pile explicite (liste ou deque) des éléments à visiter, sans limite de profondeur ; augmenter la limite de récursion ne fait que retarder le plantage.

<!-- takeaways -->

- Les closures retiennent les variables englobantes.
- Elles lisent les variables à l'appel ; liez-les par des valeurs par défaut.
- La récursion a des limites ; le cache évite le travail répété.

<!-- unit: Documenter et typer les fonctions -->

<!-- goals -->

- Écrire docstrings et type hints, y compris pour les valeurs optionnelles.
- Distinguer fonctions et méthodes.

<!-- concept -->

La signature d'une fonction dit à l'appelant comment l'utiliser ; docstrings et type hints lui disent ce qu'elle signifie. Les hints ne sont pas imposés à l'exécution, mais éditeurs et vérificateurs de types s'en servent pour détecter les erreurs avant l'exécution, et ils documentent l'intention mieux que les noms seuls.

Les méthodes sont des fonctions attachées à des classes, l'instance étant passée automatiquement. Le savoir aide quand on passe des méthodes comme callbacks.

<!-- example -->

```python
def parse_amount(raw: str, default: float | None = None) -> float | None:
    """Parse '1.234,56' or '1234.56' into a float.

    Returns `default` when the value is empty or invalid.
    """
    ...
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

#### Quand les annotations sont-elles évaluées ?

Depuis Python 3.14 (PEP 649 et 749), les annotations des fonctions, classes et modules sont évaluées paresseusement, seulement quand quelque chose les lit. Les références vers des classes définies plus loin n'ont plus besoin de guillemets ni de `from __future__ import annotations`. Le nouveau module `annotationlib` permet de les inspecter, et `typing.get_type_hints()` fonctionne toujours.

<!-- challenge -->

Une fonction est annotée `-> float` mais renvoie `None` sur une mauvaise entrée, et les appelants plantent sur `None + 1`. En quoi les hints aident-ils à l'éviter ?

<!-- solution -->

L'annoter honnêtement `-> float | None` et lancer un vérificateur de types (mypy, pyright), qui signale alors les appelants qui utilisent le résultat sans gérer `None`.

<!-- takeaways -->

- Les docstrings expliquent le comportement ; les hints décrivent les types.
- Les hints ne sont pas imposés mais alimentent les vérificateurs.
- `X | None` marque une valeur optionnelle.

### Programmation orientée objet

<!-- unit: Classes et instances -->

<!-- goals -->

- Définir des classes avec __init__, attributs d'instance et de classe.
- Utiliser staticmethod, classmethod et property.

<!-- concept -->

Une classe regroupe des données et le comportement qui agit dessus. Les instances reçoivent leurs propres attributs dans `__init__`, tandis que les attributs de classe sont partagés par toutes les instances, utile pour des constantes et dangereux pour des données mutables.

Les décorateurs façonnent l'interface : les class methods servent de constructeurs alternatifs, les static methods regroupent des utilitaires, et les properties exposent des valeurs calculées ou de la validation derrière une simple syntaxe d'attribut.

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

<!-- challenge -->

Une classe définit `items = []` au niveau de la classe, et toutes les instances finissent par partager les mêmes articles. Corrigez.

<!-- solution -->

Créer la liste par instance dans `__init__` (`self.items = []`). Les attributs mutables au niveau de la classe sont partagés par toutes les instances.

<!-- takeaways -->

- Les attributs d'instance vont dans `__init__` ; ceux de classe sont partagés.
- Les classmethods sont des constructeurs alternatifs.
- Les properties cachent un calcul derrière un attribut.

<!-- unit: Héritage et composition -->

<!-- goals -->

- Utiliser l'héritage, super() et les classes de base abstraites.
- Expliquer le MRO et quand la composition vaut mieux.

<!-- concept -->

L'héritage permet à une classe de réutiliser et spécialiser le comportement d'une autre, `super()` appelant la version du parent. Avec l'héritage multiple, l'ordre de résolution des méthodes décide quelle implémentation l'emporte. Les classes de base abstraites définissent des méthodes que les sous-classes doivent implémenter.

Les hiérarchies profondes deviennent rigides, cependant. La composition, construire des objets à partir d'autres objets, donne souvent la même réutilisation avec moins de couplage : un pipeline qui a un lecteur et un écrivain se modifie plus facilement qu'un pipeline qui est un cas particulier des deux.

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

#### Qu'est-ce que la composition, et pourquoi la préfère-t-on souvent à l'héritage ?

Construire des objets à partir d'autres objets (« a un ») plutôt qu'étendre des classes (« est un »). Elle donne un couplage plus faible et évite les hiérarchies de classes profondes et fragiles.

#### Qu'est-ce que l'encapsulation en Python ?

Python n'a pas de membres privés. Par convention, `_name` est interne, et `__name` déclenche le name mangling (`_Class__name`) pour éviter les collisions dans les sous-classes.

#### Qu'est-ce qui rend un objet hachable ?

Un `__hash__` qui ne change pas pendant sa durée de vie et un `__eq__` cohérent avec lui (des objets égaux doivent avoir le même hash). Définir `__eq__` sans `__hash__` rend une classe non hachable.

#### Qu'est-ce qu'une métaclasse ?

La classe d'une classe (par défaut `type`), qui contrôle la création des classes. Rarement nécessaire : les décorateurs de classe et `__init_subclass__` couvrent la plupart des besoins.

<!-- challenge -->

Une équipe a `CsvS3Pipeline`, `CsvLocalPipeline`, `JsonS3Pipeline`, `JsonLocalPipeline`… et chaque nouveau format ou destination double le nombre de classes. Comment restructurer ?

<!-- solution -->

Composer : un `Pipeline` qui prend en paramètres un `Reader` (CSV, JSON) et un `Sink` (S3, local). Chaque nouveau format ou destination ajoute une classe au lieu de multiplier les combinaisons.

<!-- takeaways -->

- `super()` appelle l'implémentation du parent.
- Les ABC définissent les méthodes obligatoires.
- Préférez la composition aux hiérarchies profondes.

<!-- unit: Le data model et les méthodes dunder -->

<!-- goals -->

- Implémenter des méthodes dunder comme __repr__, __eq__, __hash__ et __call__.
- Utiliser les dataclasses et __slots__.

<!-- concept -->

La syntaxe de Python repose sur des méthodes spéciales. Définir `__repr__` donne une sortie de débogage lisible ; `__eq__` et `__hash__` décident de l'égalité et de la possibilité d'utiliser des objets comme clés de dict ; `__call__` fait se comporter les instances comme des fonctions. Les implémenter rend vos classes aussi naturelles que les types intégrés.

Les dataclasses génèrent les plus courantes à partir des déclarations de champs, et `__slots__` réduit la mémoire des classes à millions d'instances.

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

#### Qu'est-ce que `__call__` ?

Une méthode qui rend les instances appelables comme des fonctions, utile pour des objets-fonctions configurables.

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

#### Que fait `copy.replace()` ?

Ajoutée dans Python 3.13, elle renvoie une copie d'un objet avec certains champs modifiés : `copy.replace(order, status="paid")`. Elle fonctionne avec les dataclasses (comme `dataclasses.replace`), les named tuples et les objets `datetime`, et toute classe peut la prendre en charge en définissant `__replace__`. C'est la manière idiomatique de « modifier » des objets figés.

#### Qu'est-ce qu'`itertools`, et citez quelques fonctions utiles ?

Un module de briques rapides pour les itérateurs : `chain`, `islice`, `groupby`, `product`, `permutations`, `combinations`, `accumulate`, `count`, `cycle`, `tee`, `zip_longest` et `batched` (Python 3.12).

<!-- challenge -->

Des objets d'une dataclass mutable servent de clés de dict, puis un champ change, et les recherches ne les trouvent plus. Pourquoi, et comment corriger ?

<!-- solution -->

Le hash dépend des champs ; changer un champ change le hash, et le dict cherche au mauvais endroit. Utiliser `frozen=True` pour les objets clés (ou ne pas les modifier).

<!-- takeaways -->

- Les méthodes dunder branchent les classes sur la syntaxe.
- Un objet hashable ne doit pas changer de hash.
- Les dataclasses génèrent le code répétitif.

<!-- unit: Interfaces par comportement -->

<!-- goals -->

- Appliquer le duck typing et les Protocols.
- Comprendre les conventions d'encapsulation de Python et les métaclasses.

<!-- concept -->

Python s'intéresse à ce qu'un objet sait faire, pas à ce qu'il est. Tout objet doté d'une méthode `read` peut être traité comme un fichier : c'est le duck typing. Les Protocols permettent aux vérificateurs de types de le contrôler structurellement, sans héritage.

La confidentialité est affaire de convention : un tiret bas initial signifie « interne », deux tirets bas transforment le nom pour éviter les collisions. Les métaclasses, qui personnalisent la création des classes elles-mêmes, existent mais sont rarement le bon outil dans du code applicatif.

<!-- example -->

```python
from typing import Protocol

class SupportsRead(Protocol):
    def read(self, n: int = -1) -> bytes: ...

def checksum(src: SupportsRead) -> str:     # works with files, BytesIO, S3 streams...
    import hashlib
    return hashlib.sha256(src.read()).hexdigest()
```

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

#### Qu'est-ce qu'un descripteur ?

Un objet placé en attribut de classe qui définit `__get__` (et éventuellement `__set__` ou `__delete__`), et contrôle ainsi ce qui se passe quand on accède à cet attribut depuis les instances. Les propriétés, les méthodes, `classmethod`, `staticmethod` et `__slots__` reposent tous sur des descripteurs ; on écrit les siens pour valider des champs de façon réutilisable.

<!-- challenge -->

Une fonction exige `isinstance(f, io.FileIO)` et rejette des flux S3 et des objets `BytesIO` qui fonctionneraient très bien. Comment les accepter ?

<!-- solution -->

Supprimer la vérification `isinstance` et se fier au comportement (appeler `read()`), en typant le paramètre comme un `Protocol` avec `read` : tout objet lisible est accepté et les vérificateurs le contrôlent toujours.

<!-- takeaways -->

- Duck typing : le comportement prime sur le type.
- Les Protocols vérifient le comportement structurellement.
- Les noms à tiret bas sont internes par convention.

### Itérateurs, générateurs, décorateurs et gestionnaires de contexte

<!-- unit: Itérateurs et générateurs -->

<!-- goals -->

- Distinguer itérables et itérateurs, et écrire des générateurs.
- Rendre des classes itérables et déléguer avec yield from.

<!-- concept -->

Tout ce qu'on peut parcourir est un itérable ; le parcourir lui demande un itérateur, qui livre les éléments un par un jusqu'à épuisement. Les générateurs sont la façon simple d'écrire des itérateurs : une fonction avec `yield` se met en pause après chaque élément et reprend à la demande suivante.

Comme les itérateurs se consomment au fil du parcours, un générateur ne se parcourt qu'une fois. C'est le prix de leur avantage : ils produisent des séquences infinies ou énormes avec presque aucune mémoire.

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

<!-- challenge -->

Une fonction passe un générateur à deux consommateurs : l'un valide les lignes, l'autre les charge. Le chargeur ne reçoit rien. Pourquoi, et quelles sont deux corrections ?

<!-- solution -->

Le validateur a épuisé le générateur. Soit appeler deux fois la fonction génératrice (itérateurs neufs), soit valider et charger en une seule passe ; `itertools.tee` fonctionne mais met des données en mémoire tampon.

<!-- takeaways -->

- Les itérables produisent des itérateurs ; les itérateurs se consomment.
- Les générateurs se mettent en pause à `yield` et consomment peu.
- Un générateur ne se parcourt qu'une fois.

<!-- unit: Pipelines paresseux avec itertools -->

<!-- goals -->

- Construire des pipelines légers en mémoire avec générateurs et itertools.
- Utiliser correctement groupby, islice et batched.

<!-- concept -->

Chaîner des générateurs crée des pipelines qui traitent les données en flux : lire une ligne, l'analyser, la filtrer, l'écrire, sans jamais garder tout le fichier. `itertools` fournit les raccords : concaténer, découper, regrouper, faire des lots et accumuler sur n'importe quel itérateur.

Un raccord surprend : `groupby` ne regroupe que les éléments consécutifs de même clé, donc l'entrée doit déjà être triée par cette clé.

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

#### Comment lire seulement les n premiers éléments d'un itérateur ?

`itertools.islice(it, n)`, qui fonctionne avec n'importe quel itérateur, y compris infini.

#### Comment découper un itérable en lots de taille fixe ?

`itertools.batched(iterable, n)` en Python 3.12+, ou avec `islice` dans une boucle pour les versions antérieures.

#### Qu'est-ce qu'`itertools` ? Citez quelques fonctions utiles.

Un module de briques rapides pour itérateurs : `chain`, `islice`, `groupby`, `product`, `permutations`, `combinations`, `accumulate`, `count`, `cycle`, `tee`, `zip_longest`, `pairwise` (3.10, paires consécutives) et `batched` (3.12 ; depuis 3.13, `strict=True` refuse un dernier lot incomplet).

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

<!-- challenge -->

`groupby(rows, key=lambda r: r["country"])` renvoie « CO » trois fois en groupes séparés. Qu'est-ce qui ne va pas ?

<!-- solution -->

`groupby` ne regroupe que les éléments consécutifs ; les lignes ne sont pas triées par pays. Trier d'abord (`sorted(rows, key=...)`) ou utiliser un `defaultdict(list)` pour regrouper sans trier.

<!-- takeaways -->

- Les pipelines de générateurs traitent en mémoire constante.
- `itertools` fournit découpage, lots et regroupement.
- `groupby` exige une entrée triée par la clé.

<!-- unit: Décorateurs -->

<!-- goals -->

- Écrire des décorateurs qui préservent les métadonnées des fonctions.
- Écrire des décorateurs qui prennent des arguments.

<!-- concept -->

Un décorateur enveloppe une fonction pour ajouter un comportement autour, comme la mesure du temps, les relances, le cache ou la journalisation, sans modifier son code. La syntaxe `@` est un raccourci pour remplacer la fonction par sa version enveloppée.

Deux détails rendent les décorateurs prêts pour la production : copier le nom et la docstring de la fonction d'origine avec `functools.wraps`, et un niveau d'imbrication supplémentaire quand le décorateur lui-même a besoin de paramètres.

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

<!-- challenge -->

Après avoir décoré des fonctions avec un `@timed` maison, toutes apparaissent sous le nom « wrapper » dans les journaux et tracebacks. Que manque-t-il ?

<!-- solution -->

`@functools.wraps(func)` sur le wrapper interne, qui copie le nom, la docstring et les autres métadonnées de la fonction d'origine.

<!-- takeaways -->

- Les décorateurs enveloppent des fonctions pour ajouter un comportement.
- Utilisez toujours `functools.wraps`.
- Les décorateurs paramétrés ajoutent un niveau d'imbrication.

<!-- unit: Context managers -->

<!-- goals -->

- Utiliser et écrire des context managers, y compris avec contextlib.
- Maîtriser la gestion des exceptions dans __exit__ et gérer de nombreuses ressources avec ExitStack.

<!-- concept -->

Fichiers, connexions, verrous et transactions doivent être nettoyés même en cas d'erreur. Les context managers le garantissent : la mise en place s'exécute à l'entrée du bloc `with`, le nettoyage à la sortie, quelle que soit la façon d'en sortir.

`contextlib` transforme un générateur en context manager en quelques lignes. `__exit__` décide si une exception se propage, et `ExitStack` gère un nombre variable de ressources à la fois.

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

<!-- challenge -->

Le `__exit__` d'un context manager maison renvoie `True` « par sécurité », et les erreurs dans les blocs `with` disparaissent. Que se passe-t-il ?

<!-- solution -->

Renvoyer une valeur vraie depuis `__exit__` supprime l'exception. Renvoyer `None`/`False` (ou relancer) pour que les erreurs se propagent après le nettoyage.

<!-- takeaways -->

- Les context managers garantissent le nettoyage.
- `@contextmanager` les construit à partir de générateurs.
- Un `__exit__` qui renvoie vrai avale les exceptions.

<!-- stage: Travailler avec le monde extérieur -->

### Erreurs, fichiers et bibliothèque standard

<!-- unit: Exceptions -->

<!-- goals -->

- Gérer, lever et chaîner correctement les exceptions.
- Définir des exceptions personnalisées et choisir entre EAFP et LBYL.

<!-- concept -->

Une bonne gestion d'erreurs n'attrape que ce qu'elle sait traiter et laisse remonter le reste. Des clauses `except` précises, le nettoyage dans `finally` et un `else` pour le code qui ne doit s'exécuter qu'en cas de succès gardent l'intention claire. Un `except` nu cache les bugs et bloque même Ctrl+C.

Les exceptions personnalisées offrent aux appelants des types significatifs à attraper, le chaînage garde la cause d'origine dans les tracebacks, et les exception groups signalent plusieurs échecs à la fois.

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

#### Comment intercepter plusieurs types d'exception dans une seule clause ?

En les listant dans un tuple : `except (ConnectionError, TimeoutError) as exc:`. Depuis Python 3.14 (PEP 758), on peut omettre les parenthèses quand il n'y a pas de clause `as` : `except ConnectionError, TimeoutError:`. Entre plusieurs clauses, le premier `except` qui correspond l'emporte : placez les exceptions spécifiques avant les générales.

#### Comment calculer l'empreinte de données ou de fichiers en Python ?

Avec `hashlib` : `hashlib.sha256(data).hexdigest()`. Pour les fichiers, lisez par blocs et appelez `update()` pour garder une mémoire constante.

<!-- challenge -->

Un chargeur enveloppe tout dans `try: ... except: pass`, et des données manquantes passent inaperçues pendant des semaines. Comment le réécrire ?

<!-- solution -->

N'attraper que les erreurs attendues (par exemple `ValueError` pour les enregistrements défectueux), les journaliser avec contexte et les compter, et laisser les exceptions inattendues se propager pour que le job échoue visiblement.

<!-- takeaways -->

- N'attrapez que des exceptions précises.
- Chaînez avec `raise ... from exc`.
- Des types d'exception personnalisés aident les appelants.

<!-- unit: Fichiers et chemins -->

<!-- goals -->

- Lire de gros fichiers en sécurité avec `with` et l'itération ligne par ligne.
- Utiliser pathlib, la compression et les fichiers temporaires.

<!-- concept -->

Les fichiers sont l'entrée la plus courante du travail sur les données, et deux habitudes évitent la plupart des problèmes. Les ouvrir avec `with`, pour qu'ils soient fermés même en cas d'erreur. Les parcourir ligne par ligne, pour que la mémoire reste constante quelle que soit la taille.

`pathlib` fait des chemins des objets qu'on peut joindre, inspecter et filtrer avec glob ; les modules de compression lisent et écrivent des fichiers compressés comme s'ils étaient bruts ; et les fichiers temporaires se nettoient seuls.

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

#### À quoi sert `tempfile` ?

À créer des fichiers et des répertoires temporaires nettoyés automatiquement : `with tempfile.TemporaryDirectory() as tmp: ...`.

#### Comment compresser ou décompresser des fichiers en Python ?

Avec les modules `gzip`, `bz2`, `lzma` et `zipfile`. `gzip.open(path, "rt", encoding="utf-8")` lit un fichier texte compressé ligne par ligne.

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

<!-- challenge -->

Un script appelle `open(path).read().splitlines()` sur des journaux de 30 Go et plante. Réécrivez la partie lecture.

<!-- solution -->

`with open(path, encoding="utf-8") as f: for line in f: process(line)`, qui lit une ligne à la fois et ferme le fichier de façon fiable.

<!-- takeaways -->

- Ouvrez les fichiers avec `with`.
- Itérez par ligne pour garder une mémoire constante.
- `pathlib` pour les chemins ; `gzip` pour les fichiers compressés.

<!-- unit: Formats de données et dates -->

<!-- goals -->

- Lire et écrire du CSV et du JSON avec la bibliothèque standard.
- Analyser des dates et utiliser des datetimes avec fuseau horaire.

<!-- concept -->

La bibliothèque standard gère les formats courants. Le module `csv` traite guillemets et délimiteurs qu'un découpage naïf gère mal ; `json` convertit entre texte et dicts, avec des points d'accroche pour les types qu'il ne connaît pas.

Les dates demandent du soin : analyser avec des formats explicites, et garder des heures conscientes de leur fuseau, de préférence en UTC, car mélanger datetimes naïfs et conscients provoque des erreurs et des décalages silencieux.

<!-- example -->

```python
import csv, json
from datetime import datetime, timezone

with open("in.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))
ts = datetime.strptime("17/10/2026 09:41", "%d/%m/%Y %H:%M").replace(tzinfo=timezone.utc)
print(json.dumps({"rows": len(rows), "loaded_at": ts}, default=str))
```

#### Qu'est-ce qu'une condition de concurrence, et comment l'éviter avec des threads ?

Deux threads qui accèdent à des données partagées et produisent un résultat qui dépend du hasard de l'ordonnancement. On l'évite avec des verrous (`threading.Lock`), des files thread-safe (`queue.Queue`) ou en évitant l'état mutable partagé.

#### Comment limiter la concurrence quand on appelle une API à débit limité ?

En bornant la taille du pool de workers, ou avec `asyncio.Semaphore`, et en ajoutant des nouvelles tentatives avec temporisation croissante sur les réponses 429.

#### Comment profiler du code Python ?

`cProfile` (`python -m cProfile -s cumtime script.py`) pour le temps par fonction, `timeit` pour de petits extraits, `tracemalloc` pour la mémoire, et des profileurs par échantillonnage comme py-spy pour un processus en cours.

#### Qu'est-ce qui rend vraiment le code Python plus rapide ?

De meilleurs algorithmes et structures de données (ensembles et dictionnaires pour les recherches), les fonctions intégrées et les compréhensions plutôt que des boucles manuelles, des bibliothèques vectorisées (NumPy, pandas, Polars) pour les calculs en masse, éviter les calculs répétés (cache), et déporter le travail lourd vers du code compilé ou un moteur distribué.

#### Pourquoi `datetime.utcnow()` est-il déprécié ?

Il renvoie un datetime naïf qui a seulement l'air d'être en UTC : du code qui le traite ensuite comme une heure locale décale les valeurs sans prévenir. Il est déprécié depuis Python 3.12 (avec `utcfromtimestamp()`) : utilisez `datetime.now(timezone.utc)` ou `datetime.fromtimestamp(ts, tz=timezone.utc)`, qui renvoient des datetimes conscients du fuseau. `datetime.UTC` (3.11) est un alias plus court de `timezone.utc`.

#### Pourquoi parcourir un DataFrame pandas ligne par ligne est-il lent ?

Chaque ligne devient un objet Python et le travail se fait dans l'interpréteur. Les opérations vectorisées s'exécutent en code C optimisé sur des colonnes entières à la fois.

<!-- challenge -->

Un script découpe des lignes CSV avec `line.split(",")`, et certaines lignes ont trop de champs. Pourquoi, et comment corriger ?

<!-- solution -->

Des champs comme `"Pérez, Ana"` contiennent des virgules entre guillemets. Utiliser `csv.reader`/`DictReader`, qui gèrent correctement guillemets et échappements.

<!-- takeaways -->

- Utilisez `csv` au lieu de découper les lignes.
- `json` gère texte ↔ dicts ; `default=` pour les types personnalisés.
- Gardez les datetimes avec fuseau, idéalement en UTC.

<!-- unit: Modules standard utiles -->

<!-- goals -->

- Journaliser correctement et construire des interfaces en ligne de commande.
- Utiliser expressions régulières, sous-processus et hachage.

<!-- concept -->

« Piles incluses » : la plupart des utilitaires sont déjà là. `logging` offre niveaux, formatage et handlers, pour envoyer les messages vers la console en développement et vers des fichiers ou collecteurs en production. `argparse` transforme les scripts en véritables outils en ligne de commande.

Les expressions régulières extraient la structure du texte ; `subprocess` exécute des commandes externes en sécurité sans shell ; `hashlib` calcule des sommes de contrôle de fichiers et des clés pseudonymisées.

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

#### À quoi sert le module `enum` ?

À définir un ensemble fixe de constantes nommées, mieux que des littéraux de texte éparpillés dans le code : les membres sont typés, itérables et comparés par identité. Les membres de `StrEnum` (3.11) sont aussi des chaînes, pratiques pour le JSON et les bases de données ; `IntEnum` et `Flag` couvrent les entiers et les drapeaux binaires.

```python
from enum import StrEnum

class Status(StrEnum):
    PENDING = "pending"
    DONE = "done"

Status("done") is Status.DONE   # True
```

<!-- challenge -->

Un script exécute `subprocess.run(f"rm -rf {folder}", shell=True)` avec un nom de dossier saisi par l'utilisateur. Quel est le risque, et la correction ?

<!-- solution -->

L'injection shell : un nom piégé pourrait exécuter des commandes arbitraires. Passer une liste d'arguments sans `shell=True`, valider le chemin, et préférer `shutil.rmtree` à un appel au shell.

<!-- takeaways -->

- Utilisez `logging` avec des loggers par module et un formatage paresseux.
- `argparse` construit des interfaces en ligne de commande.
- Lancez les sous-processus avec des listes d'arguments, sans shell.

### Concurrence et performances

<!-- unit: Le GIL et les modèles de concurrence -->

<!-- goals -->

- Expliquer le GIL et comparer threading, multiprocessing et asyncio.
- Utiliser concurrent.futures, éviter conditions de course et pièges du pickling, et connaître la version free-threaded et les sous-interpréteurs.

<!-- concept -->

Dans la version standard de CPython, un seul thread exécute du bytecode Python à la fois. Les threads aident tout de même quand le travail attend réseau ou disque, car l'attente libère le verrou ; le travail gourmand en CPU exige des processus, chacun avec son interpréteur. Asyncio gère de nombreuses attentes dans un seul thread.

Chaque modèle a ses pièges : des threads qui partagent des données ont besoin de verrous pour éviter les conditions de course ; les processus exigent des fonctions et données sérialisables par pickle ; les threads daemon meurent brutalement à la sortie.

<!-- example -->

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=16) as pool:          # I/O-bound: downloads
    pages = list(pool.map(fetch, urls))

def heavy(chunk): ...                                     # module-level: picklable
with ProcessPoolExecutor() as pool:                       # CPU-bound: parsing
    results = list(pool.map(heavy, chunks))
```

#### Qu'est-ce que le GIL ?

Le Global Interpreter Lock de CPython ne laisse qu'un seul thread exécuter du bytecode Python à la fois. Les threads restent utiles pour le travail limité par les E/S, car le GIL est relâché pendant l'attente, mais pas pour du code Python pur limité par le CPU. Une version free-threaded sans GIL existe depuis 3.13 et est officiellement prise en charge depuis 3.14, mais la version par défaut garde le GIL.

#### Qu'est-ce que Python free-threaded ?

Une version de CPython sans GIL (PEP 703), où les threads exécutent du code Python en parallèle sur plusieurs cœurs. Expérimentale en 3.13, elle est officiellement prise en charge depuis 3.14 (PEP 779) et s'installe comme un interpréteur distinct, par exemple `python3.14t`. Le code monothread y tourne un peu plus lentement, et les extensions C doivent être compilées pour elle ; sinon, les importer réactive le GIL.

#### Que sont les sous-interpréteurs ?

Plusieurs interpréteurs isolés dans un même processus, chacun avec son propre GIL, exposés par le module `concurrent.interpreters` de Python 3.14 (PEP 734) et par `InterpreterPoolExecutor` dans `concurrent.futures`. Ils offrent du parallélisme CPU avec moins de surcoût que des processus, mais les objets ne sont pas partagés : les données passent par des files ou sont copiées.

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

#### Quelle méthode de démarrage multiprocessing utilise-t-il ?

`spawn` sous Windows et macOS, et depuis Python 3.14 `forkserver` sous Linux et les autres Unix (c'était `fork` auparavant). Dans les deux cas, les workers partent d'un interpréteur neuf : fonctions et arguments doivent être sérialisables par pickle et le script a besoin de la garde `if __name__ == "__main__":`. Le code qui dépendait de variables globales héritées peut demander `multiprocessing.get_context("fork")` explicitement.

#### Qu'est-ce qu'un environnement virtuel, et pourquoi en utiliser un ?

Une installation Python isolée avec ses propres paquets (`python -m venv .venv`), pour que chaque projet ait ses propres versions de dépendances sans casser le Python du système ni les autres projets.

<!-- challenge -->

Une équipe accélère un job d'analyse gourmand en CPU avec 16 threads et ne constate aucun gain. Pourquoi, et que suggérez-vous ?

<!-- solution -->

Le GIL ne laisse qu'un thread exécuter du code Python à la fois, donc les threads limités par le CPU ne s'exécutent pas en parallèle. Utiliser un `ProcessPoolExecutor` (ou une bibliothèque vectorisée) pour exploiter plusieurs cœurs.

<!-- takeaways -->

- Threads pour les E/S ; processus pour le CPU.
- Les données partagées entre threads exigent des verrous.
- Les pools de processus exigent des fonctions sérialisables au niveau module.

<!-- unit: asyncio -->

<!-- goals -->

- Expliquer coroutines, event loop et asyncio.run.
- Limiter la concurrence, fixer des timeouts et gérer la backpressure.

<!-- concept -->

Le code asynchrone exécute de nombreuses tâches d'E/S dans un seul thread. Les coroutines se mettent en pause à chaque `await`, laissant l'event loop en exécuter d'autres pendant l'attente. Appeler une fonction async ne fait que créer une coroutine ; la boucle doit l'exécuter, ce que fait `asyncio.run` au niveau supérieur.

La concurrence a besoin de limites. Les API à débit limité exigent sémaphores et backoff, chaque appel réseau exige un timeout, et les producteurs rapides exigent des files bornées pour que la mémoire ne croisse pas sans fin.

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

#### Qu'est-ce que `pyproject.toml` ?

Le fichier de configuration standard des projets Python : système de build, métadonnées, dépendances, points d'entrée et réglages des outils (pytest, ruff, mypy).

#### Comment fonctionne asyncio ?

Une boucle d'événements exécute des coroutines. À chaque `await` sur une opération d'E/S, la coroutine rend la main pour que d'autres avancent. `asyncio.gather` en lance plusieurs à la fois :

```python
import asyncio, httpx

async def main(urls):
    async with httpx.AsyncClient(timeout=30) as client:
        return await asyncio.gather(*(client.get(u) for u in urls))

asyncio.run(main(urls))
```

#### Qu'est-ce que `asyncio.TaskGroup` ?

Un gestionnaire de contexte (3.11+) pour la concurrence structurée : le bloc attend toutes les tâches créées dans le groupe, et si l'une échoue, les autres sont annulées et les erreurs sont levées ensemble dans un `ExceptionGroup`. C'est plus sûr que `gather`, qui par défaut laisse les autres tâches continuer après un échec.

```python
async with asyncio.TaskGroup() as tg:
    orders = tg.create_task(fetch_orders())
    users = tg.create_task(fetch_users())
print(orders.result(), users.result())
```

#### Qu'est-ce que `uv` ?

Un gestionnaire de paquets et de projets Python très rapide, écrit en Rust, qui remplace les flux pip, pip-tools et virtualenv (`uv add`, `uv sync`, `uv run`) et sait installer des versions de Python.

#### Qu'est-ce qu'un wheel ?

Un format de distribution précompilé (`.whl`) qui s'installe sans étape de build. Les jobs Databricks, par exemple, exécutent du code empaqueté en wheels.

#### Comment mettre un timeout sur un appel réseau ?

Passez un timeout à la bibliothèque (`requests.get(url, timeout=30)`, `httpx.AsyncClient(timeout=30)`) et, en code asynchrone, bornez un bloc d'awaits avec `async with asyncio.timeout(10):` (3.11+) ou un seul avec `asyncio.wait_for`. N'appelez jamais un service externe sans timeout : une connexion bloquée attendrait indéfiniment.

#### Qu'est-ce que pytest, et pourquoi le préfère-t-on à unittest ?

Un framework de tests où les tests sont de simples fonctions avec de simples `assert`, avec des messages d'échec détaillés, des fixtures, la paramétrisation et un large écosystème de plugins.

<!-- challenge -->

Un scraper asynchrone lance 50 000 requêtes d'un coup avec `gather` et l'API bannit le client. Comment corriger ?

<!-- solution -->

Limiter la concurrence avec un `asyncio.Semaphore` (ou un pool de workers borné), respecter `Retry-After`, relancer les 429 avec backoff exponentiel et fixer un timeout sur chaque requête.

<!-- takeaways -->

- Les coroutines se mettent en pause à `await` ; la boucle exécute les autres.
- `asyncio.run` démarre l'event loop.
- Bornez la concurrence ; fixez toujours des timeouts.

<!-- unit: Accélérer le code -->

<!-- goals -->

- Profiler avant d'optimiser et savoir ce qui rend Python rapide.
- Éviter pandas ligne par ligne, et choisir entre PyPy, multiprocessing et Spark.

<!-- concept -->

La vitesse vient de la mesure, puis de la modification de la partie la plus lente. Les profileurs montrent où passe le temps, souvent à un endroit inattendu. La plupart des gains viennent de meilleurs algorithmes et structures de données, et du transfert des boucles vers du C : built-ins, NumPy, opérations vectorisées de pandas ou Polars.

D'autres interpréteurs et le parallélisme aident dans des cas précis. Spark sert aux données qui dépassent une machine, pas à accélérer de petits jobs.

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

#### Comment profiler du code Python ?

`cProfile` (`python -m cProfile -s cumtime script.py`) pour le temps par fonction, `timeit` pour les petits extraits, `tracemalloc` pour la mémoire, et des profileurs par échantillonnage pour les processus en cours. Python 3.15 ajoute le paquet `profiling` : `profiling.sampling` s'attache à un processus en cours avec un surcoût très faible et produit des flame graphs, et `profiling.tracing` est le nouvel emplacement de `cProfile`. Dans les versions antérieures, py-spy joue ce rôle.

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

#### CPython a-t-il un compilateur JIT ?

Un compilateur expérimental, ajouté en 3.13 (PEP 744) et inclus dans les installeurs Windows et macOS depuis 3.14, mais désactivé par défaut (`PYTHON_JIT=1` l'active). Ses gains restent modestes ; l'essentiel des accélérations de CPython depuis 3.11 vient de l'interpréteur adaptatif spécialisé. Pour de gros gains sur du code numérique, les bibliothèques vectorisées ou PyPy restent les options.

#### Qu'est-ce que la couverture de tests, et viser 100 % est-il un bon objectif ?

La part du code exécutée par les tests (`pytest-cov`). Elle montre les zones non testées, mais une forte couverture ne prouve pas que les tests vérifient les bonnes choses. Visez des tests utiles sur la logique risquée.

<!-- challenge -->

Une transformation pandas utilise `df.apply(func, axis=1)` sur 20 millions de lignes et prend 40 minutes. Que tentez-vous d'abord ?

<!-- solution -->

Réécrire `func` avec des opérations vectorisées sur les colonnes (arithmétique, `np.where`, accesseurs `str` et `dt`) pour que le travail s'exécute en C ; profiler pour confirmer, et envisager Polars si c'est encore lent.

<!-- takeaways -->

- Profilez d'abord.
- Meilleures structures de données et vectorisation gagnent le plus.
- Spark sert l'échelle, pas la vitesse des petits jobs.

<!-- unit: Mémoire -->

<!-- goals -->

- Expliquer comment Python gère la mémoire.
- Repérer les croissances de mémoire de type fuite et comprendre les caches de bytecode.

<!-- concept -->

CPython libère la plupart des objets dès que plus rien n'y fait référence, par comptage de références, et un collecteur de cycles nettoie les groupes d'objets qui ne se référencent qu'entre eux. Les problèmes de mémoire des programmes de longue durée sont donc presque toujours des références maintenues en vie : caches globaux, listes qui grandissent, closures qui retiennent de gros objets.

Les trouver suppose de mesurer les allocations dans le temps. Les caches de bytecode n'ont rien à voir, même si on les confond souvent avec la mémoire : ils ne font qu'accélérer les imports.

<!-- example -->

```python
import tracemalloc
tracemalloc.start()
run_batch()
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("lineno")[:5]:
    print(stat)          # top allocation sites
```

#### Quelle est la différence entre tests unitaires, d'intégration et de bout en bout ?

Les tests unitaires vérifient une fonction ou une classe isolément. Les tests d'intégration vérifient des composants qui fonctionnent ensemble (le code et une base de données). Les tests de bout en bout exécutent tout le système sur des entrées réalistes.

#### Quels outils maintiennent la qualité du code Python ?

Un formateur et un linter (ruff, ou black et flake8), un vérificateur de types (mypy, pyright), des hooks pre-commit, des tests en CI et la revue de code.

#### Comment vérifier les types avec mypy ?

Ajouter des annotations de type et lancer `mypy src/`. Il signale les incohérences de types de façon statique, avant l'exécution. On l'adopte progressivement avec des réglages par module.

#### Que sont les références faibles ?

Des références qui ne maintiennent pas un objet en vie (`weakref.ref`, `WeakValueDictionary`, `WeakKeyDictionary`) : dès qu'il ne reste aucune référence forte, l'objet est libéré et la référence faible renvoie `None`. Elles conviennent aux caches et registres qui ne doivent pas garder des objets en mémoire à eux seuls.

<!-- challenge -->

La mémoire d'un worker de longue durée augmente de 100 Mo par heure jusqu'à ce qu'il soit tué. Le code a un `CACHE = {}` au niveau module rempli à chaque requête. Que changez-vous ?

<!-- solution -->

Borner le cache : utiliser `functools.lru_cache(maxsize=...)` ou un cache limité en taille ou en durée, ou le vider périodiquement ; confirmer avec `tracemalloc` qu'il était bien la source.

<!-- takeaways -->

- Le comptage de références libère les objets immédiatement.
- Les fuites sont généralement des références maintenues.
- Mesurez les allocations avec `tracemalloc`.

<!-- stage: Pratique de l'ingénierie -->

### Typage, packaging, environnements et tests

<!-- unit: Environnements et packaging -->

<!-- goals -->

- Isoler les projets avec des environnements virtuels et pyproject.toml.
- Rendre les installations reproductibles et construire des wheels avec entry points.

<!-- concept -->

Chaque projet a besoin de son propre ensemble de paquets, sinon les mises à jour de l'un cassent l'autre. Les environnements virtuels les isolent ; `pyproject.toml` déclare en un seul endroit le projet, ses dépendances et ses outils.

La reproductibilité vient des lock files qui figent la version de chaque paquet, installés de la même façon en développement, en CI et en production. Les wheels empaquettent votre code pour le déploiement, et les entry points transforment des fonctions en commandes.

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

#### Comment lire un gros CSV avec pandas sans manquer de mémoire ?

Lire par blocs, ne sélectionner que les colonnes utiles, fixer des types compacts, ou utiliser un format en colonnes et un moteur paresseux :

```python
for chunk in pd.read_csv("big.csv", usecols=["id", "amount"], dtype={"id": "int64"}, chunksize=500_000):
    process(chunk)
```

#### Quelle version de Python un nouveau projet doit-il cibler ?

Une version récente qui a encore des années de support. Une nouvelle version sort chaque mois d'octobre, reçoit environ deux ans de corrections de bugs, puis des correctifs de sécurité jusqu'à cinq ans après sa sortie (PEP 602). Fin 2026, cela veut dire de 3.13 à 3.15, selon ce que votre plateforme prend en charge (runtimes Databricks, Lambda, images Airflow). Déclarez-la dans `requires-python` et testez-la en CI.

<!-- challenge -->

Un job fonctionne sur le portable d'un développeur mais échoue en production après la sortie d'une nouvelle version majeure d'une bibliothèque. Que mettez-vous en place ?

<!-- solution -->

Un lock file (uv, pip-tools ou Poetry) figeant toutes les versions, installé avec `--frozen` en CI et en production, les mises à jour de dépendances passant délibérément par des pull requests.

<!-- takeaways -->

- Un environnement virtuel par projet.
- `pyproject.toml` déclare le projet.
- Les lock files rendent les installations reproductibles.

<!-- unit: Tester avec pytest -->

<!-- goals -->

- Écrire des tests pytest avec fixtures, paramétrage et mocks.
- Choisir les niveaux de test et utiliser judicieusement couverture et tests par propriétés.

<!-- concept -->

pytest garde les tests simples : des fonctions ordinaires avec des `assert` ordinaires et des messages d'échec utiles. Les fixtures fournissent ce dont les tests ont besoin, des données d'exemple aux répertoires temporaires ; le paramétrage exécute un test sur de nombreuses entrées ; les mocks remplacent les dépendances lentes ou externes.

Une suite équilibrée a beaucoup de tests unitaires rapides, quelques tests d'intégration et peu de tests de bout en bout. La couverture montre les zones non testées ; les tests par propriétés trouvent des cas limites auxquels on n'avait pas pensé.

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

<!-- challenge -->

Les tests d'un client d'API appellent la vraie API : ils sont lents et échouent quand elle est indisponible. Comment les corriger ?

<!-- solution -->

Simuler la couche HTTP dans les tests unitaires (pytest-mock, respx ou responses) avec des réponses enregistrées, et garder un ou deux tests d'intégration contre un bac à sable, exécutés à part.

<!-- takeaways -->

- pytest : asserts simples, fixtures, paramétrage.
- Simulez les dépendances externes dans les tests unitaires.
- La couverture est un signal, pas un objectif.

<!-- unit: Vérifications statiques et types -->

<!-- goals -->

- Maintenir la qualité du code avec formateurs, linters et vérificateurs de types.
- Utiliser mypy, TypedDict et les génériques.

<!-- concept -->

Les vérifications automatiques détectent les erreurs avant l'exécution des tests. Un formateur met fin aux débats de style, un linter signale bugs et mauvais motifs, et un vérificateur de types trouve, grâce à vos hints, les mauvais arguments et les `None` non gérés. Les lancer en pre-commit et en CI en fait une routine.

Les type hints gagnent en utilité avec des types plus riches : `TypedDict` décrit des enregistrements en forme de dict, et les génériques décrivent conteneurs et fonctions qui travaillent avec n'importe quel type de façon cohérente.

<!-- example -->

```python
from typing import TypedDict

class OrderRow(TypedDict):
    order_id: int
    amount: float
    country: str

def first_or_none[T](items: list[T]) -> T | None:     # syntaxe des génériques de Python 3.12
    return items[0] if items else None
```
```bash
ruff check . && ruff format --check . && mypy src/
```

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

#### Que fait l'instruction `type` ?

Elle déclare un alias de type (Python 3.12, PEP 695) : `type Row = dict[str, str | int]`. Les alias sont évalués paresseusement et peuvent être génériques : `type Pair[T] = tuple[T, T]`. La même PEP permet aux classes et fonctions de déclarer leurs paramètres de type entre crochets (`class Box[T]: ...`), ce qui remplace la plupart des usages de `TypeVar`.

<!-- challenge -->

Une fonction reçoit des lignes sous forme de dicts, et des fautes de frappe comme `row["ammount"]` atteignent la production. Comment le typage peut-il les attraper ?

<!-- solution -->

Décrire les lignes avec un `TypedDict` (ou une dataclass ou un modèle pydantic) et annoter la fonction ; mypy signale alors les clés inconnues comme `"ammount"` avant l'exécution.

<!-- takeaways -->

- Formatez, lintez et vérifiez les types automatiquement.
- `TypedDict` type les enregistrements en dict.
- Les génériques gardent cohérents les types des conteneurs.

<!-- unit: Configuration et structure du projet -->

<!-- goals -->

- Gérer configuration et secrets en sécurité.
- Valider les réglages avec pydantic et structurer un projet de pipeline.

<!-- concept -->

Le même code doit tourner en développement, en CI et en production avec des réglages différents : la configuration vient donc de l'environnement, jamais de valeurs codées en dur, et les secrets d'un gestionnaire de secrets. La valider au démarrage, avec des erreurs claires, vaut mieux que découvrir une variable manquante au milieu d'un job.

La structure du projet suit les responsabilités : un paquet `src` découpé en ingestion, transformations et sorties, des points d'entrée minces, et les tests à côté du code qu'ils couvrent.

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

#### Comment se connecter à une base de données depuis Python en toute sécurité ?

Avec un pilote (psycopg pour PostgreSQL) ou SQLAlchemy, en utilisant des requêtes paramétrées et jamais du formatage de chaînes, pour éviter l'injection SQL :

```python
cur.execute("select * from companies where country = %s", (country,))
```

#### Comment charger rapidement beaucoup de lignes dans PostgreSQL depuis Python ?

Utiliser `COPY` (le `cursor.copy()` de psycopg) plutôt que des insertions ligne à ligne, ou des insertions par lots avec `executemany` et des tailles de page. Faire le chargement dans une seule transaction.

#### Comment lire une configuration TOML ?

Avec `tomllib`, dans la bibliothèque standard depuis 3.11. Il ne fait que lire, et le fichier doit être ouvert en mode binaire ; pour écrire, il faut un paquet comme `tomli-w`. Python 3.15 le met à jour vers TOML 1.1.

```python
import tomllib
with open("settings.toml", "rb") as f:
    config = tomllib.load(f)
```

#### Qu'est-ce que SQLAlchemy ?

Une boîte à outils pour bases de données avec une couche Core (langage d'expressions SQL, pool de connexions, engines) et un ORM. pandas utilise des engines SQLAlchemy pour `read_sql` et `to_sql`.

<!-- challenge -->

Un job lit `os.environ["BATCH_SIZE"]` au fond d'une boucle et plante au bout de deux heures quand la variable manque en production. Comment l'éviter ?

<!-- solution -->

Charger et valider toute la configuration une fois au démarrage (settings pydantic ou fonction de validation), avec types et valeurs par défaut, pour que les valeurs manquantes ou invalides échouent immédiatement.

<!-- takeaways -->

- Configuration depuis l'environnement ; secrets depuis un gestionnaire.
- Validez les réglages au démarrage.
- Structurez les projets par responsabilité.

### Python pour le data engineering

<!-- unit: L'essentiel de pandas -->

<!-- goals -->

- Lire de gros fichiers avec pandas et sélectionner des données avec loc et iloc.
- Grouper, fusionner et gérer les valeurs manquantes sans avertissements.

<!-- concept -->

pandas est l'outil quotidien pour les données qui tiennent en mémoire. Ses gestes de base : sélectionner (par étiquette ou position), grouper avec des agrégations nommées, fusionner comme des jointures SQL, et traiter délibérément les valeurs manquantes.

La mémoire est la limite habituelle : ne lire que les colonnes utiles avec des types compacts, ou par morceaux, la repousse loin. L'indexation chaînée déclenche le fameux avertissement parce que pandas ne peut pas savoir si vous modifiez une copie ou l'original.

<!-- example -->

```python
import pandas as pd
df = pd.read_csv("companies.csv", usecols=["country", "industry", "revenue"],
                 dtype={"country": "category", "industry": "category"})
summary = (df.groupby(["country", "industry"], as_index=False, observed=True)
             .agg(companies=("revenue", "size"), revenue=("revenue", "sum")))
df.loc[df["revenue"] < 0, "revenue"] = pd.NA       # assign on the original, no warning
```

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

<!-- challenge -->

`pd.merge(orders, customers, on="customer_id")` renvoie plus de lignes que `orders`. Que s'est-il passé, et comment le détecter ?

<!-- solution -->

`customers` contient des `customer_id` en double : les commandes se démultiplient. Dédupliquer d'abord les clients et utiliser `validate="many_to_one"` dans `merge`, qui lève une erreur si le côté droit n'est pas unique.

<!-- takeaways -->

- Ne lisez que les colonnes utiles, avec des dtypes compacts.
- Utilisez `.loc` pour les assignations.
- `merge(validate=...)` détecte le fan-out.

<!-- unit: Formats colonnaires et moteurs rapides -->

<!-- goals -->

- Expliquer Parquet et Arrow, et écrire du Parquet partitionné.
- Savoir quand Polars ou DuckDB battent pandas.

<!-- concept -->

Le CSV est un mauvais format pour l'analytique : non typé, non compressé, lu en entier. Parquet stocke les données par colonne avec types et statistiques, pour que les outils ne lisent que le nécessaire. Arrow est le format en mémoire correspondant, qui permet à pandas, Polars, DuckDB et Spark d'échanger des données sans copie.

Par-dessus, de nouveaux moteurs changent ce qu'une machine peut faire : Polars tourne en multithread avec un optimiseur de requêtes, et DuckDB exécute du SQL directement sur des fichiers Parquet et des DataFrames.

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

<!-- challenge -->

Un analyste charge 8 Go de CSV dans pandas pour calculer un agrégat et manque de mémoire. Que lui suggéreriez-vous ?

<!-- solution -->

Convertir une fois les fichiers en Parquet, puis les interroger avec DuckDB (ou des scans paresseux Polars), qui ne lisent que les colonnes utiles, traitent les données en flux et utilisent tous les cœurs.

<!-- takeaways -->

- Parquet est typé, colonnaire et compressé.
- Arrow permet aux outils de partager des données sans copie.
- Polars et DuckDB repoussent les limites d'une machine.

<!-- unit: API, fichiers et bases de données -->

<!-- goals -->

- Appeler des API REST de façon robuste et télécharger de gros fichiers en flux.
- Se connecter aux bases en sécurité, charger des lignes en masse et lire depuis S3.

<!-- concept -->

Les pipelines passent une grande partie de leur temps à dialoguer avec d'autres systèmes, et chaque échange peut échouer. Les appels d'API exigent sessions, timeouts, relances avec backoff et pagination. Les gros téléchargements doivent être écrits en flux sur disque au lieu de remplir la mémoire.

Les bases de données exigent des requêtes paramétrées pour la sécurité et des voies de masse comme `COPY` pour la vitesse ; SQLAlchemy ajoute pooling et portabilité. Le stockage objet a ses propres clients, ou un accès de type fichier via fsspec.

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

<!-- challenge -->

Un job construit du SQL avec `f"SELECT * FROM users WHERE email = '{email}'"`. Quels sont les deux problèmes, et la correction ?

<!-- solution -->

L'injection SQL (une valeur piégée peut modifier la requête) et les bugs de guillemets (les e-mails avec apostrophe la cassent). Utiliser des requêtes paramétrées : `cur.execute("... WHERE email = %s", (email,))`.

<!-- takeaways -->

- Sessions, timeouts, relances et pagination pour les API.
- Téléchargez les gros fichiers en flux.
- Paramétrez le SQL ; chargez en masse avec `COPY`.

<!-- unit: Des étapes de pipeline fiables -->

<!-- goals -->

- Rendre les étapes de pipeline idempotentes et valider les données avant chargement.
- Gérer encodages et gros JSON, et orchestrer des pipelines Python.

<!-- concept -->

Une étape de pipeline sera relancée, réexécutée et nourrie de données surprenantes. Des étapes idempotentes, qui donnent le même résultat exécutées deux fois, rendent les relances sûres ; valider avant de charger arrête les mauvaises données à l'entrée. Encodage et taille des fichiers figurent parmi les surprises courantes.

Planification, dépendances et alertes relèvent d'un orchestrateur, pas de cron et de l'espoir. Que Python transforme lui-même les données (ETL) ou les déplace surtout pour qu'un entrepôt les transforme (ELT) détermine la quantité de code à écrire.

<!-- example -->

```python
def load_day(conn, day: str, rows: list[dict]) -> None:
    validate(rows)                                   # schema, nulls, ranges, duplicates
    with conn.transaction():
        conn.execute("DELETE FROM sales WHERE sale_date = %s", (day,))
        copy_rows(conn, "sales", rows)               # rerun-safe: replaces the day
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

#### Comment gérer les problèmes d'encodage à la lecture de fichiers ?

Passez explicitement le bon `encoding`, n'utilisez `errors="replace"` qu'en connaissance de cause, détectez un BOM avec `encoding="utf-8-sig"` et réparez le mojibake (`'TravesÃ­a'.encode('latin-1').decode('utf-8')`) avec une protection pour les chaînes où l'aller-retour échoue. Depuis Python 3.15, `open()` utilise UTF-8 par défaut au lieu de l'encodage de la locale (PEP 686), ce qui évite bien des surprises sous Windows, mais indiquer l'encodage reste le choix portable.

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

<!-- challenge -->

Une étape quotidienne ajoute des lignes à une table, et une relance après un timeout a doublé les données du jour. Réécrivez sa stratégie d'écriture.

<!-- solution -->

Remplacer la tranche du jour dans une transaction (supprimer la date puis insérer, ou faire un upsert sur la clé métier), pour qu'une double exécution laisse les mêmes données.

<!-- takeaways -->

- Les étapes idempotentes rendent les relances sûres.
- Validez avant de charger.
- Les orchestrateurs gèrent planification, relances et alertes.

<!-- unit: Python et Spark -->

<!-- goals -->

- Expliquer le lien entre PySpark et Python.
- Éviter les UDF Python lentes dans PySpark.

<!-- concept -->

PySpark permet à Python de décrire des calculs distribués, mais le travail s'exécute dans le moteur JVM de Spark. Le code Python construit le plan ; les lignes touchent rarement l'interpréteur Python, et c'est pourquoi PySpark passe à l'échelle.

L'exception, ce sont les UDF Python : chaque ligne est envoyée à un processus Python puis renvoyée, avec perte de vitesse et d'optimisation. Les fonctions intégrées, ou les pandas UDF vectorisées quand Python est inévitable, gardent le travail là où Spark est rapide.

<!-- example -->

```python
from pyspark.sql import functions as F
# slow: Python UDF per row
# clean = F.udf(lambda s: s.strip().lower())
# fast: built-in functions
df = df.withColumn("email", F.lower(F.trim("email")))
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

<!-- challenge -->

Un job PySpark utilise une UDF pour calculer `price * qty * (1 - discount)`. Pourquoi est-ce du gaspillage, et qu'est-ce qui la remplace ?

<!-- solution -->

Une UDF Python sérialise chaque ligne vers Python pour une arithmétique simple que Spark sait faire nativement. Utiliser une expression de colonne : `F.col("price") * F.col("qty") * (1 - F.col("discount"))`.

<!-- takeaways -->

- PySpark construit les plans ; la JVM les exécute.
- Les UDF Python sérialisent chaque ligne.
- Préférez les built-ins ; pandas UDF si nécessaire.
