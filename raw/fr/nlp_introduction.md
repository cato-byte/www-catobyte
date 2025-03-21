## Comment les machines nous comprennent-elles ? Introduction au PNL (traitement du langage naturel)

##### Publié le {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Image créée par ChatGPT, OpenAI. 7 octobre 2024](../../images/nlp_introduction_title_img.webp)

Vous êtes-vous déjà demandé comment des outils comme les assistants IA comprennent vos questions et vos commandes et produisent une réponse qui, à première vue, semble au moins cohérente ? Comment une machine qui, à son niveau le plus élémentaire, effectue des calculs sur des octets, peut-elle obtenir des résultats aussi étonnants ?

Pour accomplir cet exploit, nous utilisons des techniques de traitement du langage naturel (TALN), un sous-domaine de l’informatique qui combine l’étude de la grammaire et de l’apprentissage automatique pour permettre aux ordinateurs de comprendre le langage humain et de produire des réponses cohérentes.

La PNL a acquis une notoriété significative au cours de la dernière année grâce à l’émergence des LLM, ou grands modèles de langage. Même si le nom LLM ne vous dit peut-être pas grand-chose à première vue, vous avez probablement déjà interagi avec certains d'entre eux : ChatGPT, Gemini et DeepSeek, entre autres, sont de grands modèles de langage.

Il existe également des SLM, ou modèles linguistiques à petite échelle. Ceux-ci sont généralement entraînés avec un ensemble de données plus restreint, moins de paramètres et tendent à se concentrer sur un domaine spécifique, contrairement aux LLM, qui se veulent plus généralistes et produisent des réponses dans différents domaines de connaissances.

Ci-dessous, je vais vous présenter quelques techniques de PNL afin que vous puissiez comprendre ce qui se passe dans les coulisses.

Dans cet article, nous explorerons certains concepts de base du PNL, notamment la tokenisation, le marquage des parties du discours (POS) et la reconnaissance d'entités nommées (NER).

