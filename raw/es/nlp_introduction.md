## ¿Cómo nos entienden las máquinas? Introducción al PLN o NLP(Procesamiento de lenguaje natural)

##### Publicado el {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Imagen creada por ChatGPT, OpenAI. 7 de octubre de 2024](../../images/nlp_introduction_title_img.webp)

¿Alguna vez te has preguntado como herramientas como los asistentes de IA entienden tus preguntas y ordenes y producir una respuesta que a primera vista al menos parece coherente? ¿Como puede una máquina que en su nivel más elemental realiza cálculos sobre bytes lograr estos sorprendentes resultados?

Para completar esta hazaña, se utilizan técnicas de procesamiento del lenguage natural (PLM), un subcampo de la informática que combina el estudio de la gramática y el aprendizaje de máquina para permitir a los ordenadores comprender el lenguaje humano y producir respuestas coherentes. 

El PLN ha ganado mucha notoriedad en el último año gracias al surgimiento de los LLMs o modelos de lenguaje de gran tamaño. Aunque el nombre LLM puede que no te diga mucho a primera vista ya has interactuado probablemente con alguno de ellos: ChatGPT, Gemini y DeepSeek entre otros son modelos de lenguaje de gran tamaño. 

También existen SLMs o modelos de lenguaje de temaño pequeño, estos suelen estar entrenados con un grupo de datos más pequeño, menos parámetros y suelen enfocarse en un dominio específico a diferencia de los LLMs que tratan de ser más generalistas y producir respuestas en diferentes campos del conocimiento. 

A continuación te voy a exponer algunas técnicas de PLN para que puedas comprender que sucede detraś de escena. 

En este artículo, exploraremos algunos conceptos básicos de PLN, incluida la tokenización, el etiquetado de partes del discurso (POS) y el reconocimiento de entidades nombradas (NER).

Aunque gracias al procesamiento del lenguaje natural hemos logrado una interacción muy fluida entre las personas y las máquinas abriendo nuevas oportunidades en diferentes campos, aún no se ha logrado que un modelo tenga un razonamiento verdadero y autónomo y pase la prueba de Turing (Prueba que evalua la capacidad de una máquina para exhibir un comportamiento inteligente similar al de un  humano).  

Ahora veamos más en detalle algunos de estos procesos básicos.

### Tokenización

La tokenización es el primer paso básico para procesar el lenguaje, consiste en dividir el texto en fragmentos más pequeños llamados tokens, que pueden ser palabras o frases. Este paso permite a las máquinas trabajar de forma más precisa los textos y extraer información relevante. 

Veamos un ejemplo, tomando como base las siguientes frases:

**"Tengo ganas de salir del bosque e ir al campo hoy. El sol brilla, los pájaros cantan y estoy de muy buen humor. ¿No te pasa lo mismo, Cato?"**

Los tokens de este texto serían cada palabra y signo de puntuación que se encuentre en el mismo. Se pueden crear scripts que realicen esta tarea de forma automática. Es importante recalcar que es importante conservar el orden de los tokens, ya que es información valiosa que nos puede indicar el significado de una palabra o a que familia gramatical pertenece. El resultado se vería algo aśi. 


```python
['Tengo','ganas','de','salir','de','el','bosque','e','ir','a','el','campo','hoy','.','El','sol','brilla',',','los','pajaros','cantan','y','estoy','de','muy','buen','humor','.','¿','No','te','pasa','lo','mismo',',','Cato','?']
```

Ahora tenemos una lista de tokens de palabras. Quizás te preguntes por qué dividí la palabra "del" en los tokens "de" y "el" y al en los tokens "a. Esto se debe a que "del" es una contracción de "de" y "el", y esta separación es importante para ayudar a los sistemas de PLN a procesar sus componentes gramaticales por separado. "de" es una preposición y "el" es un artículo. En español solo existen oficialmente 2 contracciones del y al pero son más comunes en otros idiomas.



También es usual la tokenización por oraciones. Al obtener tokens de frases enteras se facilita la tarea de entender el contexto general de una discusión o argumento, se suele usar en sistemas de traducción automática o resumen.  

De nuestro ejemplo obtendríamos los siguientes tokens oracionales:

