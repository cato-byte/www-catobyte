## NLP A detailed Intro

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Image created by ChatGPT, OpenAI. 7th October 2024 ](../../images/nlp_introduction_title_img.webp)


Have you ever wondered how computers can understand and generate human language? Let's explore this fascinating topic together. So, what does NLP stand for? It stands for Natural Language Processing, which refers to the use of computational techniques to derive meaning from text input and to create streams of text that are comprehensible to humans. In this article, we’ll explore some core concepts of NLP, including tokenization, part-of-speech (POS) tagging, and named entity recognition (NER).

We use language so intuitively that we rarely stop to think about how complex this process really is. For a machine, even at a high level, text is just a sequence of characters contained in a file. But for the machine, these are all the same: a sequence of bytes stored somewhere in its memory.

I must tell you that although NLP has made huge advances and is partly responsible for the AI boom we’re experiencing today, there are still improvements to be made, such as achieving true reasoning.

Without further ado, let's explore some techniques that machines can apply to derive meaning from text.

### Tokenization

Tokenization is the first step in NLP. It’s the process of splitting text into smaller chunks called tokens, which are often words or phrases. This is crucial because machines need these smaller chunks to analyze and process the text effectively.


Let’s use the following sentences as an example:

**"I feel like going out today, the sun is shinning, the birds are singing and I am in a great mood. Don't you feel the same Cato?"**

We  need a script or program to split this plain text into what are called tokens ,usually words and punctuation marks. This is one of the most basic steps in NLP and a necessary input for other NLP tasks. Without this step a machine would only see a list of characters. 


```python
['I','feel','like','going','out','today',',','the','sun','is','shinning',',','the','birds','are','singing','and','I','am','in','a','great','mood','.','Do','n\'t','you','feel','the','same','Cato','?']
 ```

Straightforward, right? There are exceptions of course but the process is relatively simple. We now have a list of word tokens. You might be wondering why I split the word "Don’t" into the tokens 'Do' and 'n't'. This is because "Don’t" is a contraction of "Do" and "not," and this separation is important to help NLP systems process its grammatical components separately. "Do" is a verb, and "not" is a negation.

Next, we need a list of sentence tokens, which divides the text into different sentences—this is important for translation.

