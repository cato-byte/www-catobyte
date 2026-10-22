## Generación aumentada por recuperación (RAG) en 2026: cómo funciona, qué la mejora y cómo medirla

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Generación aumentada por recuperación en 2026](../../images/retrieval_augmented_generation_in_practice_title_img.png)

*Artículo técnico*

## Qué es RAG

Un modelo de lenguaje sabe lo que había en sus datos de entrenamiento, congelados en una fecha de corte, y nada sobre los documentos, tickets, contratos o tablas de tu empresa. La **generación aumentada por recuperación** (RAG, por sus siglas en inglés) lo resuelve en el momento de la solicitud: antes de que el modelo responda, el sistema *recupera* información relevante de tus fuentes, *aumenta* el prompt con ella y el modelo *genera* una respuesta basada en esa evidencia. La [guía prescriptiva de AWS sobre RAG](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/introduction.html) lo describe como un modelo que consulta una fuente de datos autorizada, externa a sus datos de entrenamiento, antes de responder.

La formación de OpenAI para construir sistemas RAG usa un ejemplo sencillo: un cliente pregunta "¿cuál es su política de devoluciones?", el sistema busca en la base de conocimiento de políticas, encuentra las reglas (reembolso total hasta 14 días, un bono por la mitad del valor hasta 30 días) y el modelo responde en lenguaje claro con esas condiciones exactas. Sin recuperación, el modelo inventaría una política verosímil.

RAG importa porque da cuatro cosas que un modelo solo no puede dar:

- **Conocimiento privado y actual**, que se actualiza reindexando en lugar de reentrenar.
- **Citas**, para que usuarios y auditores puedan comprobar la fuente de cada afirmación.
- **Control de acceso**, porque la recuperación puede respetar quién puede ver cada documento.
- **Menos alucinaciones**, cuando el prompt le pide al modelo responder solo con la evidencia y abstenerse si no la hay.

Para los ingenieros de datos, RAG es además terreno conocido. La mayor parte del trabajo no es el modelo: es ingesta, extracción de texto, chunking, metadatos, indexación incremental, frescura, permisos y evaluación. Es decir, un pipeline de datos cuyo consumidor resulta ser un modelo de lenguaje. Los prompts de ejemplo están en inglés, como suelen escribirse en código de producción.

## ¿Necesitas RAG?

La formación de OpenAI ubica las tareas en un espectro según cuánto conocimiento externo necesitan:

1. **Prompt y razonamiento.** La tarea se resuelve con instrucciones y conocimiento general: reescribir un texto, clasificar, planificar a partir de restricciones.
2. **Contexto suministrado.** Un conjunto pequeño y conocido de documentos cabe directamente en el prompt: comparar tres políticas, resumir un informe adjunto.
3. **RAG.** El sistema debe buscar en fuentes privadas, cambiantes o grandes en tiempo de ejecución: bases de conocimiento de soporte, documentación de producto, preguntas sobre políticas con citas.
4. **RAG agéntico.** El modelo planifica sus propias búsquedas, elige herramientas y fuentes y combina evidencia en varios pasos: investigación de varios saltos entre sistemas.