**['Tengo ganas de salir del bosque e ir al campo hoy','El sol brilla, los pájaros cantan y estoy de muy buen humor','¿No te pasa lo mismo, Cato?']**

El resultado de la tokenización es un insumo para otros procesos como la extracción de características, cuyo objetivo es obtener una representación numérica de las palabras. Esta representación numérica luego puede usarse como insumo para entrenar o consultar un modelo de aprendizaje profundo. Detallar el proceso de extracción de características (feature extraction) puede ser un artículo en sí mismo. Para simplificar diré que esta representación numérica puede indicar el número de caracteres de una palabra, cuantas veces aparece en una oración, empieza por mayúscula, qué tan rara es, etc.  

En resumen la tokenización prepara el texto para un análisis posterior, lo que facilita la comprensión de los significados de las palabras, la detección de patrones y la realización de otras tareas, como la traducción o el análisis de sentimientos.

### Etiquetado de partes del discurso (POS)

Para permitir que una máquina procese lenguage natural es necesario que el lenguaje haya sido modelado de alguna manera. Esto quiere decir que los fenómenos que ocurren en un lenguaje estén organizados y capturados de tal manera que puedan ser usados para predecir o reorganizar futuros usos del lenguaje.

Una forma de llegar a este modelado es el etiquetado gramátical o etiquetado de partes del discurso (POS), otra tarea básica en cualquier sistema de NLP. Para realizar este paso existen herramientas que proveen la funcionalidad de etiquetado automático y son usadas en el campo del PLN tales como spaCy y NLTK. Estos etiquetadores hacen uso de corpus lingüísticos, que son colecciones de frases con su estructura gramatical anotada.  

La creación de estos corpus u colecciones de oraciones etiquetadas, han sido proyectos que han tardado años. Se han hecho de forma semiatumática mezclando etiquetado automático y correción manual. En sus inicios hicieron uso de un algoritmo llamado PARTS() que hacía un primer etiquetado. Luego un lingüista revisaba esta versión inicial y la corregía.

El proyecto Penn TreeBank desarrollado en la universidad de Pensilvania  entre los años 1989 y 1996 es una implementación concreta de uno de estos conjuntos de oraciones, específicamente para el idioma inglés. El producto final de este proyecto es un conjunto de más de 7 millones de palabras con etiquetas de parte del discurso (POS) y análisis sintáctico de alrededor de  3 millones de frases. 

