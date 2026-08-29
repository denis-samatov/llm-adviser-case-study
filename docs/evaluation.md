# Evaluation

How quality is measured — methodology, not invented numbers. This case study states
that automated evaluation is part of the platform's CI quality gates because that's
already public (résumé/GitHub), but doesn't publish specific score thresholds or
client-tied result numbers, for the same reason the rest of this repository excludes
client-specific detail — see [`limitations.md`](limitations.md).

## What "quality" means for a source-grounded RAG platform

- **Groundedness** — does the answer only state what its cited sources actually say,
  with no unsupported claims slipped in from the model's own parametric knowledge?
- **Retrieval relevance** — did the retrieval layer (hybrid BM25 + vector, reranked)
  surface the source documents that actually answer the query?
- **Traceability** — can every claim in the answer be traced back to a specific,
  correctly-cited source chunk?
- **Faithfulness under multi-hop queries** — for queries that GraphRAG traversal is
  meant to help with, does the answer actually synthesize the related entities
  correctly, or silently drop one?

## Automated evaluation as a CI gate

Evaluation isn't a manual, occasional check — it's built into the CI quality gates
described in [`architecture.md`](architecture.md), so a change to retrieval, prompting,
or routing that regresses answer quality is caught before it reaches production rather
than discovered by a user. This is the same reason deterministic document processing
matters: an evaluation suite is only trustworthy if the pipeline it's testing produces
consistent output for the same input.

## What this case study does not publish

Specific evaluation-set queries, score thresholds, pass/fail numbers, and any
client-tied volume or accuracy figures are institutional metrics and aren't published
here. Publishing a plausible-sounding but unverifiable number would undermine the exact
thing this case study is trying to demonstrate — that claims here are backed by
something real, not just asserted. I'm glad to walk through actual results in a call.
