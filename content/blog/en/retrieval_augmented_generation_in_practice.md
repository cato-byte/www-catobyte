## Retrieval-Augmented Generation (RAG) in 2026: How It Works, What Improves It and How to Measure It

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Retrieval-augmented generation in 2026](../../images/retrieval_augmented_generation_in_practice_title_img.png)

*Technical article*

## What RAG is

A language model knows what was in its training data, frozen at a cutoff date, and nothing about your company's documents, tickets, contracts or tables. **Retrieval-augmented generation** fixes that at request time: before the model answers, the system *retrieves* relevant information from your sources, *augments* the prompt with it, and the model *generates* an answer grounded in that evidence. AWS's [prescriptive guidance on RAG](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/introduction.html) describes it as the model referencing an authoritative data source outside its training data before responding.

OpenAI's RAG builder training uses a simple example: a customer asks "What is your return policy?", the system searches the policy knowledge base, finds the rules (full refund up to 14 days, a voucher for half the value up to 30 days), and the model answers in plain language with those exact conditions. Without retrieval, the model would invent a plausible policy.

RAG matters because it gives you four things a bare model can't:

- **Private and current knowledge**, updated by re-indexing instead of retraining.
- **Citations**, so users and auditors can check the source of every claim.
- **Access control**, because retrieval can respect who is allowed to see which document.
- **Lower hallucination rates**, when the prompt tells the model to answer only from the evidence and to abstain otherwise.

For data engineers, RAG is also familiar territory. Most of the work isn't the model: it's ingestion, parsing, chunking, metadata, incremental indexing, freshness, permissions and evaluation. In other words, a data pipeline whose consumer happens to be a language model.

## Do you need RAG at all?

OpenAI's training material places tasks on a spectrum of how much external knowledge they need:

1. **Prompt and reasoning.** The task can be solved from instructions and general knowledge: rewrite text, classify, plan from constraints.
2. **Supplied context.** A small, known set of documents fits directly in the prompt: compare three policies, summarize an attached report.
3. **RAG.** The system must search private, changing or large sources at run time: support knowledge bases, product documentation, policy questions with citations.
4. **Agentic RAG.** The model plans its own searches, picks tools and sources, and combines evidence over several steps: multi-hop research across systems.

Choose the lowest level that works. Context windows are now large enough that Anthropic's [contextual retrieval article](https://www.anthropic.com/news/contextual-retrieval) advises skipping RAG for knowledge bases under about 200,000 tokens (roughly 500 pages): put everything in the prompt and use prompt caching, which it reports makes repeated requests more than twice as fast and up to 90% cheaper. RAG pays off when the corpus is larger, changes often, or needs per-user permissions.

RAG and fine-tuning solve different problems. Fine-tuning changes *how* a model behaves (format, style, a narrow skill); RAG changes *what it knows* at answer time. For knowledge that changes, RAG is almost always the right first step.

## The pipeline

A RAG system has an offline part, which prepares the knowledge, and an online part, which answers each question:

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

OpenAI's training groups the techniques into the same four stages: data preparation, input processing, retrieval and answer generation. The rest of this article follows that order.

## Data preparation

### Choose and describe your sources

Retrieval can't find what isn't indexed, and it happily finds what shouldn't be. OpenAI's best practices are to index only approved, current sources with clear owners, and to attach scope, date, permissions and a source link to every chunk. Its list of common pitfalls is a data quality list: duplicate or conflicting documents produce inconsistent answers, and retired content or outdated permissions stay retrievable unless the pipeline removes them. Deletes and permission changes need to flow into the index as reliably as new documents do.

### Chunking

Documents are split into passages small enough to retrieve precisely and large enough to make sense on their own. The main strategies, in the order I'd try them:

