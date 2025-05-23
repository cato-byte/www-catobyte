## Comprendre les réseaux neuronaux

##### Publié le {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Image créée par ChatGPT, OpenAI. 7 octobre 2024](../../images/understanding_neural_networks_title_img.webp)

Bonjour à tous! Aujourd’hui, je souhaite passer en revue et donner une introduction de base aux réseaux neuronaux afin que nous puissions comprendre en termes très généraux la technologie qui fait fonctionner les modèles d’IA. J'ai un autre article sur [NLP](../post/nlp_introduction.html) si vous souhaitez approfondir, je pense que cela pourrait être utile, ainsi qu'un autre ensemble de techniques qui permettent à des outils comme Gemini et ChatGPT de comprendre ce que vous essayez de dire.

Vous pouvez trouver une bonne introduction dans cet article du MIT [https://news.mit.edu/2017/explained-neural-networks-deep-learning-0414], à partir duquel j'ai tiré quelques idées pour écrire cet article. Je vous recommande également de lire mon autre article [une introduction simple à l'apprentissage automatique](../a_simple_introduction_to_machine_learning.html) afin que vous puissiez avoir une base de base sur l'apprentissage automatique.


### 1. Que sont les réseaux neuronaux ?

Un réseau neuronal est un modèle informatique inspiré de la structure du cerveau humain, constitué de couches de neurones artificiels reliés par des « poids » qui déterminent la force des connexions entre eux. Ces réseaux peuvent apprendre à partir des données et s’améliorer au fil du temps grâce à un processus appelé formation. Dans sa forme la plus basique, un réseau neuronal comporte trois types de couches : la couche d'entrée, qui reçoit les données brutes (telles que les valeurs des pixels d'une image ou les mots d'une phrase) ; les couches cachées, qui effectuent le calcul réel et dont le nombre et la complexité déterminent la capacité du réseau à apprendre des caractéristiques profondes et abstraites ; et la couche de sortie, qui produit le résultat, comme la prédiction d'une étiquette (par exemple, « chat » ou « chien » pour un classificateur d'images ou le mot suivant dans une phrase pour un modèle de langage).

### 2. Composants de base d'un réseau neuronal

Pour comprendre comment fonctionne un réseau neuronal, nous devons décomposer ses composants fondamentaux. Au cœur du réseau se trouvent les neurones (également appelés nœuds), qui sont les unités de calcul de base. Chaque neurone reçoit des entrées, les traite en appliquant des poids et produit une sortie. La force des connexions entre les neurones est déterminée par des poids, qui contrôlent l’influence de la sortie d’un neurone sur l’entrée du neurone suivant. Au cours du processus d’entraînement, les poids apprennent l’importance de différentes caractéristiques. Un autre élément important est le biais, qui est une constante ajoutée à la somme pondérée des entrées, donnant au réseau la flexibilité nécessaire pour modéliser des relations complexes. Enfin, une fois les entrées additionnées et pondérées, le neurone applique une fonction d'activation (telle que ReLU ou Sigmoid) pour décider s'il faut « s'activer » (produire une valeur significative) ou rester inactif. Les fonctions d'activation introduisent la non-linéarité dans le réseau, lui permettant de résoudre des problèmes complexes que les modèles linéaires simples ne peuvent pas résoudre.


### 3. Formation, validation et recyclage

La formation d’un réseau neuronal implique la saisie de données et l’ajustement de leurs pondérations via un processus appelé rétropropagation. Au cours de la formation, le réseau se voit présenter un grand ensemble de données de paires d'entrée et de sortie, telles que des images et leurs étiquettes correspondantes. Pour chaque point de données, le réseau fait une prédiction et la différence entre le résultat prévu et le résultat réel (appelée perte) est calculée. Pour minimiser cette perte, le réseau utilise la rétropropagation et la descente de gradient. La rétropropagation consiste à propager la perte à travers le réseau pour mettre à jour les poids, tandis que la descente de gradient est un algorithme d'optimisation qui ajuste les poids pour minimiser la perte lors de l'itération suivante. La validation est cruciale pendant la formation pour surveiller les performances du réseau sur un ensemble de données indépendant, en garantissant qu'il ne se suradapte pas et qu'il peut bien se généraliser à de nouvelles données. Si les performances du réseau sont médiocres, il peut être nécessaire de recycler le réseau. Cela peut impliquer de modifier la structure du réseau, d’ajouter des couches supplémentaires ou d’appliquer des techniques de régularisation pour améliorer la généralisation et éviter le surajustement.

### 4. Un exemple concret

Voyons maintenant un exemple simple du monde réel pour étayer ces concepts. Essayons de prédire si un e-mail est un spam ou non. Dans cet exemple, nous voulons que notre réseau neuronal classe les e-mails comme spam ou non. Chaque e-mail est représenté comme un vecteur de caractéristiques, où chaque caractéristique pourrait indiquer : la présence de mots spécifiques, la fréquence de certains signes de ponctuation, la présence de certains mots-clés associés au spam (comme « gra »), etc.Le processus de transformation de caractéristiques telles que des mots, des signes de ponctuation ou d'autres données non numériques en valeurs numériques pour l'apprentissage automatique est communément appelé extraction de caractéristiques ou ingénierie de caractéristiques. Plus précisément, lorsqu'il s'agit de données textuelles, ce processus est souvent appelé vectorisation ou vectorisation de texte.

Examinons ce processus plus en détail :

Tout d’abord, le prétraitement du texte implique le nettoyage des données brutes. Cette étape comprend la suppression des éléments inutiles tels que les mots vides (tels que « le », « est », « dans »), les caractères spéciaux ou les chiffres (à moins qu'ils ne soient essentiels). Après avoir nettoyé le texte, il est souvent converti en minuscules pour garantir la cohérence, de sorte que des mots comme « Spam » et « spam » soient traités de la même manière. Par exemple, la phrase « Argent gratuit !!! Cliquez maintenant pour réclamer votre récompense !!! » devient « argent gratuit, cliquez maintenant pour réclamer votre récompense ».

Le processus de transformation de fonctionnalités telles que des mots, des signes de ponctuation ou d'autres données non numériques en valeurs numériques pour l'apprentissage automatique est appelé extraction de fonctionnalités ou ingénierie de fonctionnalités. Plus précisément, lorsque l’on travaille avec des données textuelles, cette transformation est souvent appelée vectorisation ou vectorisation de texte. Ceci est essentiel pour les modèles d’apprentissage automatique, car ils nécessitent des entrées numériques pour effectuer des prédictions ou des classifications.

Passons en revue les étapes d'extraction de fonctionnalités et de vectorisation dans le contexte d'une tâche de classification de spam, où l'objectif est de classer si un e-mail est un spam ou non en fonction de la présence de certains mots, signes de ponctuation et autres fonctionnalités pertinentes.

Tout d’abord, le prétraitement du texte implique le nettoyage des données brutes. Cette étape comprend la suppression des éléments inutiles, tels que les mots vides (tels que « le », « est », « dans »), les caractères spéciaux ou les chiffres (à moins qu'ils ne soient essentiels). Une fois le texte nettoyé, il est souvent converti en minuscules pour garantir la cohérence, de sorte que des mots comme « Spam » et « spam » sont traités de la même manière. Par exemple, la phrase « Argent gratuit !!! Cliquez maintenant pour réclamer votre récompense !!! » devient « argent gratuit, cliquez maintenant pour réclamer votre récompense ».

Ensuite, nous extrayons les fonctionnalités du texte nettoyé. Les caractéristiques communes incluent la fréquence des mots, la fréquence de ponctuation, la présence de mots spécifiques (tels que « gratuit » ou « gagner » qui sont associés au spam) et la longueur du message. Ces fonctionnalités peuvent fournir des informations utiles pour distinguer les courriers indésirables des courriers non indésirables.

Une fois les caractéristiques identifiées, l’étape suivante est la vectorisation, où les données textuelles sont converties en un format numérique qu’un modèle d’apprentissage automatique peut traiter. Une méthode courante est le Bag of Words (BoW), où un vocabulaire est créé à partir de tous les mots uniques de l'ensemble de données d'entraînement. Pour chaque document (email), un vecteur est créé en fonction de la fréquence de chaque mot de ce vocabulaire. Par exemple, si le vocabulaire est composé de mots tels que « gratuit », « argent », « réclamation » et « récompense », chaque e-mail sera représenté par un vecteur qui compte le nombre de fois que chaque mot apparaît dans cet e-mail.

Exemple:
Pour les prières :

E-mail 1 : « Argent gratuit, réclamez votre récompense maintenant ! »
E-mail 2 : « Achetez maintenant, offre spéciale sur les produits ! »
Vocabulaire : ["gratuit", "argent", "réclamer", "le vôtre", "récompense", "maintenant", "acheter", "spécial", "offre", "sur", "produits"]

Vecteur de courrier électronique 1 : [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
Vecteur de courrier électronique 2 : [0, 0, 0, 0, 1, 1, 1, 1, 1]

Chaque valeur du vecteur représente la fréquence du mot correspondant dans l’e-mail.

Une autre technique de vectorisation est la fréquence des termes-fréquence inverse des documents (TF-IDF), qui ajuste les fréquences des mots en prenant en compte la fréquence ou la rareté d'un mot dans tous les documents. Cette méthode permet de mettre en évidence les mots qui apparaissent fréquemment dans un document particulier mais qui sont rares dans l’ensemble des données, ce qui les rend plus utiles pour les tâches de classification.

Dans certains cas, le codage One-Hot est utilisé, en particulier pour les fonctionnalités catégorielles. Par exemple, si vous vérifiez la présence de certains mots ou signes de ponctuation, vous pouvez attribuer une valeur binaire (1 pour la présence, 0 pour l'absence). Par exemple, si vous vérifiez les mots « argent » et « gratuit », un e-mail contenant les deux mots pourrait être représenté par le vecteur \[1, 1\], tandis qu'un e-mail ne contenant aucun d'eux pourrait être représenté par le vecteur \[1, 1\].ils seraient représentés par \[0, 0\].

Enfin, après avoir appliqué la vectorisation, toutes les fonctionnalités sont combinées dans un vecteur de fonctionnalités final. Ce vecteur, qui comprend les fréquences des mots, le nombre de signes de ponctuation et d’autres caractéristiques, sert d’entrée à un algorithme d’apprentissage automatique. Par exemple, le vecteur de caractéristiques d'un e-mail pourrait ressembler à ceci : \[3 (gratuit), 1 (argent), 0 (offre), 2 (points d'exclamation), 5 (longueur)\

En bref, la transformation de données non numériques, telles que des mots et des signes de ponctuation, en valeurs numériques est appelée vectorisation ou extraction de caractéristiques. En appliquant des méthodes telles que Bag of Words, TF-IDF et One-Hot Encoding, nous pouvons convertir les données textuelles dans un format adapté aux modèles d’apprentissage automatique. Ces méthodes aident à capturer les modèles et les caractéristiques essentiels des données qui sont importantes pour des tâches telles que la classification du spam.

Ensuite, nous définissons l’architecture de notre réseau neuronal. Dans cet exemple, la couche d’entrée contiendra un neurone pour chaque caractéristique extraite de l’e-mail (par exemple, la fréquence des mots ou le nombre de caractères). Les neurones d'entrée sont connectés à une couche cachée, où nous spécifions le nombre de neurones en fonction de la complexité du problème (par exemple, 64 neurones dans une couche cachée). Ces neurones appliquent une fonction d'activation telle que ReLU pour ajouter de la non-linéarité, permettant au réseau d'apprendre des relations complexes entre les fonctionnalités. La couche de sortie finale comporte deux neurones, un pour chaque classe : « spam » et « non-spam », qui génèrent des probabilités pour chaque classe. L'utilisation de la fonction d'activation softmax garantit que les résultats sont des probabilités dont la somme est égale à 1, indiquant la probabilité qu'un e-mail appartienne à chaque classe.

Pendant la formation, chaque e-mail passe par le réseau dans un processus appelé propagation directe. Le réseau calcule une somme pondérée des entrées de chaque neurone, applique des fonctions d'activation et génère une prédiction (probabilité d'être un spam ou non). Nous utilisons ensuite une fonction de perte, telle que l'entropie croisée catégorielle, pour mesurer la différence entre la prédiction du réseau et la véritable étiquette de courrier électronique.

Pour améliorer la précision, nous appliquons la rétropropagation pour ajuster les poids en fonction de la perte. Dans la rétropropagation, la perte est propagée vers l'arrière à travers le réseau, calculant dans quelle mesure chaque poids a contribué à l'erreur. À l’aide d’un algorithme d’optimisation tel que la descente de gradient, les poids sont ajustés pour minimiser l’erreur. Ce processus est répété sur plusieurs époques, où chaque époque représente un passage à travers l’ensemble des données d’entraînement.

Pendant la formation, nous validons périodiquement les performances du modèle sur un ensemble de données de validation pour détecter le surajustement. Si le modèle fonctionne bien sur les données d'entraînement mais mal sur les données de validation, nous devrons peut-être ajuster les hyperparamètres (par exemple, le taux d'apprentissage, le nombre de couches) ou introduire des techniques de régularisation pour l'aider à se généraliser aux nouveaux e-mails.

Enfin, une fois la formation terminée et que le modèle fonctionne bien sur l’ensemble de données de validation, nous le testons sur l’ensemble de données de test pour confirmer qu’il peut classer avec précision les e-mails invisibles. En suivant ce flux de travail, le réseau neuronal apprend à partir des exemples étiquetés, affine sa compréhension de ce qui distingue le spam des e-mails légitimes et devient un classificateur fiable pour détecter le spam dans les applications du monde réel.


### 5. De quelle quantité de données un réseau neuronal a-t-il besoin ?

La quantité de données dépend de la complexité du problème. Les tâches simples, telles que la reconnaissance de nombres manuscrits, peuvent nécessiter moins de données, tandis que les tâches plus complexes, telles que la classification d'images ou le traitement du langage naturel, nécessitent de grandes quantités de données pour bien généraliser et éviter le surajustement.

### 6. Que sont les poids et comment sont-ils déterminés ?

Les poids représentent la force des connexions entre les neurones, initialement établies de manière aléatoire mais affinées au cours de l'entraînement. Au fur et à mesure que le réseau apprend, les pondérations sont ajustées pour réduire la valeur de la fonction de perte. Grâce à ce processus d’optimisation, le réseau devient plus précis, améliorant ainsi ses capacités prédictives.

### 7. Comment les réseaux neuronaux traitent les images et le texte

Bien que les concepts de base des réseaux neuronaux (poids, neurones, fonctions d'activation) soient les mêmes, la structure et la conception des réseaux pour les images et le texte peuvent différer considérablement :

Réseaux neuronaux pour le traitement d'images : ces rCes réseaux sont généralement des réseaux neuronaux convolutifs (CNN), conçus pour traiter des données de type grille, telles que les pixels d'une image. Les CNN utilisent des couches spécialisées appelées couches convolutives qui appliquent des filtres à l'image et capturent des caractéristiques telles que les bords, les textures et les motifs à différents niveaux. Cette approche hiérarchique aide les CNN à apprendre à reconnaître des objets complexes à partir de modèles simples.

Réseaux neuronaux pour le traitement de texte : les réseaux neuronaux basés sur du texte utilisent généralement des réseaux neuronaux récurrents (RNN) ou des transformateurs. Les RNN sont conçus pour gérer des données séquentielles (telles que les mots d'une phrase) et maintenir un état interne qui les aide à « se souvenir » des entrées précédentes. Ceci est crucial pour comprendre le contexte de la langue. Les modèles modernes comme Transformers (utilisés dans des modèles comme GPT-4) s'appuient sur des mécanismes d'attention pour comprendre les relations entre les mots sans avoir besoin de les traiter séquentiellement, permettant une compréhension du langage plus efficace et évolutive.


### 8. Similitudes entre les réseaux d'images et de textes

Malgré ces différences, les réseaux neuronaux pour les images et le texte partagent plusieurs similitudes :

Architecture en couches : les réseaux d'images et de texte utilisent plusieurs couches (entrée, masquée et sortie) pour extraire des fonctionnalités et faire des prédictions.

Pondérations et rétropropagation : Le processus d’ajustement des pondérations à l’aide de la rétropropagation et de la descente de gradient s’applique aux deux types de réseaux.

Fonctions d'activation : les fonctions d'activation non linéaires (telles que ReLU) sont utilisées dans les deux types de réseaux pour introduire la non-linéarité, permettant au modèle de capturer des relations complexes.

### 9. Différences clés

Structure des données : les images sont en 2D (ou 3D avec des canaux de couleur), donc des couches convolutives et un pooling sont utilisés pour traiter les relations spatiales. Le texte, en revanche, est séquentiel, les réseaux ont donc besoin de mécanismes pour capturer l’ordre des mots et leurs dépendances.

Prétraitement : les données d’image doivent souvent être redimensionnées, normalisées ou agrandies (par exemple, pivotées ou retournées) pour aider le réseau à se généraliser. Les données textuelles nécessitent une tokenisation (décomposition des phrases en mots ou en caractères) et peuvent impliquer l'intégration des mots dans des vecteurs continus.

### Conclusion

Les réseaux neuronaux sont des outils puissants qui permettent à l’IA de s’attaquer à des problèmes complexes dans des domaines tels que la vision par ordinateur et le traitement du langage naturel. Au cœur de ces réseaux se trouvent des composants simples (neurones, poids et fonctions d’activation), mais leur véritable force réside dans leur capacité à apprendre et à s’adapter grâce à des processus tels que l’entraînement, la rétropropagation et la validation. Qu'ils traitent des images ou du texte, les réseaux neuronaux partagent les mêmes principes fondamentaux, mais adaptent leurs architectures à la nature spécifique des données qu'ils traitent, ce qui les rend polyvalents et efficaces dans un large éventail d'applications.