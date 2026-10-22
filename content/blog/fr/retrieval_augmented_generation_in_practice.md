## La génération augmentée par récupération (RAG) en 2026 : fonctionnement, améliorations et mesure

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![La génération augmentée par récupération en 2026](../../images/retrieval_augmented_generation_in_practice_title_img.png)

*Article technique*

## Qu'est-ce que le RAG ?

Un modèle de langage connaît ce que contenaient ses données d'entraînement, figées à une date limite, et rien des documents, tickets, contrats ou tables de votre entreprise. La **génération augmentée par récupération** (RAG, pour *retrieval-augmented generation*) règle ce problème au moment de la requête : avant que le modèle réponde, le système *récupère* les informations pertinentes dans vos sources, *augmente* le prompt avec elles, et le modèle *génère* une réponse fondée sur ces éléments. Le [guide prescriptif d'AWS sur le RAG](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/introduction.html) le décrit comme un modèle qui consulte une source de données faisant autorité, extérieure à ses données d'entraînement, avant de répondre.

La formation d'OpenAI consacrée à la construction de systèmes RAG prend un exemple simple : un client demande « quelle est votre politique de retour ? », le système cherche dans la base de connaissances des politiques, trouve les règles (remboursement intégral jusqu'à 14 jours, un bon d'achat de la moitié de la valeur jusqu'à 30 jours), et le modèle répond en langage clair avec ces conditions exactes. Sans récupération, le modèle inventerait une politique plausible.

Le RAG compte parce qu'il apporte quatre choses qu'un modèle seul ne peut pas offrir :

- **Des connaissances privées et à jour**, actualisées par réindexation plutôt que par réentraînement.
- **Des citations**, pour que les utilisateurs et les auditeurs vérifient la source de chaque affirmation.
- **Un contrôle d'accès**, car la récupération peut respecter qui a le droit de voir quel document.
- **Moins d'hallucinations**, quand le prompt demande au modèle de répondre uniquement à partir des éléments fournis et de s'abstenir sinon.

Pour les data engineers, le RAG est aussi un terrain connu. L'essentiel du travail n'est pas le modèle : c'est l'ingestion, l'extraction du texte, le découpage, les métadonnées, l'indexation incrémentale, la fraîcheur, les droits et l'évaluation. Autrement dit, un pipeline de données dont le consommateur se trouve être un modèle de langage. Les prompts d'exemple sont en anglais, comme on les écrit souvent dans le code de production.

## Avez-vous besoin du RAG ?

La formation d'OpenAI place les tâches sur un spectre selon la quantité de connaissances externes qu'elles exigent :

1. **Prompt et raisonnement.** La tâche se résout avec des instructions et des connaissances générales : réécrire un texte, classer, planifier à partir de contraintes.
2. **Contexte fourni.** Un petit ensemble connu de documents tient directement dans le prompt : comparer trois politiques, résumer un rapport joint.
3. **RAG.** Le système doit chercher dans des sources privées, changeantes ou volumineuses au moment de l'exécution : bases de connaissances du support, documentation produit, questions sur des politiques avec citations.
4. **RAG agentique.** Le modèle planifie ses propres recherches, choisit outils et sources et combine les éléments en plusieurs étapes : recherche à plusieurs sauts entre systèmes.