**['I feel like going out today, the sun is shinning, the birds are singing and I am in a great mood.','Don't you feel the same Cato?']**

Now you might be wondering: Why do we need a list of sentences if we already have a list of words? Why is it important to make that distinction? Well, we can use word tokens for understanding context, as each word carries a specific meaning or function and is important to analyze separately. For grammatical analysis, as we’ll see when we talk about POS tagging, this distinction is essential.

We can use word tokens for undestanding context, each word carries a specific meaning or function and is important to analize them separately. For grammatical analysis that we will see below when we talk about POS tagging. For feature extraction these are a series of techniques that allow to have numerical representations of words, important for NLP modeling, going into full detail can be an article in itself so I will basically say that there you can give numbers to word for example counting their number of charactesrs, how many times they appear in a sentence, wether they are capitalized or not how rare they are etc. 

For sentence tokens, it’s more about context—words get meaning depending on their position and the sentence they are found in. It’s also used for higher-level analysis, such as sentiment analysis and translation, since sentences are the natural translation units.

Tokenization is foundational because it prepares the text for further analysis, making it easier to understand word meanings, detect patterns, and perform other tasks like sentiment analysis.

### Part-of-speech POS tagging

Next, let's dive into part-of-speech (POS) tagging. This process assigns each word in a sentence a specific role, like noun, verb, or adjective. But why is it important?

Without POS tagging, we might misunderstand sentences like:

**I booked a flight.** (Here, "booked" is a verb, meaning to reserve something.) **I read a book.** (In this case, "read" is a verb, but "book" is a noun!)

Tags for defining the categories to which words belong are mostly standardized. A tag set commonly used in English is the Penn Treebank POS tag set, with over 36 categories. However, this tag set might not be ideal for other languages, as it was conceived with English grammar in mind. For other languages, the Universal POS (UPOS) tag system is often used, particularly for multilingual applications, because of its support for over 100 languages and its consistency across languages. There are special cases, such as Chinese, which uses its own dataset. UPOS has fewer tags than Penn Treebank, which can simplify parsing.

Here are two tables with some common NLP tag categories for both of these systems.

**Penn Treebank** 

|Tag | Grammatical category | Definiton |
|------------|------------|------------|
|NN	     |     NOUN      | Names of people, places, things, or ideas|
|VB	     |     VERB      | Words that describe actions, states, or occurrences|
|JJ      | ADJECTIVE     | Words that describe or modify nouns|
|RB	     |     ADVERB      | Words that modify verbs, adjectives, or other adverbs|
|PRP	     |     PRONOUN      | Words that replace noun|
|DT	     |     DETERMINER      | Words that introduce nouns|
|IN	     |     PREPOSITION     |  Words that show relationships between nouns or pronouns and other words in a sentence.|
|CC     |     CONJUNCTION      | Words that connect clauses, sentences, or words.|
|AUX	|  AUXILIARY  VERB      | Verbs used to form tenses, moods, or voices of other verbs.|
|PP	     |     PARTICLE      | Words that form part of phrasal verbs|

**UPOS Universal POS tag System** 

|Tag | Grammatical categoty | Definiton |
|------------|------------|------------|
|ADJ	|Adjective|	Describes a noun (e.g., happy, green, small).|
|ADP	|Adposition|	Prepositions and postpositions (e.g., in, on, at).|
|ADV	|Adverb|	Modifies verbs, adjectives, or other adverbs (e.g., quickly, very, here).|
|AUX	|Auxiliary Verb|	Verbs that help form tense, mood, or voice (e.g., is, have, will).|
|CCONJ|	Coordinating Conjunction|	Links words, phrases, or clauses as equals (e.g., and, but, or).|
|DET| Determiner|	Modifies a noun (e.g., the, a, some, my).|
|INTJ|	Interjection|	Expresses emotion or sound (e.g., wow, ouch, uh-huh).|
|NOUN|	Noun|	Names people, places, things, or ideas (e.g., cat, city, freedom).|
|NUM	|Numeral|	Indicates numbers (e.g., one, two, 42).|
|PART|	Particle|	Functional words or morphemes (e.g., not, to in not go or to go).|
|PRON|	Pronoun|	Substitutes for a noun (e.g., she, it, themselves).|
|PROPN|	Proper Noun|	Names specific entities (e.g., John, Paris, Google).|
|PUNCT|	Punctuation|	Any punctuation mark (e.g., ., ;, ?).|
|SCONJ|	Subordinating Conjunction|	Links clauses with dependency (e.g., because, although, if).|
|SYM	|Symbol|	Non-alphanumeric symbols (e.g., $, %, +, @).|
|VERB|	Verb|	Actions, events, or states (e.g., run, become, exist).|
|X|Other|	Catch-all for unclassified words (e.g., foreign phrases or typos)|


POS tagging can be done using various methods:

**Rules Based Systems** : These use predefined linguistic rules to assign a category to a token. For example, words ending in "ing" are likely verbs. This method is rigid and prone to ambiguity.

**Statistical Models** :These are mathematical frameworks used to understand relationships between variables. They ususally make explicit assumptions that explain the distribution of data points. they are interpretable and their goal is to understand the relationships between variables. In NLP they can work for simple cases. Hidden markov models is one of the statistical models used for NLP. It calculates the probability that a word belongs to a category using the following inputs. Annotated corpus of text, this is a set of sentences where each word is already annotated as belonging to a specific category (done by humans), and by using states. What do I mean by state is that the algorithm calculates the probability that a token is a verb for example if the previous token was a pronoun. It calcultes word by word only taking into account the previous word. One advantage of these models is that they are lightweight and they can run on limited computational resources and for small data such as a domain specific dataset. But one of its limitations is that it only takes into account the previous word which can be limiting as it does not take into account the whole context and can be more prone to errors. 

**Machine Learning Models**:  modern NLP systems rely on this technology to deal with context and handle ambiguous cases. The model is exposed to a high number of linguisting patterns already annotated to make its predictions. For more details you can check my posts about [machine learning](../post/a_simple_introduction_to_machine_learning.html) or [deep learning](../post/understanding_neural_networks.html). They require a large amount of data to train and they need a lot of computational resources to function properly, particularly access to GPUs. What is good about these models is that they can learn from context.

Since the example we are doing today is in English, passing the tokens through a machine learning model using treebank tags seems like an appropriate choice. After passing the tokens through the pos tag system here's how the result could look like. 

```python
[('I', 'PRP'), ('feel', 'VBP'), ('like', 'IN'), ('going', 'VBG'), ('out', 'RP'), 
 ('today', 'NN'), (',', ','), ('the', 'DT'), ('sun', 'NN'), ('is', 'VBZ'), 
 ('shining', 'VBG'), (',', ','), ('the', 'DT'), ('birds', 'NNS'), ('are', 'VBP'), 
 ('singing', 'VBG'), ('and', 'CC'), ('I', 'PRP'), ('am', 'VBP'), ('in', 'IN'), 
 ('a', 'DT'), ('great', 'JJ'), ('mood', 'NN'), ('.', '.'), ('Do', 'VB'), ("n't", 'RB'), 
 ('you', 'PRP'), ('feel', 'VB'), ('the', 'DT'), ('same', 'JJ'), ('Cato', 'NNP'), ('?', '.')]
 ```

 POS tagging helps machines understand not just individual words but also the structure of sentences, which is essential for tasks like machine translation and speech recognition.

### Named Entity recognition

Named Entity Recognition (NER) helps machines identify and categorize key elements in text, such as names, dates, and locations. For instance, in the sentence.:

"Cato won the award in Bogota last week,"

NER would label:

"Cato" as a PERSON,
"award" as an EVENT, and
"Bogota" as a LOCATION.


NER is useful for extracting valuable information from large texts. It can help summarize text, answer questions, and enhance sentiment analysis tasks.NER labels are often determined based on human-created ontologies or vocabularies. 


Here's a list of some common NER categories:

|NER Category | Definition | Example |
|------------|------------|------------|
|PER (Person) |Names of people|	Carlos Perez, Isabel Allende|
|ORG (Organization)	|Names of organizations or companies|	Umbrella Corporation, Nokia|
|LOC (Location)	|Names of geographic locations|	Bogota, Tayrona Park, Sagrada Familia|
|GPE (Geopolitical Entity)	|Political regions, such as countries, cities, or states| Colombia, Sucre	|
|DATE|	Specific date or time expressions |	September 1st, 2024, tomorrow |
|TIME| Specific times|	3 PM, noon|
|MONEY|	Monetary amounts|	50.000 pesos, 10 euros|
|PERCENT| Percentages| 15 per cent, 50%|
|FAC (Facility) |Buildings, airports, highways|	Casa de la Moneda ,El Dorado airport, Pan American Highway|
|NORP |	Nationalities, religions, political groupse| Colombian, catholicism, green party|
|PROD|	Product| Juan Valdez Coffee, Flowers, Renault|
|WORK_OF_ART|	Creative works|	Relatos salvajes, Las meninas|
|LANGUAGE|	Languages|	Spanish, Wayuu, Creole, English|
|EVENT	|Named events|	Reinado de la Panela, Pan American Games|

And going back to our initial sentence we could expect a result like the following. 


```shellsession
Named Entity Recognition:
Entity: today, Label: DATE, Start: 22, End: 27
Entity: Cato, Label: ORG, Start: 123, End: 127
```

NER is essential for extracting structured information from unstructured text, which is useful in tasks like information retrieval and summarization.

### Sentiment Analysis

Sentiment analysis involves determining the sentiment or emotion behind a piece of text. This can be tricky because sarcasm, irony, or context can drastically change the meaning. For instance, the phrase "Great, just what I needed!" may seem positive, but it’s likely negative due to tone.

Sentiment analysis categorizes a sentence as positive, neutral, or negative, and sometimes even more finely, as strongly positive or strongly negative. This is particularly useful for processing customer feedback or understanding public opinion. Modern nlp systems can go beyond positive neutral and negative and detect more emotions for text.

Here's a list of some of the emotions these systems are able to detect. 

| Emotion       | Emotional Tone   | Example|
|---------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| Happiness     | Positive         | I finally achieved my goal, and I feel so happy about it!                                                                                      |
| Excitement    | Positive         | I can’t wait to start my new job tomorrow—it’s going to be amazing!                                                                            |
| Gratitude     | Positive         | Thank you so much for helping me through this tough time—it means the world to me.                                                             |
| Anger         | Negative         | I can’t believe they lied to me—I’m furious!                                                                                                   |
| Sadness       | Negative         | I feel so down today; everything reminds me of what I’ve lost.                                                                                 |
| Fear          | Negative         | Walking alone in this dark alley is making me terrified.                                                                                       |
| Disappointment| Negative         | I was really hoping for a better result, but I guess I’ll have to try again.                                                                   |
| Indifference  | Neutral          | I don’t really have an opinion on this topic—it doesn’t affect me.                                                                             |
| Curiosity     | Context Specific | I’m so curious about how this experiment will turn out!  I’m curious why they’re avoiding me—it feels suspicious.                              |
| Confusion     | Context Specific | This puzzle is confusing, but I’m having fun figuring it out!  I’m confused about what’s happening, and it’s making me anxious.                |
| Hope          | Context Specific | I hope this new opportunity brings the change I’ve been waiting for. I hope they’ll forgive me, but deep down, I’m afraid they won’t.          |
| Frustration   | Context Specific | I’m frustrated with this project, but I know I’ll feel proud once I finish it. This traffic is so frustrating—it’s wasting my entire afternoon.|
| Love          | Context Specific | I love spending time with my family—it’s so fulfilling. I love them, but this relationship is destroying my mental health.                     |
| Guilt         | Context Specific | I feel guilty for what I said, so I’m going to apologize and make things right.                                                                |

However, emotions are tricky, and context is essential. For example, "I’m not unhappy" is technically negative but implies something positive. Sentiment analysis uses machine learning models to account for such subtleties, though even the best models can struggle with sarcasm or ambiguity.

### Coreference Resolution


Ever read a story where characters like "he," "she," or "they" keep showing up, and you find yourself piecing together who is being talked about? That’s the essence of coreference resolution—pinpointing when different words or phrases actually refer to the same person or thing.

Let’s take a closer look at this with our example sentence: “I feel like going out today, the sun is shining, the birds are singing, and I am in a great mood. Don’t you feel the same, Cato?” In this cheerful narrative, "you" is clearly directed at Cato, while "I" belongs to the speaker. For us, this is straightforward—our minds seamlessly connect the dots. But for a computer? It’s like untangling a complex web. Coreference resolution gives machines the tools to follow these connections, ensuring they can figure out who’s who, even in lengthy and intricate texts.

This skill plays a key role in applications like summarizing articles, where understanding who or what each pronoun refers to is crucial. Imagine a summary where "he" or "they" is used ambiguously without context—it would feel disjointed and hard to follow. Coreference resolution ensures that summaries, and other text-heavy tasks, maintain clarity and flow.

In our example, using tools like spaCy and neuralcoref, the computer identifies the following coreferences: “I” refers to the speaker, appearing twice in the text. “You” points directly to Cato, the person being addressed. This mapping might seem trivial to us, but for a machine, it’s the result of sophisticated algorithms working behind the scenes to mimic our natural understanding.

With these connections in place, machines can navigate text more fluidly, transforming fragmented data into coherent insights.

An expected output of this process would be something like: 

```shellsession
[I: [I, I], you: [you, Cato]]
```


## Conclusion: Bringing It All Together

NLP may sound intimidating at first, but when you break it down—tokenization, POS tagging, NER, sentiment analysis, and coreference resolution—it becomes more approachable. Each of these techniques plays a vital role in helping machines understand human language. We have not covered every possible technique in the field but maybe this is a good overniew so you get a sense of behind the scenes of machine language. 

The key takeaway is that NLP is all about enabling machines to process and understand human language in a meaningful way. Whether you're analyzing sentiment, tagging parts of speech, or identifying key entities, these building blocks are essential for creating effective NLP systems.

By demystifying these concepts, I hope you feel more connected to the technology that powers much of our digital world. And maybe this newfound understanding will inspire you to dive deeper into NLP or simply gain a greater appreciation for the beauty of language.