Elige el nivel más bajo que funcione. Las ventanas de contexto ya son tan grandes que el [artículo de Anthropic sobre contextual retrieval](https://www.anthropic.com/news/contextual-retrieval) aconseja prescindir de RAG con bases de conocimiento de menos de unos 200.000 tokens (unas 500 páginas): pon todo en el prompt y usa el caché de prompts, que según el artículo hace las solicitudes repetidas más de dos veces más rápidas y hasta un 90% más baratas. RAG compensa cuando el corpus es más grande, cambia a menudo o necesita permisos por usuario.

RAG y fine-tuning resuelven problemas distintos. El fine-tuning cambia *cómo* se comporta un modelo (formato, estilo, una habilidad concreta); RAG cambia *lo que sabe* al responder. Para conocimiento que cambia, RAG es casi siempre el primer paso correcto.

## El pipeline

Un sistema RAG tiene una parte offline, que prepara el conocimiento, y una parte online, que responde cada pregunta:

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

La formación de OpenAI agrupa las técnicas en las mismas cuatro etapas: preparación de datos, procesamiento de la entrada, recuperación y generación de la respuesta. El resto del artículo sigue ese orden.

## Preparación de datos

### Elige y describe tus fuentes

La recuperación no puede encontrar lo que no está indexado, y encuentra sin problema lo que no debería. Las buenas prácticas de OpenAI son indexar solo fuentes aprobadas y vigentes, con responsables claros, y adjuntar a cada chunk su alcance, fecha, permisos y enlace a la fuente. Su lista de errores comunes es una lista de calidad de datos: los documentos duplicados o contradictorios producen respuestas inconsistentes, y el contenido retirado o los permisos desactualizados siguen siendo recuperables si el pipeline no los elimina. Las eliminaciones y los cambios de permisos deben llegar al índice con la misma fiabilidad que los documentos nuevos.

### Chunking

Los documentos se dividen en pasajes lo bastante pequeños para recuperarlos con precisión y lo bastante grandes para tener sentido por sí solos. Las estrategias principales, en el orden en que las probaría:

| Estrategia | Cómo divide | Sirve para |
|---|---|---|
| Según la estructura | Encabezados, secciones, párrafos, tablas | Documentación, políticas, Markdown, HTML |
| Tamaño fijo con solapamiento | N tokens con algo de solapamiento | Una base confiable para contenido irregular |
| Ventanas de oraciones | Oraciones completas, con las vecinas como contexto | Prosa |
| Límites semánticos | Cambios de tema detectados con embeddings | Documentos largos que mezclan temas; más costoso |

El [cookbook de RAG de Anthropic](https://platform.claude.com/cookbook/capabilities-retrieval-augmented-generation-guide) divide su documentación por encabezados y guarda cada chunk con su encabezado y su URL, y luego calcula el embedding del encabezado junto con el texto. Ese pequeño paso mantiene un chunk como "Límites: 100 solicitudes por minuto" unido a *cuál* API describe. El solapamiento protege las ideas que cruzan un límite, pero demasiado llena el índice de duplicados. Ajusta el tamaño y el solapamiento con evaluaciones, no por intuición.

### Añade contexto a cada chunk

Un chunk suele perder sentido al separarlo de su documento: "Los ingresos crecieron un 3% respecto al trimestre anterior" no dice de qué empresa ni de qué trimestre. La técnica de **contextual retrieval** de Anthropic le pide a un modelo una o dos frases que sitúen cada chunk dentro de su documento, y las antepone antes de calcular el embedding y el índice de palabras clave. Un prompt en la línea del suyo:

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

Con el caché de prompts, el documento completo se procesa una vez y se reutiliza para cada uno de sus chunks; así estima Anthropic un costo único de alrededor de un dólar por millón de tokens de documentos. Otros enriquecimientos funcionan igual: resúmenes de cada documento (la "indexación por resúmenes" del cookbook), sinónimos y palabras clave, o descripciones en texto de imágenes. La formación de OpenAI añade una advertencia: parte de la fuente original, añade señales generadas solo cuando las pruebas de recuperación muestren un hueco y revisa el texto generado antes de indexarlo.

### Imágenes y documentos escaneados

La búsqueda de texto no ve lo que solo está en una imagen. El [cookbook de OpenAI sobre comprensión de imágenes con RAG](https://developers.openai.com/cookbook/examples/multimodal/image_understanding_with_rag) convierte cada imagen en una descripción de una línea con un modelo de visión, la añade al texto relacionado e indexa el resultado. En su ejemplo de pedidos de comida a domicilio, una búsqueda solo de texto sobre comentarios de espaguetis encontró únicamente "la pasta estaba demasiado cocida", mientras que el índice con imágenes también mostró la foto de "un plato de espaguetis en salsa de tomate, bien presentado". La contrapartida son más tokens por elemento, así que mide si la mejora lo justifica.

### Embeddings e índice

Un modelo de embeddings convierte cada chunk en un vector, y los textos de significado parecido apuntan en direcciones similares aunque usen palabras distintas: "¿Cómo devuelvo un artículo dañado?" queda cerca de "Los productos defectuosos se pueden devolver en un plazo de 30 días" y lejos de "¿Dónde actualizo mi dirección de facturación?". La similitud se mide normalmente con la similitud del coseno.

Los vectores van a un índice: una base de datos vectorial dedicada, un motor de búsqueda con soporte de vectores como OpenSearch, o `pgvector` en el PostgreSQL que ya operas. Para la mayoría de los equipos, el mejor índice es el que su plataforma ya opera bien, con búsqueda por palabras clave, filtros de metadatos y control de acceso junto a la búsqueda vectorial.

## Procesamiento de la entrada

Los usuarios preguntan con sus palabras; los documentos están escritos con las de otros. La formación de OpenAI lista cuatro transformaciones, que conviene aplicar solo cuando las evaluaciones muestran un fallo de recuperación que corrigen:

- **Reescritura de la consulta**: reformular la solicitud con el vocabulario de la fuente sin cambiar la intención ("mi MX-200 llegó roto" pasa a "política de devolución de artículos dañados MX-200").
- **Descomposición**: dividir las preguntas compuestas y recuperar para cada parte ("¿Puedo devolverlo y quién aprueba las excepciones?").
- **Extracción de entidades y filtros**: convertir producto, región, fecha o versión en filtros estructurados.
- **HyDE** (hypothetical document embeddings): pedirle al modelo una respuesta hipotética y buscar con ella, lo que ayuda a que preguntas cortas y conceptuales encuentren pasajes largos.

Una sola llamada puede hacer las tres primeras:

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

La última instrucción ataca el principal riesgo que señala la formación: reescrituras que pierden las palabras clave o las restricciones del usuario sin mejorar la recuperación.

## Recuperación

### Búsqueda semántica, por palabras clave e híbrida

La búsqueda semántica encuentra paráfrasis pero es débil con identificadores exactos; un código de error como `ERR-4297` o una referencia de producto se encuentra mejor con búsqueda por palabras clave. BM25, el algoritmo estándar de palabras clave, premia los términos raros: un código que aparece en 2 de 10.000 documentos puntúa alto, mientras que la palabra "error", presente en 7.800, casi no cuenta. La formación de OpenAI lo resume en una línea: la semántica encuentra paráfrasis, las palabras clave protegen los identificadores exactos y la búsqueda híbrida fusiona las clasificaciones, no las puntuaciones brutas.

El método de fusión habitual es la **reciprocal rank fusion** (RRF), que solo usa la posición de cada documento en cada lista de resultados:

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

Añade **filtros de metadatos** para todo lo estructurado: una pregunta sobre "la política del MX-200 para compras en California en 2026" solo debería buscar en documentos de ese producto, región y periodo, y solo en los que el usuario puede leer. Filtrar por permisos en el momento de la recuperación es la única forma confiable de evitar que un sistema RAG cite documentos a quien no debe verlos.

Las cifras muestran por qué combinar señales importa. En los experimentos de contextual retrieval de Anthropic, medidos como la proporción de chunks relevantes que faltan entre los 20 primeros resultados, los embeddings contextuales redujeron los fallos un 35%, añadir BM25 contextual llevó la reducción al 49% y añadir reranking llegó al 67% (de 5,7% a 1,9% de recuperaciones fallidas).

### Recuperación en varios pasos

Algunas respuestas están repartidas. "¿Qué equipos dependen del proyecto Aurora y quién los dirige?" necesita una búsqueda para encontrar los equipos dependientes y otra para encontrar a sus responsables. La recuperación de un solo paso no puede hacerlo; una cadena de recuperaciones, o un agente que decide qué buscar después, sí. Aquí RAG se vuelve **RAG agéntico**: la recuperación se expone como una herramienta (a menudo junto a consultas SQL, APIs y búsqueda web), y el modelo planifica las búsquedas, lee los resultados y vuelve a buscar hasta tener la evidencia. Resuelve preguntas más difíciles a cambio de más latencia, costo y variabilidad, así que mantén un pipeline simple para las preguntas comunes y reserva los agentes para las de varios saltos.

Un enfoque relacionado para preguntas sobre todo un corpus ("¿Cuáles son los temas principales de estos 5.000 tickets de soporte?") es [GraphRAG](https://www.microsoft.com/en-us/research/project/graphrag/), de Microsoft Research, que extrae entidades y relaciones a un grafo de conocimiento y resume sus comunidades, en lugar de recuperar chunks aislados.

## Reranking

La recuperación de primera etapa es rápida pero tosca: compara un vector de consulta con millones de vectores de chunks. El reranking toma los 50 a 150 mejores candidatos y puntúa cada uno frente a la pregunta con más cuidado, quedándose con los 5 a 20 mejores. La formación de OpenAI describe cuatro tipos, cada uno contra un fallo distinto, con un costo y una latencia que crecen más o menos en este orden:

- **Reglas de negocio** que suben señales conocidas: promover las políticas aprobadas y vigentes, bajar los borradores.
- **Reevaluación léxica** cuando importan términos exactos, como un identificador CVE y un nombre de paquete juntos.
- **Modelos cross-encoder** que leen la consulta y el pasaje a la vez, y distinguen "devoluciones tras abrir la caja" de "devoluciones de artículos sin abrir".
- **Rerankers basados en LLM** que aplican una rúbrica cualitativa, como preferir cifras auditadas a resúmenes de marketing.

Un prompt de reranking con un LLM puede ser corto:

```text
Question: {{QUESTION}}

Below are candidate passages. Score each from 0 to 3 for how directly it helps
answer the question: 3 = answers it, 2 = contains part of the answer, 1 = related
background, 0 = irrelevant. Prefer current, official policy over drafts or FAQs.

{{PASSAGES_WITH_IDS}}

Return JSON: [{"id": "...", "score": n}, ...] for every passage.
```

Valida la elección con métricas de recuperación (MRR, nDCG), la latencia del percentil 95 y el costo por consulta, no con unas pocas pruebas a ojo.

## Generar la respuesta

### Gasta la ventana de contexto con intención

La ventana de contexto es un presupuesto compartido entre las instrucciones, la pregunta, el historial de la conversación, la evidencia y el espacio para la respuesta. La regla de decisión de OpenAI es la correcta: recupera evidencia suficiente para responder bien, pero no inundes al modelo con chunks marginales, que diluyen su atención y suben el costo. El orden también importa: Anthropic recomienda poner los documentos largos antes de la pregunta y las instrucciones.

### Un contrato de respuesta fundamentada

El prompt de respuesta define las reglas que hacen confiable un sistema RAG: responder con la evidencia, citarla, abstenerse o preguntar cuando falta evidencia y señalar los conflictos en lugar de elegir un lado en silencio. Una versión de la que partiría:

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

El cookbook de Anthropic usa una versión más simple de la regla 1 ("remain faithful to the underlying context") y la acompaña de una instrucción para omitir preámbulos. Para las respuestas importantes, una segunda verificación puede comprobar que cada fuente citada respalda de verdad su afirmación, que es también la forma de medir la calidad de las citas.

## Evaluación

RAG falla en lugares concretos, y una única puntuación de extremo a extremo oculta dónde. La formación de OpenAI asocia las métricas a la etapa que falla:

| Etapa | Pregunta | Métricas |
|---|---|---|
| Fuentes e índice | ¿La respuesta está presente, vigente y es legible? | Cobertura, frescura, calidad de extracción, duplicados |
| Recuperación | ¿La evidencia correcta apareció entre los primeros resultados? | Hit rate@k, recall@k, MRR, nDCG |
| Generación | ¿La respuesta se mantuvo fiel a la evidencia? | Fidelidad, respaldo de las citas, abstención |
| Extremo a extremo | ¿El usuario recibió una respuesta útil a un costo aceptable? | Relevancia, éxito de la tarea, latencia, costo |

El cookbook de Anthropic hace exactamente eso con un conjunto de 100 preguntas sobre su propia documentación, y mide la recuperación (precisión, recall, F1, MRR) por separado de la precisión de extremo a extremo, juzgada por un modelo. Su pipeline básico (chunks por encabezado, embeddings, los 3 mejores) alcanzó un 71% de precisión de extremo a extremo; añadir indexación por resúmenes y reranking subió el MRR de 0,74 a 0,87 y la precisión al 81%. La formación de OpenAI muestra un asistente de servicios financieros que pasó de cerca del 45% al 98% de precisión acumulando experimentos de chunking y embeddings, expansión de consultas, HyDE, embeddings ajustados, reranking, clasificación, uso de herramientas y prompt engineering, cada paso medido contra el mismo objetivo. Lo importante de ambos ejemplos no son las técnicas concretas, sino que cada cambio se midió.

Para escalar la calificación, usa un modelo como juez, con una rúbrica estricta y un veredicto fácil de procesar, y revisa a mano una muestra de sus decisiones:

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

Después convierte la evaluación en una barrera de regresión, como recomienda la formación de OpenAI: un conjunto dorado de preguntas representativas con sus respuestas y pasajes esperados; casos difíciles de ambigüedad, frescura, permisos, entradas maliciosas y preguntas sin respuesta; cada cambio en la ingesta, el ranking, los prompts, el enrutamiento o los modelos probado contra una línea base antes de salir a producción; y casos nuevos añadidos a partir de los comentarios de los usuarios y de los fallos.

## Construir o comprar

No tienes que ensamblar cada pieza. La guía de AWS compara las [opciones totalmente gestionadas](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/rag-fully-managed.html), Knowledge Bases for Amazon Bedrock, Amazon Q Business y SageMaker Canvas, que se conectan a fuentes como SharePoint, Confluence y sitios web y resuelven buena parte del pipeline, con arquitecturas propias construidas a partir de un recuperador (Amazon Kendra, OpenSearch, Aurora con pgvector y otros) y un modelo en Bedrock. OpenAI ofrece búsqueda de archivos alojada con vector stores a través de su Responses API, y las plataformas de datos traen la suya (Cortex Search en Snowflake, Vector Search en Databricks). La disyuntiva es la misma en todas partes: los servicios gestionados eliminan trabajo poco diferenciador pero limitan la personalización del chunking, el ranking y la evaluación. Un servicio gestionado es una buena forma de obtener una línea base y un conjunto dorado; pasa a un pipeline propio cuando las evaluaciones muestren un hueco que solo puedes cerrar con más control.

## Seguridad y gobierno

RAG amplía la superficie de ataque de dos maneras. Cada documento indexado se vuelve un canal de **inyección indirecta de prompts**: una página web o un ticket envenenados pueden contener instrucciones que el modelo siga, así que el texto recuperado debe marcarse como datos y las herramientas que el modelo puede llamar deben limitarse. Y el índice se convierte en una copia de datos sensibles: aplica los permisos del sistema de origen al recuperar, enmascara o excluye los datos personales que las respuestas no necesitan, propaga las eliminaciones y registra qué documentos se recuperaron para cada respuesta, para poder auditarla después.

## Una lista de verificación

- Decide si necesitas RAG: los corpus pequeños caben en el prompt con caché.
- Trata la ingesta como un pipeline de datos: fuentes con responsable, metadatos, permisos, actualizaciones incrementales y eliminaciones.
- Empieza con chunks según la estructura que lleven su encabezado o el contexto del documento.
- Usa búsqueda híbrida con filtros de metadatos; añade reranking cuando las métricas lo justifiquen.
- Escribe un prompt de respuesta fundamentada con citas y reglas de abstención y de conflictos.
- Construye un conjunto dorado antes de ajustar, mide cada etapa por separado y condiciona cada cambio a él.
- Reserva el RAG agéntico para las preguntas de varios saltos que una sola recuperación no puede responder.

## Fuentes

- AWS: [Retrieval Augmented Generation options and architectures on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/introduction.html), [Fully managed RAG options on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/rag-fully-managed.html)
- Anthropic: [Retrieval-augmented generation cookbook](https://platform.claude.com/cookbook/capabilities-retrieval-augmented-generation-guide), [Introducing contextual retrieval](https://www.anthropic.com/news/contextual-retrieval)
- OpenAI: [Retrieval-augmented generation builder training (OpenAI Academy)](https://d2xo500swnpgl1.cloudfront.net/slide-upload/oaiacademy/Builder-Bootcamp-RAG-cd2cd443-9b6e-42ec-8300-0c084268f7d1-1789064989962.pdf), [Image understanding with RAG](https://developers.openai.com/cookbook/examples/multimodal/image_understanding_with_rag)
- Microsoft Research: [GraphRAG](https://www.microsoft.com/en-us/research/project/graphrag/)