Bien que le traitement du langage naturel nous ait permis d'obtenir une interaction homme-machine très fluide, ouvrant de nouvelles opportunités dans divers domaines, nous n'avons pas encore réussi à obtenir un modèle de raisonnement véritablement autonome capable de passer le test de Turing (un test qui évalue la capacité d'une machine à présenter un comportement intelligent de type humain).

Examinons maintenant plus en détail certains de ces processus de base.

### Tokenisation

La tokenisation est la première étape fondamentale du traitement du langage. Elle consiste à diviser un texte en fragments plus petits, appelés tokens, qui peuvent être des mots ou des phrases. Cette étape permet aux machines de traiter les textes plus précisément et d’extraire les informations pertinentes.

Prenons un exemple en utilisant les phrases suivantes comme base :

**« J'ai hâte de sortir des bois et d'aller à la campagne aujourd'hui. Le soleil brille, les oiseaux chantent et je suis de très bonne humeur. Tu ne ressens pas la même chose, Caton ? »**

Les jetons de ce texte seraient chaque mot et signe de ponctuation qui s'y trouvent. Des scripts peuvent être créés pour effectuer cette tâche automatiquement. Il est important de souligner qu’il est important de préserver l’ordre des jetons, car il s’agit d’informations précieuses qui peuvent nous indiquer le sens d’un mot ou à quelle famille grammaticale il appartient. Le résultat ressemblerait à ceci.


Python
['Je','veux','quitter','la',forêt','et','aller','au',champ','aujourd'hui','.'Le','soleil','brille','les',oiseaux','chantent','et','je','suis',de'très','bonne','humeur','.'N'arrive-t-il','pas',les'mêmes','choses','à',Cato','?']
```

Nous avons maintenant une liste de jetons de mots. Vous vous demandez peut-être pourquoi j'ai divisé le mot « del » en « de » et « el » et « al » en « a ». En effet, « del » est une contraction de « de » et « el », et cette séparation est importante pour aider les systèmes de traitement du langage naturel (TAL) à traiter séparément leurs composantes grammaticales. « de » est une préposition et « el » un article. Officiellement, il n'existe que deux contractions en espagnol : del et al, mais elles sont plus courantes dans d'autres langues.



La tokenisation des phrases est également courante. L'obtention de jetons de phrases entières facilite la compréhension du contexte général d'une discussion ou d'un argument et est souvent utilisée dans les systèmes de traduction automatique ou de résumé.

À partir de notre exemple, nous obtiendrions les jetons de phrase suivants :

**['J'ai hâte de sortir des bois et d'aller à la campagne aujourd'hui','Le soleil brille, les oiseaux chantent et je suis de très bonne humeur','N'es-tu pas pareil, Caton ?']**

Le résultat de la tokenisation est une entrée pour d’autres processus tels que l’extraction de caractéristiques, dont l’objectif est d’obtenir une représentation numérique des mots. Cette représentation numérique peut ensuite être utilisée comme entrée pour former ou interroger un modèle d’apprentissage en profondeur. Détailler le processus d’extraction de fonctionnalités peut faire l’objet d’un article à part entière. Pour simplifier, je dirai que cette représentation numérique peut indiquer le nombre de caractères d'un mot, combien de fois il apparaît dans une phrase, s'il commence par une majuscule, à quel point il est rare, etc.

En bref, la tokenisation prépare le texte à l’analyse ultérieure.supérieur, ce qui facilite la compréhension du sens des mots, la détection de modèles et l'exécution d'autres tâches telles que la traduction ou l'analyse des sentiments.

### Balisage des parties du discours (POS)

Pour permettre à une machine de traiter le langage naturel, il est nécessaire que le langage ait été modélisé d’une manière ou d’une autre. Cela signifie que les phénomènes qui se produisent dans une langue sont organisés et capturés de telle manière qu’ils peuvent être utilisés pour prédire ou réorganiser les utilisations futures de la langue.

Une façon de réaliser cette modélisation est le balisage grammatical ou le balisage des parties du discours (POS), une autre tâche de base dans tout système PNL. Pour réaliser cette étape, il existe des outils qui offrent une fonctionnalité d'étiquetage automatique et sont utilisés dans le domaine du NLP tels que spaCy et NLTK. Ces tagueurs utilisent des corpus linguistiques, qui sont des collections de phrases dont la structure grammaticale est annotée.

La création de ces corpus, ou collections de phrases étiquetées, est un projet qui a pris des années. Elles ont été réalisées de manière semi-automatique, combinant étiquetage automatique et correction manuelle. Au début, ils utilisaient un algorithme appelé PARTS() qui effectuait le premier étiquetage. Un linguiste réviserait ensuite cette version initiale et la corrigerait.

Le projet Penn TreeBank, développé à l'Université de Pennsylvanie entre 1989 et 1996, est une implémentation concrète de l'un de ces ensembles de phrases, spécifiquement pour la langue anglaise. Le produit final de ce projet est un ensemble de plus de 7 millions de mots avec des balises de parties du discours (POS) et une analyse syntaxique d'environ 3 millions de phrases.

[Plus d'informations sur le projet Penn TreeBank peuvent être trouvées ici](https://www.researchgate.net/publication/2873803_The_Penn_Treebank_An_overview#:~:text=The%20Penn%20Treebank%2C%20in%20its,spoken%20text%20annotated%20for%20speech)

En utilisant des étiqueteurs automatiques basés sur ces corpus, nous pouvons attribuer chaque mot d'une phrase à l'une des catégories grammaticales définies dans le corpus. C'est important pour que les machines comprennent le contexte et le sens.

Sans marquage POS, nous pourrions mal interpréter des phrases telles que :

**Je vous raconte une histoire intéressante.** (Ici, « histoire » est un verbe qui signifie raconter quelque chose.) **J'aime lire une bonne histoire avant de me coucher.** (Dans ce cas, « histoire » est un nom.)



L'ensemble de balises Penn Treebank est spécifique à l'anglais, mais n'est pas adaptable à d'autres langues avec des types de mots, des structures grammaticales et une évolution différents.

Pour remédier à cette limitation, il existe le projet ['Universal Dependencies project'](https://universaldependencies.org/introduction.html) (UPOS), qui vise à créer une banque de structures grammaticales cohérentes dans plusieurs langues. Cette approche est utile pour les applications multilingues, en raison de sa prise en charge de plus de 100 langues.

Il existe également des recherches et développements pour créer des corpus spécifiques à d'autres langues comme cet [article](https://www.researchgate.net/publication/39436708_Anotacion_semiautomatica_con_papeles_tematicos_de_los_corpus_CESS-ECE) qui parle de la création d'un corpus pour l'espagnol et le catalan.

Vous trouverez ci-dessous deux tableaux contenant quelques catégories de balises grammaticales issues des corpus Penn TreeBank et UPOS.

**Penn Treebank**


|Étiquette | Catégorie grammaticale | Définition |
|------------|------------------------|
|NN | NOM | Noms de personnes, de lieux, de choses ou d'idées |
|VB | VERBE | Mots qui décrivent des actions, des états ou des événements |
|JJ | ADJECTIF | Mots qui décrivent ou modifient les noms |
|RB | ADVERBE | Mots qui modifient les verbes, les adjectifs ou d’autres adverbes |
|PRP | PRONOM | Mots qui remplacent les noms |
|DT | DÉTERMINATEUR | Mots qui introduisent les noms |
|DANS | PRÉPOSITION | Mots qui montrent les relations entre les noms ou les pronoms et d’autres mots dans une phrase.
|CC | CONJONCTION | Mots qui relient des clauses, des phrases ou des mots.
|AUX | VERBE AUXILIAIRE | Verbes utilisés pour former les temps, les modes ou les voix d'autres verbes.
|PP | PARTICULE | Mots qui font partie des verbes à particule |

**Projet de dépendances universelles UPOS**

|Étiquette | Catégorie grammaticale | Définition |
|------------|------------------------|
|ADJ |Adjectif| Décrit un nom (par exemple, heureux, vert, petit).
|ADP |Adposition| Prépositions et postpositions (par exemple, dans, sur, à).|
|ADV |Adverbe| Modifie les verbes, les adjectifs ou d’autres adverbes (par exemple, rapidement, très, ici).
|AUX |Verbe auxiliaire| Verbes qui aident à former le temps, l'humeur ou la voix (par exemple, est, avoir, volonté).
|CCONJ| Conjonction de coordination | Associez des mots, des phrases ou des phrases de manière égale (par exemple, et, mais, ou).
|DET| Déterminant| Modifie un nom (par exemple, le, un, certains, mon).
|INTJ| Interjection| Exprime une émotion ou un son (par exemple, wow, aïe, uh-huh).
|NOUN| Nom| Nommez des personnes, des lieux, des choses ou des idées (par exemple, un chat, une ville, la liberté).
|NUM |Numéral| Indique des nombres (par exemple, un, deux, 42).|
|PARTIE| Particule| Mots fonctionnels ou morphèmes (par exemple, not, to in, not go ou to go).
|PRON| Pronom| Remplace un nom (par exemple, elle, cela, eux-mêmes).
|PROPN| Nom propre| Nommez des entités spécifiques (par exemple, John, Paris, Google).|
|PUNCT| Score| Tout signe de ponctuation (par exemple, ., ;, ?).|
|SCONJ| Conjonction de subordination| Liens entre les clauses avec dépendance (par exemple, parce que, cependant, si).
|SYM | Symbole| Symboles non alphanumériques (par exemple, $, %, +, @).|
|VERBE| Verbe| Actions, événements ou états (par exemple, exécuter, devenir, exister).
|X|Autre| Catégorisation générale des mots non classés (par exemple, expressions étrangères ou fautes de frappe) |

Le balisage grammatical peut être effectué de différentes manières, dont certaines sont :

**Systèmes basés sur des règles** : Ils utilisent des règles linguistiques pour catégoriser les mots. Il peut y avoir des règles aussi simples que Colombie est un nom (NOM). D'autres sont un peu plus complexes, comme le remplacement de la catégorie nominale (NOM) par un verbe (VERBE) s'il est précédé d'un pronom. Un autre exemple serait de dire que tous les mots se terminant par -mente sont des adverbes de manière tels que tranquillement, tranquillement et sereinement. Mais cette règle ne fonctionnerait pas pour les mots demente, clemente, vehemente, lamente, aumenta etc. qui sont des adjectifs et des verbes mais pas des adverbes de manière. Cette modélisation du langage basée sur des règles est assez rigide et présente des difficultés pour gérer l’ambiguïté ou étiqueter des mots inconnus.

**Modèles statistiques**:

Les approches statistiques classent les probabilités qu'un jeton appartienne à différentes catégories en choisissant la catégorie la plus probable.

L’un de ces modèles statistiques est celui des chaînes de Markov cachées. Ces modèles ont ce qu’on appelle des états cachés. Il s’agirait des catégories grammaticales telles que le déterminant, le verbe, l’adjectif, etc. Le modèle calcule deux types de probabilités : les probabilités de transition et les probabilités d’énonciation pour un mot.

Les probabilités de transition calculent, par exemple, la probabilité qu'un article soit suivi d'un nom. Les probabilités d'émission calculent la probabilité que le jeton analysé appartienne à une certaine catégorie. En considérant cette approche plus large, qui prend en compte la séquence de mots, le modèle atteint une approximation plus précise que les systèmes basés sur des règles. L’un des avantages de ces modèles est qu’ils sont légers et peuvent fonctionner avec des ressources de calcul limitées et pour de petits ensembles de données, comme un ensemble de données spécifique à un domaine. Mais ils peuvent être plus sujets aux erreurs que les modèles basés sur les réseaux neuronaux que je décrirai ci-dessous.

**Modèles d’apprentissage automatique** : les marqueurs grammaticaux modernes utilisent un mélange de méthodes statistiques et de réseaux neuronaux pour étiqueter les mots d’une langue. Les réseaux neuronaux sont formés à l'aide de bases de données linguistiques telles que Penn TreeBank et Universal Dependencies pour créer des étiqueteurs qui prédisent les catégories grammaticales des jetons en fonction d'une entrée de texte que le modèle n'a pas vue auparavant. Ce sont les systèmes qui se sont avérés plus flexibles dans la gestion de l’ambiguïté et l’étiquetage des mots inconnus.

 Pour plus de détails, vous pouvez vous référer à mes articles sur [l'apprentissage automatique](../post/a_simple_introduction_to_machine_learning.html) ou [l'apprentissage profond](../post/understanding_neural_networks.html).

Revenons à notre exemple et avons un bref aperçu des modèles. Après avoir passé les jetons via le système de balises upos, voici à quoi pourrait ressembler le résultat.

Python
jetons_upos = [
 ("J'ai", "VERBE"),("veux", "NOM"),("de", "ADP"),("sortir", "VERBE"),("de", "ADP"),("le", "DET"),("forêt", "NOM"),("et", "CCONJ"),("aller", "VERBE"),("à", "ADP"),("le", "DET"),("champ", "NOM"),("aujourd'hui", "ADV"),("., "PUNCT"),("Le", "DET"),("soleil", "NOM"),("brille", "VERBE"),(",", "PUNCT"),("les", "DET"),("oiseaux", "NOM"),("chanter", "VERBE"),("et", "CCONJ"),("Je suis", "VERBE"),("de", "ADP"),("très", "ADV"),("bon", "ADJ"),("humour", "NOM"),("., "PUNCT"),("¿", "PUNCT"),("Non", "ADV"),("te", "PRON"),("pasa", "VERBE"),("lo", "PRON"),("même", "ADJ"),(",", "PUNCT"),("Cato", "PROPN"),("?", "PUNCT")
]
```

### Reconnaissance d'entité nommée NER

La reconnaissance d'entités nommées (NER) est un processus par lequel les entités sont reconnues dans un texte, telles que des lieux, des personnes, des produits, des organisations, des nationalités, des dates, des valeurs numériques, entre autres. .

En utilisant NER, nous pouvons extraire des informations pertinentes d’un texte et les transformer en informations structurées (comme un tableau), qui peuvent être utilisées pour une analyse plus approfondie.



Vous essayez d'extraire différentes entitésd'un texte.

Vous pouvez trouver plus d'informations sur NER [ici](https://www.ibm.com/es-es/think/topics/named-entity-recognition)

La reconnaissance d’entités nommées (NER) aide les machines à identifier et à catégoriser les éléments clés du texte, tels que les noms, les dates et les lieux. Par exemple, dans la phrase :

« Cato a remporté le prix à Bogotá la semaine dernière »,

NER étiquetterait :

« Caton » en tant que PERSONNE,
« prix » en tant qu'ÉVÉNEMENT et
"Bogotá" comme LIEU.

Le NER est utile pour extraire des informations précieuses à partir de textes longs. Il peut aider à résumer du texte, à répondre à des questions et à améliorer les tâches d’analyse des sentiments. Les étiquettes NER sont généralement déterminées sur la base d’ontologies ou de vocabulaires créés par l’homme.

Vous trouverez ci-dessous une liste de certaines catégories NER courantes :

|Catégorie NER | Définition | Exemple |
|------------|------------------------|
|PER (Personne) |Noms de personnes| Isabel Allende, Mon Laferte |
|ORG (Organisation) |Noms d'organisations ou d'entreprises| Umbrella Corporation, Nokia|
|LOC (Localisation) |Noms de lieux géographiques| Bogotá, Parc Tayrona, Sagrada Familia|
|GPE (Entité géopolitique) |Régions politiques, telles que pays, villes ou États| Colombie, Sucre |
|DATE| Expressions de date ou d'heure spécifiques | 1er septembre 2024, demain |
|TEMPS| Horaires spécifiques | 15h00, midi |
|ARGENT| Montants monétaires | 50 000 pesos, 10 euros|
|POURCENTAGE| Pourcentages| 15 pour cent, 50 % |
|FAC (Installation) |Bâtiments, aéroports, routes| Monnaie, aéroport El Dorado, autoroute panaméricaine
|NORP | Nationalités, religions, groupes politiques | Colombie, Catholicisme, Parti vert
|PROD| Produit| Café Juan Valdez, Flores, Renault|
|OEUVRE_D'ART| Œuvres créatives| Contes sauvages, Les Ménines |
|LANGUE| Langues| Espagnol, Wayuu, Créole, Anglais|
|ÉVÉNEMENT |Événements nommés| Règne de la Panela, Jeux panaméricains |

Et pour revenir à notre prière initiale, nous pourrions nous attendre à un résultat comme celui-ci.

```shellsession
Reconnaissance d'entité nommée :
Entité : aujourd'hui, Étiquette : DATE, Début : 22, Fin : 27
Entité : Cato, Étiquette : ORG, Début : 123, Fin : 127
```

Le NER est essentiel pour extraire des informations structurées à partir de textes non structurés, ce qui est utile dans des tâches telles que la recherche et le résumé d'informations.

Analyse des sentiments

L’analyse des sentiments consiste à déterminer le sentiment ou l’émotion derrière un texte. Cela peut être délicat car le sarcasme, l’ironie ou le contexte peuvent changer radicalement le sens. Par exemple, la phrase « Super, exactement ce dont j'avais besoin ! » Cela peut sembler positif, mais il est probable que cela soit négatif en raison du ton.

L'analyse des sentiments classe une phrase comme positive, neutre ou négative, et parfois même plus précisément, comme fortement positive ou fortement négative. Cela est particulièrement utile pour traiter les commentaires des clients ou comprendre l’opinion publique. Les systèmes PNL modernes peuvent aller au-delà du positif, du neutre et du négatif et détecter davantage d’émotions dans le texte.

Voici une liste de certaines des émotions que ces systèmes peuvent détecter.

| Émotion | Ton émotionnel | Exemple|
|---------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| Bonheur | Positif | J'ai enfin atteint mon objectif et j'en suis très heureux ! |
| Émotion | Positif | J'ai hâte de commencer mon nouveau travail demain. Ce sera incroyable ! |
| Gratitude | Positif | Merci beaucoup de m'avoir aidé à traverser cette période difficile. Cela signifie beaucoup pour moi. |
| Colère | Négatif | Je n'arrive pas à croire qu'ils m'ont menti. Je suis furieux! |
| Tristesse | Négatif | Je me sens très déprimé aujourd'hui. Tout me rappelle ce que j'ai perdu. |
| La peur | Négatif | Marcher seul dans cette ruelle sombre me terrifie. |
| Déception | Négatif | J'espérais vraiment un meilleur résultat, mais je pense que je vais devoir réessayer. |
| Indifférence | Neutre | Je n'ai pas vraiment d'opinion sur ce sujet. Cela ne m'affecte pas. |
| Curiosité | Contexte spécifique | Je suis vraiment curieux de voir comment cette expérience va se dérouler ! Je suis curieux de savoir pourquoi tu m'évites. Cela me semble suspect. |
| Confusion | Contexte spécifique | Ce puzzle est déroutant, mais je m'amuse à le résoudre ! Je suis confus quant à ce qui se passe et cela me rend anxieux. |
| Espoir | Contexte spécifique | J’espère que cette nouvelle opportunité apportera le changement que j’attendais. J'espère que tu me pardonneras, mais au fond, j'ai peur que non. |
| Frustration | Contexte spécifique | Je suis frustré par ce projet, mais je sais que j'en serai fier une fois terminé. Ce trafic est tellement frustrant qu'il me fait perdre tout mon après-midi. |
| Amour | Contexte spécifique | J'aime passer du temps avec ma famille ;C'est très gratifiant. Je t'aime, mais cette relation détruit ma santé mentale. |
| Culpabilité | Contexte spécifique | Je me sens coupable de ce que j'ai dit, alors je vais m'excuser et arranger les choses. |

Cependant, les émotions sont complexes et le contexte est essentiel. Par exemple, « Je ne suis pas malheureux » est techniquement négatif, mais cela implique quelque chose de positif. L’analyse des sentiments utilise des modèles d’apprentissage automatique pour tenir compte de ces subtilités, même si même les meilleurs modèles peuvent être confrontés au sarcasme ou à l’ambiguïté.

### Résolution de co-référence

Avez-vous déjà lu une histoire dans laquelle les personnages apparaissent comme « il », « elle » ou « ils » et vous vous retrouvez à essayer de reconstituer de qui il s’agit ? C'est l'essence même de la résolution de coréférence : déterminer quand différents mots ou expressions font réellement référence à la même personne ou à la même chose.

Examinons cela de plus près avec notre exemple de phrase : « J’ai hâte de sortir aujourd’hui. Le soleil brille, les oiseaux chantent et je suis de très bonne humeur. Tu ne ressens pas la même chose, Caton ? » Dans ce récit léger, « tu » s’adresse clairement à Caton, tandis que « je » appartient à l’orateur. Pour nous, c’est simple : nos esprits relient les points de manière transparente. Mais pour un ordinateur ? C'est comme démêler une toile complexe. La résolution de coréférence donne aux machines les outils pour suivre ces connexions, garantissant qu'elles peuvent déterminer qui est qui, même dans un texte long et alambiqué.

Cette compétence joue un rôle clé dans des applications telles que la rédaction de résumés, où il est crucial de comprendre à qui ou à quoi chaque pronom fait référence. Imaginez un résumé qui utilise « il » ou « ils » de manière ambiguë et sans contexte : il semblerait décousu et difficile à suivre. La résolution des coréférences garantit que les résumés et autres tâches à forte intensité de texte restent clairs et fluides.

Dans notre exemple, en utilisant des outils comme spaCy et neuralcoref, l'ordinateur identifie les coréférences suivantes : « je » fait référence au locuteur et apparaît deux fois dans le texte. « Vous » désigne directement Caton, la personne à laquelle vous vous adressez. Cette corrélation peut nous sembler triviale, mais pour une machine, elle est le résultat d’algorithmes sophistiqués travaillant en coulisses pour imiter notre compréhension naturelle.

Grâce à ces connexions établies, les machines peuvent parcourir le texte de manière plus fluide, transformant des données fragmentées en informations cohérentes.

Un résultat attendu de ce processus serait quelque chose comme :

```shellsession
[Je : [je, je], toi : [toi, Caton]]
```

## Conclusion : Mettre tout cela ensemble

La PNL peut sembler intimidante au début, mais lorsque vous la décomposez (tokenisation, marquage POS, NER, analyse des sentiments et résolution de coréférence), elle devient plus accessible. Chacune de ces techniques joue un rôle essentiel pour aider les machines à comprendre le langage humain. Nous n'avons pas couvert toutes les techniques possibles dans le domaine, mais c'est peut-être un bon aperçu pour vous donner une idée de ce qui se passe dans les coulisses du langage machine.

Le point essentiel à retenir est que la PNL vise à permettre aux machines de traiter et de comprendre le langage humain de manière significative. Que vous analysiez des sentiments, étiquetiez des parties du discours ou identifiiez des entités clés, ces éléments de base sont essentiels pour créer des systèmes PNL efficaces.

En démystifiant ces concepts, j’espère que vous vous sentirez plus connecté à la technologie qui alimente une grande partie de notre monde numérique. Et peut-être que cette nouvelle compréhension vous incitera à approfondir la PNL ou simplement à mieux apprécier la beauté du langage.