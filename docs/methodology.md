# Methodology

How the core technical ideas are implemented, described generically enough to be
reusable outside this specific platform — everything below is grounded in the
already-public scope of the role; nothing here asserts proprietary implementation
choices that haven't been disclosed elsewhere.

## Ingestion & provenance

1. Source documents pass through OCR where they're scanned or image-based rather than
   native text.
2. Each extracted chunk retains a link back to its exact source location (document,
   page/section) — this is what later makes an answer's citations checkable rather than
   just plausible-sounding.
3. Chunking and parsing run deterministically: the same source document produces the
   same chunk boundaries and provenance links on every run, which is what lets the
   pipeline be tested in CI like any other deterministic component.

## Hybrid retrieval

Combines BM25 (lexical/keyword match) with vector search over embeddings (semantic
match), then reranks the merged candidate set before it reaches generation. The two
retrieval modes cover different query shapes: BM25 is strong on exact terms and
identifiers that embeddings can blur together; vector search is strong on paraphrased
or conceptual queries that share no exact wording with the source text. Combining both
and reranking the union outperforms either alone on a knowledge base with mixed query
patterns — which is the general justification for hybrid retrieval in RAG systems, and
the reason it's used here rather than a single retrieval mode.

## Parent-document recovery

Retrieval operates on small chunks (for precision), but generation needs enough context
to answer correctly (for correctness). Parent-document recovery closes that gap: once a
chunk is retrieved, the pipeline pulls in its containing section/parent document before
handing context to generation, so the model isn't reasoning over an isolated fragment
stripped of the context that would disambiguate it.

## GraphRAG

Plain vector/keyword retrieval treats each chunk independently, which misses questions
that span multiple related entities or documents (e.g. "how does component A's config
interact with component B's retry policy" when A and B are documented separately).
GraphRAG builds a knowledge graph over extracted entities and their relationships, so
retrieval can traverse related nodes rather than relying on a single chunk happening to
mention everything relevant. This is the class of query where GraphRAG earns its
complexity over plain retrieval — it's not a blanket replacement for hybrid retrieval,
it's a complement for the multi-hop case.

## Source-grounded generation

Generation is constrained to answer only from retrieved, provenance-tagged context, not
from the model's own parametric knowledge — the model is directed to cite the specific
source chunks it used, and to say so explicitly rather than guess when the retrieved
context doesn't actually answer the question. This is what makes "traceable outputs" a
property of every answer rather than an occasional nice-to-have.

## Reranking

The retrieval layer over-fetches (pulls more candidates than needed) and then reranks
the combined BM25 + vector result set before it reaches generation, since raw retrieval
scores from two different methods aren't directly comparable and the naive union of two
ranked lists is a weaker ordering than a dedicated reranking pass over the merged set.