[Aqui puedes ver más información sobre el Proyecto  Penn TreeBank](https://www.researchgate.net/publication/2873803_The_Penn_Treebank_An_overview#:~:text=The%20Penn%20Treebank%2C%20in%20its,spoken%20text%20annotated%20for%20speech)

Con el uso de etiquetadores automáticos basados en estos corpus podemos asignar cada palabra dentro de una frase a una de las categorías gramáticales definidas en el corpus. Esto es importante para la comprensión del contexto y significado por parte de las máquinas. 

Sin el etiquetado POS, podríamos malinterpretar oraciones como:

**Te cuento una historia interesante.** (Aquí, "cuento" es un verbo, que significa contar algo). **Me gusta leer un buen cuento antes de dormir.** (En este caso, "cuento" es un sustantivo).



El  conjunto de etiquetas de Penn Treebank es específico para el inglés, pero no es adaptable a otros idiomas con palabras ,estructuras gramaticales y evolución distintas. 

Para abordar esta limitación, existe  el proyeto ['Universal Dependencies project'](https://universaldependencies.org/introduction.html) (UPOS), que plantea crear un banco de estructuras gramáticales que sea consistente para varios idiomas. Este enfoque es útil para aplicaciones multilingües, debido a su compatibilidad con más de 100 idiomas.

También hay investigación y desarrollo para crear corpus específicos a otros idiomas como este [artículo](https://www.researchgate.net/publication/39436708_Anotacion_semiautomatica_con_papeles_tematicos_de_los_corpus_CESS-ECE) donde se habla de la creación de un corpus para Español y Catalán.

A continuación se muestran dos tablas con algunas categorías de etiquetas gramaticales de los corpus Penn TreeBank y UPOS.

**Penn Treebank** 


|Etiqueta | Categoría gramatical | Definición |
|------------|------------|------------|
|NN | SUSTANTIVO | Nombres de personas, lugares, cosas o ideas|
|VB | VERBO | Palabras que describen acciones, estados o sucesos|
|JJ | ADJETIVO | Palabras que describen o modifican sustantivos|
|RB | ADVERBIO | Palabras que modifican verbos, adjetivos u otros adverbios|
|PRP | PRONOMBRE | Palabras que reemplazan sustantivos|
|DT | DETERMINADOR | Palabras que introducen sustantivos|
|IN | PREPOSICIÓN | Palabras que muestran relaciones entre sustantivos o pronombres y otras palabras en una oración.|
|CC | CONJUNCIÓN | Palabras que conectan cláusulas, oraciones o palabras.|
|AUX | VERBO AUXILIAR | Verbos utilizados para formar tiempos, modos o voces de otros verbos.|
|PP | PARTÍCULA | Palabras que forman parte de los verbos frasales |

**Universal Dependencies Project UPOS**

|Etiqueta | Categoría gramatical | Definición |
|------------|------------|------------|
|ADJ |Adjetivo| Describe un sustantivo (p. ej., feliz, verde, pequeño).|
|ADP |Adposición| Preposiciones y posposiciones (p. ej., en, sobre, a).|
|ADV |Adverbio| Modifica verbos, adjetivos u otros adverbios (p. ej., rápidamente, muy, aquí).|
|AUX |Verbo auxiliar| Verbos que ayudan a formar tiempo, modo o voz (p. ej., es, tener, voluntad).|
|CCONJ| Conjunción coordinante| Une palabras, frases u oraciones como iguales (p. ej., y, pero, o).|
|DET| Determinante| Modifica un sustantivo (p. ej., el, un, algún, mi).|
|INTJ| Interjección| Expresa emoción o sonido (p. ej., wow, ay, uh-huh).|
|NOUN| Sustantivo| Nombra personas, lugares, cosas o ideas (p. ej., gato, ciudad, libertad).|
|NUM |Numeral| Indica números (p. ej., uno, dos, 42).|
|PART| Partícula| Palabras funcionales o morfemas (p. ej., not, to in not go o to go).|
|PRON| Pronombre| Sustituye a un sustantivo (p. ej., she, it, themselves).|
|PROPN| Nombre propio| Nombra entidades específicas (p. ej.,  John, Paris, Google).|
|PUNCT| Puntuación| Cualquier signo de puntuación (p. ej., ., ;, ?).|
|SCONJ| Conjunción subordinada| Vincula cláusulas con dependencia (p. ej., because, however, if).|
|SYM | Símbolo| Símbolos no alfanuméricos (p. ej., $, %, +, @).|
|VERB| Verbo| Acciones, eventos o estados (p. ej., ejecutar, convertirse, existir).|
|X|Otro| Categorización general para palabras no clasificadas (p. ej., frases extranjeras o errores tipográficos)|

El etiquetado gramatical se puede realizar de diferentes maneras, algunas de ellas son:

**Sistemas basados ​​en reglas**:  Utilizan reglas lingüísticas para categorizar las palabras. Pueden haber reglas tan simples como Colombia es un sustantivo (NOUN). Otras algo más complejas como reemplazar la categoría de sustantivo (NOUN) por verbo (VERB) si va precedida por pronombre. Otro ejemplo sería decir que todas las palabras terminadas en -mente son adverbios de modo como tranquilamente, calladamente y serenamente. Pero esta regla no funcionaria para las palabras demente, clemente, vehemente, lamente, aumente etc que son adjetivos y verbos pero no adverbios de modo. Este modelado del lenguaje de acuerdo a reglas es bastante rígido y presenta dificultades para manejar la ambigüedad o etiquetar palabras desconocidas. 

**Modelos estadísticos**: 

Los enfoques estadísticos clasifican las probabilidades de que un token pertenezca a las distintas categorías escogiendo la categoría más probable. 

Uno de estos modelos estadísticos son las cadenas ocultas de Markov. Estos modelos tienen algo llamado estados ocultos. Estas serían las categorías gramaticales como determinante, verbo adjetivo etcétera. El modelo calcula dos tipos de probabilidades las probabilidades de transición y las probabilidades de emisión para una palabra.  

Las probabilidades de transición calculan por ejemplo que tan probable que después de un artículo siga un sustantivo. Las probabilidades de emisión calculan que tan probable que el token que se esté analizando pertenezca a una determianda categoría. Mirando este enfoque más amplio , que tiene en cuenta la secuencia de palabras el modelo logra una aproximación más precisa que los sistemas basados en reglas. Una ventaja de estos modelos es que son livianos y pueden ejecutarse en recursos computacionales limitados y para datos pequeños, como un conjunto de datos específico del dominio. Pero  pueden ser más propenso a errores que los modelos apoyados en redes neuronales que describiré a continuación.

**Modelos de aprendizaje automático**: Los etiquetadores gramaticales modernos utilizan una mezcla de métodos estadísticos y redes neuronales para etiquetar las palabras del lenguaje. Se entrenan redes neuronales con  bases de datos del lenguaje tales como Penn TreeBank y Universal Dependencies para crear etiquetadores que predigan las categorías gramaticales de los tokens de acuerdo a una entrada de texto que el modelo no ha visto antes. Estos son los sistemas que han demostrado ser más flexibles al manejar mejor la ambigüedad y el etiquetado de palabras no conocidas.   

 Para más detalles, puede consultar mis publicaciones sobre [aprendizaje automático](../post/a_simple_introduction_to_machine_learning.html) o [aprendizaje profundo](../post/understanding_neural_networks.html). 

Volviendo a nuestro ejemplo y teniendo una breve vista de los modelos  Después de pasar los tokens a través del sistema de etiquetas upos, así es como podría verse el resultado.

```python
tokens_upos = [
    ("Tengo", "VERB"),("ganas", "NOUN"),("de", "ADP"),("salir", "VERB"),("de", "ADP"),("el", "DET"),("bosque", "NOUN"),("e", "CCONJ"),("ir", "VERB"),("a", "ADP"),("el", "DET"),("campo", "NOUN"),("hoy", "ADV"),(".", "PUNCT"),("El", "DET"),("sol", "NOUN"),("brilla", "VERB"),(",", "PUNCT"),("los", "DET"),("pájaros", "NOUN"),("cantan", "VERB"),("y", "CCONJ"),("estoy", "VERB"),("de", "ADP"),("muy", "ADV"),("buen", "ADJ"),("humor", "NOUN"),(".", "PUNCT"),("¿", "PUNCT"),("No", "ADV"),("te", "PRON"),("pasa", "VERB"),("lo", "PRON"),("mismo", "ADJ"),(",", "PUNCT"),("Cato", "PROPN"),("?", "PUNCT")
]
```

### Reconocimiento de entidades con nombre NER

[Para información más detallada sobre la construccion de corpus y el proceso de reconocimiento de entidades](https://www.researchgate.net/publication/374674771_COMPREHENSIVE_OVERVIEW_OF_NAMED_ENTITY_RECOGNITION_MODELS_DOMAIN-SPECIFIC_APPLICATIONS_AND_CHALLENGES)

En el reconocimiento de entidades o NER (Named entity recognition) intentamos reconocer las entidades que se puedan encontrar al interior de un texto, una entidad puede ser un país por ejemplo, una figura pública, una organización, un producto etcétera.  

Existe un concepto llamado base de conocimiento 

Dependiendo de la tarea en cuestion tambien hay bases de conocimiento específicas como  ViBert y BioBert especializadas en campos específicos como las finanzas y la biología.

El reconocimiento de entidades o NER (Named Entity Reognition) es un proceso mediante el cual se procede a reconocer entidades dentro de un texto tales como lugares, personas, productos, organizaciones, nacionalidades, fechas, valores numéricos entre otros. 

Para realizarlo se necesita una base de conocimiento que va a contener una lista de palabras y los posibles lugares a los que podría pertenecer. 

Mediante el NER podemos extraer información relevante de un texto y transformarla en información estructurada (como una tabla), que se puede usar para análisis posteriores. 


Puedes encontrar más informacion sobre NER [aquí](https://www.ibm.com/es-es/think/topics/named-entity-recognition)

Un ejemplo de NER, en una oración sería:

"Cato ganó el premio en Bogotá la semana pasada",

NER etiquetaría:

"Cato" como PERSONA,
"premio" como EVENTO y
"Bogotá" como LUGAR.

NER es útil para extraer información valiosa de textos extensos. Puede ayudar a resumir texto, responder preguntas y mejorar las tareas de análisis de sentimientos. Las etiquetas NER suelen determinarse en función de ontologías o vocabularios creados por humanos.

A continuación, se incluye una lista de algunas categorías NER comunes:

|Categoría NER | Definición | Ejemplo |
|------------|------------|------------|
|PER (Persona) |Nombres de personas| Isabel Allende, Mon Laferte |
|ORG (Organización) |Nombres de organizaciones o empresas| Umbrella Corporation, Nokia|
|LOC (Localización) |Nombres de lugares geográficos| Bogotá, Parque Tayrona, Sagrada Familia|
|GPE (Entidad Geopolítica) |Regiones políticas, como países, ciudades o estados| Colombia, Sucre |
|FECHA| Expresiones de fecha u hora específicas | 1 de septiembre de 2024, mañana |
|HORA| Horas específicas| 15:00, mediodía|
|DINERO| Montos monetarios| 50.000 pesos, 10 euros|
|PORCENTAJE| Porcentajes| 15 por ciento, 50%|
|FAC (Instalación) |Edificios, aeropuertos, carreteras| Casa de la Moneda, aeropuerto El Dorado, carretera Panamericana|
|NORP | Nacionalidades, religiones, grupos políticos| Colombia, catolicismo, partido verde|
|PROD| Producto| Café Juan Valdez, Flores, Renault|
|OBRA_DE_ARTE| Obras creativas| Relatos salvajes, Las meninas|
|IDIOMA| Idiomas| Español, Wayuu, Criollo, Inglés|
|EVENTO |Eventos con nombre| Reinado de la Panela, Juegos Panamericanos|

Y volviendo a nuestra oración inicial podríamos esperar un resultado como el siguiente.

```shellsession
Reconocimiento de entidad con nombre:
Entidad: hoy, Etiqueta: FECHA, Inicio: 22, Fin: 27
Entidad: Cato, Etiqueta: ORG, Inicio: 123, Fin: 127
```

NER es esencial para extraer información estructurada de texto no estructurado, lo que es útil en tareas como la recuperación y el resumen de información.

### Análisis de sentimientos

El análisis de sentimientos implica determinar el sentimiento o la emoción detrás de un fragmento de texto. Esto puede ser complicado porque el sarcasmo, la ironía o el contexto pueden cambiar drásticamente el significado. Por ejemplo, la frase "¡Genial, justo lo que necesitaba!" puede parecer positiva, pero es probable que sea negativa debido al tono.

El análisis de sentimientos clasifica una oración como positiva, neutral o negativa y, a veces, incluso de manera más precisa, como fuertemente positiva o fuertemente negativa. Esto es particularmente útil para procesar los comentarios de los clientes o comprender la opinión pública. Los sistemas de PNL modernos pueden ir más allá de lo positivo, lo neutral y lo negativo y detectar más emociones en el texto.

Aquí hay una lista de algunas de las emociones que estos sistemas pueden detectar.

| Emoción | Tono emocional | Ejemplo|
|---------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| Felicidad | Positivo | ¡Finalmente logré mi objetivo y me siento muy feliz por eso! |
| Emoción | Positivo | No veo la hora de empezar mañana en mi nuevo trabajo. ¡Será increíble! |
| Gratitud | Positivo | Muchas gracias por ayudarme en este momento difícil. Significa mucho para mí. |
| Enojo | Negativo | No puedo creer que me hayan mentido. ¡Estoy furioso! |
| Tristeza | Negativo | Me siento muy deprimido hoy. Todo me recuerda lo que he perdido. |
| Miedo | Negativo | Caminar solo en este callejón oscuro me aterroriza. |
| Decepción | Negativo | Realmente esperaba un mejor resultado, pero creo que tendré que intentarlo de nuevo. |
| Indiferencia | Neutral | Realmente no tengo una opinión sobre este tema. No me afecta. |
| Curiosidad | Contexto específico | ¡Tengo mucha curiosidad por saber cómo resultará este experimento! Tengo curiosidad por saber por qué me están evitando. Me parece sospechoso. |
| Confusión | Contexto específico | ¡Este rompecabezas es confuso, pero me estoy divirtiendo resolviéndolo! Estoy confundida sobre lo que está pasando y me está poniendo ansiosa. |
| Esperanza | Contexto específico | Espero que esta nueva oportunidad traiga el cambio que he estado esperando. Espero que me perdonen, pero en el fondo, temo que no lo hagan. |
| Frustración | Contexto específico | Estoy frustrada con este proyecto, pero sé que me sentiré orgullosa una vez que lo termine. Este tráfico es tan frustrante que me está haciendo perder toda la tarde. |
| Amor | Contexto específico | Me encanta pasar tiempo con mi familia; es muy gratificante. Los amo, pero esta relación está destruyendo mi salud mental. |
| Culpa | Contexto específico | Me siento culpable por lo que dije, así que voy a disculparme y arreglar las cosas. |

Sin embargo, las emociones son complicadas y el contexto es esencial. Por ejemplo, "No soy infeliz" es técnicamente negativo, pero implica algo positivo. El análisis de sentimientos utiliza modelos de aprendizaje automático para dar cuenta de esas sutilezas, aunque incluso los mejores modelos pueden tener problemas con el sarcasmo o la ambigüedad.

### Resolución de correferencia

¿Alguna vez has leído una historia en la que aparecen personajes como "él", "ella" o "ellos" y te encuentras tratando de reconstruir de quién se está hablando? Esa es la esencia de la resolución de correferencia: determinar cuándo diferentes palabras o frases se refieren en realidad a la misma persona o cosa.

Veamos esto más de cerca con nuestra oración de ejemplo: "Tengo ganas de salir hoy, el sol brilla, los pájaros cantan y estoy de muy buen humor. ¿No te pasa lo mismo, Cato?". En esta alegre narración, "tú" está claramente dirigido a Cato, mientras que "yo" pertenece al hablante. Para nosotros, esto es sencillo: nuestras mentes conectan los puntos sin problemas. ¿Pero para una computadora? Es como desenredar una red compleja. La resolución de correferencia les da a las máquinas las herramientas para seguir estas conexiones, lo que garantiza que puedan averiguar quién es quién, incluso en textos largos e intrincados.

Esta habilidad desempeña un papel fundamental en aplicaciones como la redacción de resúmenes, donde es crucial comprender a quién o a qué se refiere cada pronombre. Imagine un resumen en el que se utilice "él" o "ellos" de forma ambigua y sin contexto: parecería inconexo y difícil de seguir. La resolución de correferencias garantiza que los resúmenes y otras tareas con mucho texto mantengan la claridad y la fluidez.

En nuestro ejemplo, utilizando herramientas como spaCy y neuralcoref, la computadora identifica las siguientes correferencias: "Yo" se refiere al hablante y aparece dos veces en el texto. "Tú" apunta directamente a Cato, la persona a la que se dirige. Esta correlación puede parecernos trivial, pero para una máquina es el resultado de sofisticados algoritmos que funcionan entre bastidores para imitar nuestra comprensión natural.

Con estas conexiones establecidas, las máquinas pueden navegar por el texto de forma más fluida, transformando los datos fragmentados en información coherente.

Un resultado esperado de este proceso sería algo como:

```shellsession
[I: [I, I], you: [you, Cato]]
```

## Conclusión: Uniendo todo

El PLN puede sonar intimidante al principio, pero cuando lo desglosas (tokenización, etiquetado POS, NER, análisis de sentimientos y resolución de correferencia) se vuelve más accesible. Cada una de estas técnicas juega un papel vital para ayudar a las máquinas a comprender el lenguaje humano. No hemos cubierto todas las técnicas posibles, pero tal vez esta sea una buena descripción general para que te hagas una idea de lo que ocurre detrás de escena en el lenguaje de las máquinas.

La conclusión clave es que el PLN tiene que ver con permitir que las máquinas procesen y comprendan el lenguaje humano de una manera significativa. Ya sea que estés analizando sentimientos, etiquetando partes del discurso o identificando entidades clave, estos bloques de construcción son esenciales para crear sistemas de PNL efectivos.

Al desmitificar estos conceptos, espero que te sientas más conectado con la tecnología que impulsa gran parte de nuestro mundo digital. Y tal vez esta nueva comprensión te inspire a profundizar en el PLN o simplemente a obtener una mayor apreciación por la belleza del lenguaje.