| Strategy | How it splits | Good for |
|---|---|---|
| Structure-aware | Headings, sections, paragraphs, tables | Documentation, policies, Markdown, HTML |
| Fixed size with overlap | N tokens with some overlap | A reliable baseline for irregular content |
| Sentence windows | Whole sentences, with neighbors as context | Prose |
| Semantic boundaries | Topic shifts detected by embeddings | Long documents mixing unrelated topics; costlier |

Anthropic's [RAG cookbook](https://platform.claude.com/cookbook/capabilities-retrieval-augmented-generation-guide) splits its documentation by heading and stores each chunk with its heading and URL, then embeds the heading together with the text. That small step keeps a chunk like "Limits: 100 requests per minute" attached to *which* API it describes. Overlap protects ideas that cross a boundary, but too much of it fills the index with duplicates. Tune size and overlap with evaluations, not by intuition.

### Add context to each chunk

A chunk often loses meaning when cut from its document: "Revenue grew 3% over the previous quarter" doesn't say which company or quarter. Anthropic's **contextual retrieval** technique asks a model to write a short sentence situating each chunk within its document, and prepends it before embedding and keyword indexing. A prompt in the spirit of theirs:

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

With prompt caching, the whole document is processed once and reused for each of its chunks, which is how Anthropic estimates the one-time cost at about one dollar per million document tokens. Other enrichments work the same way: summaries of each document (the cookbook's "summary indexing"), synonyms and keywords, or text descriptions of images. OpenAI's training adds a caution: start from the original source and add generated signals only when retrieval tests show a gap, and review generated text before indexing it.

### Images and scanned documents

Text search can't see what's only in a picture. OpenAI's [image understanding with RAG cookbook](https://developers.openai.com/cookbook/examples/multimodal/image_understanding_with_rag) converts each image into a one-line description with a vision model, appends it to the related text, and indexes the result. In its food-delivery example, a text-only search for comments about spaghetti found only "Pasta was overcooked", while the image-augmented index also surfaced a photo of "a neatly plated spaghetti in tomato sauce". The trade-off is more tokens per item, so measure whether the gain justifies it.

### Embeddings and the index

An embedding model turns each chunk into a vector, and texts with related meaning point in similar directions even when their wording differs: "How do I return a damaged item?" lands close to "Defective products can be sent back within 30 days" and far from "Where can I update my billing address?". Similarity is usually measured with cosine similarity.

The vectors go into an index: a dedicated vector database, a search engine with vector support such as OpenSearch, or `pgvector` in the PostgreSQL you already run. For most teams the best index is the one their platform already operates well, with keyword search, metadata filters and access control available next to vector search.

## Input processing

Users ask questions in their words; documents are written in someone else's. OpenAI's training lists four transformations, to apply only when evaluations show a retrieval failure they fix:

- **Query rewriting**: rephrase the request in the source's vocabulary while preserving intent ("my MX-200 arrived broken" becomes "MX-200 damaged-item return policy").
- **Decomposition**: split multipart questions and retrieve for each part ("Can I return it and who approves exceptions?").
- **Entity extraction and filters**: pull product, region, date or version into structured filters.
- **HyDE** (hypothetical document embeddings): have the model write a hypothetical answer and search with it, which helps short conceptual questions match long passages.

One call can do the first three:

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

The last instruction addresses the main risk the training warns about: rewrites that drop the user's keywords or constraints without improving retrieval.

## Retrieval

### Semantic, keyword and hybrid search

Semantic search finds paraphrases but is weak on exact identifiers; an error code like `ERR-4297` or a product reference is better found by keyword search. BM25, the standard keyword algorithm, rewards rare terms: a code that appears in 2 of 10,000 documents scores high, while the word "error", in 7,800 of them, barely counts. OpenAI's training sums it up in a line: semantic finds paraphrases, keyword protects exact identifiers, and hybrid search fuses the rankings, not the raw scores.

The usual fusion method is **reciprocal rank fusion** (RRF), which only uses each document's position in each result list:

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

Add **metadata filters** for anything structured: a question about "the MX-200 policy for California purchases in 2026" should only search documents for that product, region and period, and only those the user may read. Filtering by permissions at retrieval time is the only reliable way to keep a RAG system from quoting documents to people who shouldn't see them.

The numbers show why combining signals matters. In Anthropic's contextual retrieval experiments, measured as the share of relevant chunks missing from the top 20 results, contextual embeddings cut failures by 35%, adding contextual BM25 brought the reduction to 49%, and adding reranking reached 67% (from 5.7% to 1.9% of failed retrievals).

### Multi-step retrieval

Some answers live in several places. "Which teams depend on Project Aurora, and who manages them?" needs one search to find the dependent teams and a second to find their managers. Single-step retrieval can't do that; a chain of retrievals, or an agent that decides what to search next, can. This is where RAG becomes **agentic RAG**: retrieval is exposed as a tool (often next to SQL queries, APIs and web search), and the model plans the searches, reads the results and searches again until it has the evidence. It handles harder questions at the price of more latency, cost and variability, so keep a simple pipeline for the common questions and reserve agents for the multi-hop ones.

A related approach for questions about a whole corpus ("What are the main themes in these 5,000 support tickets?") is [GraphRAG](https://www.microsoft.com/en-us/research/project/graphrag/) from Microsoft Research, which extracts entities and relationships into a knowledge graph and summarizes its communities, instead of retrieving isolated chunks.

## Reranking

First-stage retrieval is fast but rough: it compares one query vector with millions of chunk vectors. Reranking takes the top 50 to 150 candidates and scores each one against the question more carefully, keeping the best 5 to 20. OpenAI's training describes four kinds, each fixing a different failure, with cost and latency rising roughly in this order:

- **Rule-based boosts** for known business signals: promote approved, current policies; demote drafts.
- **Lexical rescoring** when exact terms matter, such as a CVE identifier and a package name together.
- **Cross-encoder models** that read the query and passage together, telling "returns after opening the box" apart from "returns of unopened items".
- **LLM rerankers** that apply a qualitative rubric, such as preferring audited figures over marketing summaries.

An LLM reranking prompt can be short:

```text
Question: {{QUESTION}}

Below are candidate passages. Score each from 0 to 3 for how directly it helps
answer the question: 3 = answers it, 2 = contains part of the answer, 1 = related
background, 0 = irrelevant. Prefer current, official policy over drafts or FAQs.

{{PASSAGES_WITH_IDS}}

Return JSON: [{"id": "...", "score": n}, ...] for every passage.
```

Validate the choice with retrieval metrics (MRR, nDCG), 95th-percentile latency and cost per query, not with a few spot checks.

## Generating the answer

### Spend the context window deliberately

The context window is a budget shared by instructions, the question, conversation history, evidence and room for the answer. OpenAI's decision rule is the right one: retrieve enough evidence to answer well, but don't flood the model with marginal chunks, which dilute attention and raise cost. Order matters too: Anthropic recommends putting long documents before the question and instructions.

### A grounded response contract

The answer prompt defines the rules that make RAG trustworthy: answer from the evidence, cite it, abstain or ask when evidence is missing, and flag conflicts instead of picking a side silently. A version I'd start from:

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

Anthropic's cookbook uses a simpler version of rule 1 ("remain faithful to the underlying context") and pairs it with an instruction to skip preambles. For important answers, a second check can verify that every cited source actually supports its claim, which is also how you measure citation quality.

## Evaluation

RAG fails in specific places, and a single end-to-end score hides where. OpenAI's training maps metrics to the stage that fails:

| Stage | Question | Metrics |
|---|---|---|
| Sources and index | Is the answer present, current and parseable? | Coverage, freshness, parse quality, duplicates |
| Retrieval | Did the right evidence appear near the top? | Hit rate@k, recall@k, MRR, nDCG |
| Generation | Did the answer stay faithful to the evidence? | Faithfulness, citation support, abstention |
| End to end | Did the user get a useful answer at acceptable cost? | Answer relevance, task success, latency, cost |

Anthropic's cookbook does exactly this on a 100-question dataset over its own documentation, measuring retrieval (precision, recall, F1, MRR) separately from end-to-end accuracy judged by a model. Its basic pipeline (heading-based chunks, embeddings, top 3) reached 71% end-to-end accuracy; adding summary indexing and reranking raised MRR from 0.74 to 0.87 and accuracy to 81%. OpenAI's training shows a financial-services assistant climbing from about 45% to 98% accuracy by stacking chunking and embedding experiments, query expansion, HyDE, fine-tuned embeddings, reranking, classification, tool use and prompt engineering, each step measured against the same target. The point of both examples isn't the specific techniques; it's that every change was measured.

To scale grading, use a model as a judge, with a strict rubric and a parseable verdict, and spot-check its decisions by hand:

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

Then turn the evaluation into a regression gate, as OpenAI's training recommends: a golden set of representative questions with expected answers and expected passages; hard cases for ambiguity, freshness, permissions, adversarial inputs and questions with no answer; every change to ingestion, ranking, prompts, routing or models tested against a baseline before it ships; and new cases added from user feedback and failures.

## Build or buy

You don't have to assemble every piece. AWS's guide compares [fully managed options](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/rag-fully-managed.html), Knowledge Bases for Amazon Bedrock, Amazon Q Business and SageMaker Canvas, which connect to sources such as SharePoint, Confluence and websites and handle much of the pipeline, with custom architectures built from a retriever (Amazon Kendra, OpenSearch, Aurora with pgvector and others) and a model on Bedrock. OpenAI offers hosted file search with vector stores through its Responses API, and the data platforms ship their own (Snowflake's Cortex Search, Databricks' Vector Search). The trade-off is the same everywhere: managed services remove undifferentiated work but limit customization of chunking, ranking and evaluation. A managed service is a good way to get a baseline and a golden set; move to a custom pipeline when evaluations show a gap you can only close with control.

## Security and governance

RAG widens the attack surface in two ways. Every indexed document becomes a channel for **indirect prompt injection**: a poisoned web page or ticket can contain instructions the model may follow, so retrieved text must be marked as data, and tools the model can call must be limited. And the index becomes a copy of sensitive data: apply the source system's permissions at retrieval time, mask or exclude personal data that answers don't need, propagate deletions, and log which documents were retrieved for each answer so you can audit it later.

## A checklist

- Decide whether you need RAG at all: small corpora fit in the prompt with caching.
- Treat ingestion as a data pipeline: owned sources, metadata, permissions, incremental updates and deletes.
- Start with structure-aware chunks that carry their heading or document context.
- Use hybrid search with metadata filters; add reranking when metrics justify it.
- Write a grounded answer prompt with citations, abstention and conflict rules.
- Build a golden set before tuning, measure each stage separately, and gate every change on it.
- Reserve agentic RAG for multi-hop questions that a single retrieval can't answer.

## Sources

- AWS: [Retrieval Augmented Generation options and architectures on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/introduction.html), [Fully managed RAG options on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/rag-fully-managed.html)
- Anthropic: [Retrieval-augmented generation cookbook](https://platform.claude.com/cookbook/capabilities-retrieval-augmented-generation-guide), [Introducing contextual retrieval](https://www.anthropic.com/news/contextual-retrieval)
- OpenAI: [Retrieval-augmented generation builder training (OpenAI Academy)](https://d2xo500swnpgl1.cloudfront.net/slide-upload/oaiacademy/Builder-Bootcamp-RAG-cd2cd443-9b6e-42ec-8300-0c084268f7d1-1789064989962.pdf), [Image understanding with RAG](https://developers.openai.com/cookbook/examples/multimodal/image_understanding_with_rag)
- Microsoft Research: [GraphRAG](https://www.microsoft.com/en-us/research/project/graphrag/)