Choisissez le niveau le plus bas qui fonctionne. Les fenêtres de contexte sont devenues si grandes que l'[article d'Anthropic sur la contextual retrieval](https://www.anthropic.com/news/contextual-retrieval) conseille de se passer du RAG pour les bases de connaissances de moins de 200 000 tokens environ (quelque 500 pages) : mettez tout dans le prompt et utilisez la mise en cache des prompts, qui selon l'article rend les requêtes répétées plus de deux fois plus rapides et jusqu'à 90 % moins chères. Le RAG devient rentable quand le corpus est plus gros, change souvent ou exige des droits par utilisateur.

RAG et fine-tuning répondent à des problèmes différents. Le fine-tuning change *la façon* dont un modèle se comporte (format, style, une compétence étroite) ; le RAG change *ce qu'il sait* au moment de répondre. Pour des connaissances qui évoluent, le RAG est presque toujours la bonne première étape.

## Le pipeline

Un système RAG comporte une partie hors ligne, qui prépare les connaissances, et une partie en ligne, qui répond à chaque question :

```text
OFFLINE (indexing)
sources ─► parse ─► clean ─► chunk ─► enrich (metadata, context) ─► embed ─► index
                                                                    (vector + keyword)
ONLINE (per question)
question ─► rewrite / decompose / extract filters ─► retrieve (hybrid + filters)
         ─► rerank ─► build prompt with top chunks ─► generate grounded answer + citations
                                                          │
EVALUATION ◄──────────────── golden questions, metrics per stage ◄──┘
```

La formation d'OpenAI regroupe les techniques selon les mêmes quatre étapes : préparation des données, traitement de l'entrée, récupération et génération de la réponse. La suite de l'article suit cet ordre.

## Préparation des données

### Choisir et décrire ses sources

La récupération ne peut pas trouver ce qui n'est pas indexé, et elle trouve sans difficulté ce qui ne devrait pas l'être. Les bonnes pratiques d'OpenAI : n'indexer que des sources approuvées et à jour, avec des responsables identifiés, et associer à chaque chunk son périmètre, sa date, ses droits et un lien vers la source. Sa liste d'écueils courants est une liste de qualité des données : des documents en double ou contradictoires produisent des réponses incohérentes, et le contenu retiré ou les droits périmés restent récupérables si le pipeline ne les supprime pas. Les suppressions et changements de droits doivent atteindre l'index aussi sûrement que les nouveaux documents.

### Le découpage (chunking)

Les documents sont découpés en passages assez petits pour être récupérés précisément et assez grands pour avoir du sens seuls. Les principales stratégies, dans l'ordre où je les essaierais :

| Stratégie | Découpage | Adaptée à |
|---|---|---|
| Selon la structure | Titres, sections, paragraphes, tableaux | Documentation, politiques, Markdown, HTML |
| Taille fixe avec chevauchement | N tokens avec un peu de chevauchement | Une base fiable pour du contenu irrégulier |
| Fenêtres de phrases | Phrases complètes, avec leurs voisines comme contexte | Prose |
| Frontières sémantiques | Changements de sujet détectés par embeddings | Longs documents mêlant des sujets ; plus coûteux |

Le [cookbook RAG d'Anthropic](https://platform.claude.com/cookbook/capabilities-retrieval-augmented-generation-guide) découpe sa documentation par titre, stocke chaque chunk avec son titre et son URL, puis calcule l'embedding du titre avec le texte. Ce petit geste garde un chunk comme « Limites : 100 requêtes par minute » rattaché à l'API *qu'il décrit*. Le chevauchement protège les idées à cheval sur une frontière, mais trop de chevauchement remplit l'index de doublons. Réglez la taille et le chevauchement par l'évaluation, pas à l'intuition.

### Ajouter du contexte à chaque chunk

Un chunk perd souvent son sens une fois détaché de son document : « Le chiffre d'affaires a progressé de 3 % par rapport au trimestre précédent » ne dit ni quelle entreprise ni quel trimestre. La technique de **contextual retrieval** d'Anthropic demande à un modèle une ou deux phrases qui situent chaque chunk dans son document, et les ajoute en tête avant le calcul de l'embedding et l'indexation par mots-clés. Un prompt dans l'esprit du leur :

```text
<document>
{{WHOLE_DOCUMENT}}
</document>

Here is a chunk from the document above:
<chunk>
{{CHUNK_CONTENT}}
</chunk>

Write one or two sentences that situate this chunk within the overall document, to
improve search retrieval of the chunk. Mention the entities, dates and section it
refers to. Answer only with the context, nothing else.
```

Avec la mise en cache des prompts, le document entier est traité une fois puis réutilisé pour chacun de ses chunks ; c'est ainsi qu'Anthropic estime le coût ponctuel à environ un dollar par million de tokens de documents. D'autres enrichissements fonctionnent de la même manière : des résumés de chaque document (l'« indexation par résumés » du cookbook), des synonymes et mots-clés, ou des descriptions textuelles d'images. La formation d'OpenAI ajoute une mise en garde : partez de la source d'origine, n'ajoutez des signaux générés que lorsque les tests de récupération révèlent un manque, et relisez le texte généré avant de l'indexer.

### Images et documents numérisés

La recherche textuelle ne voit pas ce qui ne figure que dans une image. Le [cookbook d'OpenAI sur la compréhension d'images avec le RAG](https://developers.openai.com/cookbook/examples/multimodal/image_understanding_with_rag) convertit chaque image en une description d'une ligne grâce à un modèle de vision, l'ajoute au texte associé et indexe le résultat. Dans son exemple de livraison de repas, une recherche texte seul sur les commentaires concernant des spaghettis ne trouvait que « les pâtes étaient trop cuites », tandis que l'index enrichi des images faisait aussi remonter la photo « d'une assiette de spaghettis à la sauce tomate, joliment dressée ». La contrepartie, c'est davantage de tokens par élément : mesurez si le gain le justifie.

### Embeddings et index

Un modèle d'embeddings transforme chaque chunk en vecteur, et des textes de sens voisin pointent dans des directions proches même s'ils emploient des mots différents : « Comment renvoyer un article endommagé ? » se retrouve près de « Les produits défectueux peuvent être renvoyés sous 30 jours » et loin de « Où modifier mon adresse de facturation ? ». La similarité se mesure en général par le cosinus.

Les vecteurs vont dans un index : une base vectorielle dédiée, un moteur de recherche gérant les vecteurs comme OpenSearch, ou `pgvector` dans le PostgreSQL que vous exploitez déjà. Pour la plupart des équipes, le meilleur index est celui que leur plateforme exploite déjà bien, avec recherche par mots-clés, filtres de métadonnées et contrôle d'accès à côté de la recherche vectorielle.

## Traitement de l'entrée

Les utilisateurs posent leurs questions avec leurs mots ; les documents sont écrits avec ceux d'autres personnes. La formation d'OpenAI liste quatre transformations, à n'appliquer que lorsque les évaluations révèlent un échec de récupération qu'elles corrigent :

- **Réécriture de la requête** : reformuler la demande avec le vocabulaire de la source sans en changer l'intention (« mon MX-200 est arrivé cassé » devient « politique de retour des articles endommagés MX-200 »).
- **Décomposition** : découper les questions composées et chercher pour chaque partie (« Puis-je le renvoyer et qui valide les exceptions ? »).
- **Extraction d'entités et filtres** : transformer produit, région, date ou version en filtres structurés.
- **HyDE** (hypothetical document embeddings) : demander au modèle une réponse hypothétique et chercher avec elle, ce qui aide les questions courtes et conceptuelles à trouver de longs passages.

Un seul appel peut faire les trois premières :

```text
You prepare search requests for a product-support knowledge base.

Given the customer's message, return JSON with:
- "queries": one to three search queries in the vocabulary of policy documents,
  one per distinct question the customer asks. Keep product names and error codes
  exactly as written.
- "filters": product, region (two-letter code) and purchase_date (ISO 8601) when
  they are stated or clearly implied, otherwise null.

Do not answer the question. Do not add constraints the customer didn't express.

<message>{{CUSTOMER_MESSAGE}}</message>
```

La dernière consigne vise le principal risque signalé par la formation : des réécritures qui perdent les mots-clés ou les contraintes de l'utilisateur sans améliorer la récupération.

## La récupération

### Recherche sémantique, par mots-clés et hybride

La recherche sémantique trouve les paraphrases mais peine sur les identifiants exacts ; un code d'erreur comme `ERR-4297` ou une référence produit se trouve mieux par mots-clés. BM25, l'algorithme de référence de la recherche par mots-clés, récompense les termes rares : un code présent dans 2 documents sur 10 000 obtient un score élevé, tandis que le mot « erreur », présent dans 7 800, ne compte presque pas. La formation d'OpenAI le résume en une ligne : la recherche sémantique trouve les paraphrases, les mots-clés protègent les identifiants exacts, et la recherche hybride fusionne les classements, pas les scores bruts.

La méthode de fusion habituelle est la **reciprocal rank fusion** (RRF), qui n'utilise que la position de chaque document dans chaque liste de résultats :

```python
def reciprocal_rank_fusion(rankings: list[list[str]], k: int = 60) -> list[str]:
    """Merge ranked lists of document IDs; k dampens the weight of the top ranks."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for position, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + position)
    return sorted(scores, key=scores.get, reverse=True)

top = reciprocal_rank_fusion([vector_search(query, 50), bm25_search(query, 50)])[:20]
```

Ajoutez des **filtres de métadonnées** pour tout ce qui est structuré : une question sur « la politique du MX-200 pour les achats en Californie en 2026 » ne devrait chercher que dans les documents de ce produit, de cette région et de cette période, et uniquement dans ceux que l'utilisateur a le droit de lire. Filtrer par droits au moment de la récupération est le seul moyen fiable d'empêcher un système RAG de citer des documents à des personnes qui ne devraient pas les voir.

Les chiffres montrent l'intérêt de combiner les signaux. Dans les expériences d'Anthropic sur la contextual retrieval, mesurées comme la part de chunks pertinents absents des 20 premiers résultats, les embeddings contextuels ont réduit les échecs de 35 %, l'ajout d'un BM25 contextuel a porté la réduction à 49 %, et l'ajout d'un reranking a atteint 67 % (de 5,7 % à 1,9 % de récupérations ratées).

### La récupération en plusieurs étapes

Certaines réponses sont dispersées. « Quelles équipes dépendent du projet Aurora, et qui les dirige ? » exige une recherche pour trouver les équipes dépendantes et une seconde pour trouver leurs responsables. Une récupération en une seule étape n'y arrive pas ; une chaîne de récupérations, ou un agent qui décide quoi chercher ensuite, le peut. C'est là que le RAG devient **agentique** : la récupération est exposée comme un outil (souvent à côté de requêtes SQL, d'API et de recherche web), et le modèle planifie les recherches, lit les résultats et cherche à nouveau jusqu'à réunir les éléments. Il traite des questions plus difficiles au prix de plus de latence, de coût et de variabilité : gardez un pipeline simple pour les questions courantes et réservez les agents aux questions à plusieurs sauts.

Une approche voisine, pour les questions qui portent sur tout un corpus (« Quels sont les grands thèmes de ces 5 000 tickets de support ? »), est [GraphRAG](https://www.microsoft.com/en-us/research/project/graphrag/) de Microsoft Research, qui extrait entités et relations dans un graphe de connaissances et résume ses communautés, au lieu de récupérer des chunks isolés.

## Le reranking

La récupération de premier niveau est rapide mais grossière : elle compare un vecteur de requête à des millions de vecteurs de chunks. Le reranking prend les 50 à 150 meilleurs candidats, évalue chacun plus soigneusement face à la question et garde les 5 à 20 meilleurs. La formation d'OpenAI en décrit quatre types, chacun corrigeant un échec différent, avec un coût et une latence qui croissent à peu près dans cet ordre :

- **Des règles métier** qui valorisent des signaux connus : mettre en avant les politiques approuvées et à jour, rétrograder les brouillons.
- **Un recalcul lexical** quand des termes exacts comptent, comme un identifiant CVE et un nom de paquet ensemble.
- **Des modèles cross-encoder** qui lisent requête et passage ensemble, et distinguent « retours après ouverture de la boîte » de « retours d'articles non ouverts ».
- **Des rerankers à base de LLM** qui appliquent une grille qualitative, par exemple préférer des chiffres audités à un résumé marketing.

Un prompt de reranking par LLM peut être court :

```text
Question: {{QUESTION}}

Below are candidate passages. Score each from 0 to 3 for how directly it helps
answer the question: 3 = answers it, 2 = contains part of the answer, 1 = related
background, 0 = irrelevant. Prefer current, official policy over drafts or FAQs.

{{PASSAGES_WITH_IDS}}

Return JSON: [{"id": "...", "score": n}, ...] for every passage.
```

Validez le choix avec des métriques de récupération (MRR, nDCG), la latence au 95e centile et le coût par requête, pas avec quelques vérifications au jugé.

## Générer la réponse

### Dépenser la fenêtre de contexte à bon escient

La fenêtre de contexte est un budget partagé entre les instructions, la question, l'historique de conversation, les éléments récupérés et la place pour la réponse. La règle de décision d'OpenAI est la bonne : récupérer assez d'éléments pour bien répondre, sans noyer le modèle sous des chunks marginaux, qui diluent son attention et augmentent le coût. L'ordre compte aussi : Anthropic recommande de placer les longs documents avant la question et les instructions.

### Un contrat de réponse fondée

Le prompt de réponse fixe les règles qui rendent un système RAG digne de confiance : répondre à partir des éléments, les citer, s'abstenir ou demander quand ils manquent, et signaler les contradictions au lieu de trancher en silence. Une version dont je partirais :

```text
You answer customer questions about our return and warranty policies.

<sources>
<source id="S1" title="Return policy" updated="2026-09-01">{{CHUNK_1}}</source>
<source id="S2" title="Damaged items" updated="2026-06-12">{{CHUNK_2}}</source>
<source id="S3" title="California exceptions" updated="2026-03-30">{{CHUNK_3}}</source>
</sources>

<question>{{QUESTION}}</question>

Rules:
1. Use only the sources above. Don't fill gaps with assumptions or general knowledge.
2. After each claim, cite its source in brackets, for example [S1].
3. If the sources don't contain the answer, say what is missing. If it depends on
   information the customer didn't give (purchase date, region), ask for it.
4. If sources conflict, prefer the most recently updated one and mention the conflict.
5. Answer in at most four sentences, in the customer's language.
```

Le cookbook d'Anthropic utilise une version plus simple de la règle 1 (« remain faithful to the underlying context ») et l'accompagne d'une consigne pour supprimer les préambules. Pour les réponses importantes, une seconde vérification peut contrôler que chaque source citée appuie réellement son affirmation, ce qui sert aussi à mesurer la qualité des citations.

## L'évaluation

Le RAG échoue à des endroits précis, et un score global de bout en bout masque lesquels. La formation d'OpenAI associe les métriques à l'étape qui échoue :

| Étape | Question | Métriques |
|---|---|---|
| Sources et index | La réponse est-elle présente, à jour et lisible ? | Couverture, fraîcheur, qualité d'extraction, doublons |
| Récupération | Les bons éléments sont-ils apparus en tête ? | Hit rate@k, recall@k, MRR, nDCG |
| Génération | La réponse est-elle restée fidèle aux éléments ? | Fidélité, appui des citations, abstention |
| De bout en bout | L'utilisateur a-t-il obtenu une réponse utile à un coût acceptable ? | Pertinence, réussite de la tâche, latence, coût |

Le cookbook d'Anthropic fait exactement cela sur un jeu de 100 questions portant sur sa propre documentation, en mesurant la récupération (précision, rappel, F1, MRR) séparément de l'exactitude de bout en bout jugée par un modèle. Son pipeline de base (chunks par titre, embeddings, les 3 meilleurs) atteignait 71 % d'exactitude de bout en bout ; l'ajout de l'indexation par résumés et du reranking a fait passer le MRR de 0,74 à 0,87 et l'exactitude à 81 %. La formation d'OpenAI montre un assistant de services financiers passé d'environ 45 % à 98 % d'exactitude en cumulant expériences de découpage et d'embeddings, expansion de requêtes, HyDE, embeddings affinés, reranking, classification, appels d'outils et prompt engineering, chaque étape étant mesurée par rapport au même objectif. L'intérêt de ces deux exemples n'est pas dans les techniques elles-mêmes, mais dans le fait que chaque changement a été mesuré.

Pour évaluer à grande échelle, utilisez un modèle comme juge, avec une grille stricte et un verdict facile à analyser, et vérifiez à la main un échantillon de ses décisions :

```text
You are grading answers from a question-answering system.

<question>{{QUESTION}}</question>
<reference_answer>{{REFERENCE}}</reference_answer>
<system_answer>{{ANSWER}}</system_answer>

The system answer is correct if it contains the key facts of the reference answer
and contradicts none of them. Ignore differences in wording, length and order. Mark
it incorrect if a critical fact is missing or wrong, or if it answers a different
question. If the reference says the information is unavailable, the system answer
is correct only if it also declines to answer.

Return JSON: {"explanation": "<one or two sentences>", "is_correct": true|false}
```

Faites ensuite de l'évaluation une barrière de non-régression, comme le recommande la formation d'OpenAI : un jeu de référence de questions représentatives avec réponses et passages attendus ; des cas difficiles d'ambiguïté, de fraîcheur, de droits, d'entrées malveillantes et de questions sans réponse ; chaque changement d'ingestion, de classement, de prompt, de routage ou de modèle testé par rapport à une référence avant la mise en production ; et de nouveaux cas ajoutés à partir des retours des utilisateurs et des échecs.

## Construire ou acheter

Inutile d'assembler chaque pièce soi-même. Le guide d'AWS compare les [options entièrement managées](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/rag-fully-managed.html), Knowledge Bases for Amazon Bedrock, Amazon Q Business et SageMaker Canvas, qui se connectent à des sources comme SharePoint, Confluence ou des sites web et prennent en charge une grande partie du pipeline, avec des architectures sur mesure construites à partir d'un moteur de récupération (Amazon Kendra, OpenSearch, Aurora avec pgvector, etc.) et d'un modèle sur Bedrock. OpenAI propose une recherche de fichiers hébergée avec des vector stores via son Responses API, et les plateformes de données ont la leur (Cortex Search chez Snowflake, Vector Search chez Databricks). L'arbitrage est partout le même : les services managés suppriment un travail peu différenciant mais limitent la personnalisation du découpage, du classement et de l'évaluation. Un service managé est un bon moyen d'obtenir une référence et un jeu de test ; passez à un pipeline sur mesure quand les évaluations révèlent un écart que seul plus de contrôle peut combler.

## Sécurité et gouvernance

Le RAG élargit la surface d'attaque de deux façons. Chaque document indexé devient un canal d'**injection de prompt indirecte** : une page web ou un ticket piégés peuvent contenir des instructions que le modèle suivra, donc le texte récupéré doit être marqué comme des données et les outils que le modèle peut appeler doivent être limités. Et l'index devient une copie de données sensibles : appliquez les droits du système source au moment de la récupération, masquez ou excluez les données personnelles dont les réponses n'ont pas besoin, propagez les suppressions et journalisez les documents récupérés pour chaque réponse afin de pouvoir l'auditer.

## Une liste de contrôle

- Décidez si vous avez besoin du RAG : les petits corpus tiennent dans le prompt avec la mise en cache.
- Traitez l'ingestion comme un pipeline de données : sources avec responsable, métadonnées, droits, mises à jour incrémentales et suppressions.
- Commencez par un découpage selon la structure, avec des chunks qui portent leur titre ou le contexte du document.
- Utilisez une recherche hybride avec filtres de métadonnées ; ajoutez du reranking quand les métriques le justifient.
- Rédigez un prompt de réponse fondée avec citations, règles d'abstention et gestion des contradictions.
- Constituez un jeu de référence avant d'optimiser, mesurez chaque étape séparément et conditionnez chaque changement à ces mesures.
- Réservez le RAG agentique aux questions à plusieurs sauts qu'une seule récupération ne peut pas traiter.

## Sources

- AWS : [Retrieval Augmented Generation options and architectures on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/introduction.html), [Fully managed RAG options on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/rag-fully-managed.html)
- Anthropic : [Retrieval-augmented generation cookbook](https://platform.claude.com/cookbook/capabilities-retrieval-augmented-generation-guide), [Introducing contextual retrieval](https://www.anthropic.com/news/contextual-retrieval)
- OpenAI : [Retrieval-augmented generation builder training (OpenAI Academy)](https://d2xo500swnpgl1.cloudfront.net/slide-upload/oaiacademy/Builder-Bootcamp-RAG-cd2cd443-9b6e-42ec-8300-0c084268f7d1-1789064989962.pdf), [Image understanding with RAG](https://developers.openai.com/cookbook/examples/multimodal/image_understanding_with_rag)
- Microsoft Research : [GraphRAG](https://www.microsoft.com/en-us/research/project/graphrag/)
