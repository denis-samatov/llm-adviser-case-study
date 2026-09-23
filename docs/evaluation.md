# Evaluation

This document describes the author's evaluation approach, not a reproducible public
evaluation. The author reports automated evaluation in private CI, but this repository
does not include the workflows, fixtures, scores or logs needed to verify that claim.
Specific thresholds and client-tied results are withheld; see
[`limitations.md`](limitations.md).

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

## Dataset construction

A CI-gating evaluation set has to satisfy two properties that a live query log alone
doesn't: it needs a known-correct answer to check against, and it needs to be stable
across runs. In practice that means:

- **Representative, not exhaustive.** Queries are chosen to cover the query shapes the
  architecture is explicitly built for — exact-term/identifier lookups (BM25's target),
  paraphrased conceptual questions (vector search's target), and multi-hop questions
  spanning related entities (GraphRAG's target) — rather than trying to sample "all"
  traffic.
- **Reference-labeled.** Each evaluation query has an expected set of source chunks and,
  where applicable, an expected answer or answer property (e.g. "must cite both X and
  Y"), reviewed by someone with domain knowledge of the source documents — not generated
  by the same model being evaluated.
- **Versioned with the corpus.** Because ingestion is deterministic (see
  [`methodology.md`](methodology.md)), an evaluation query's expected chunks stay valid
  as long as the source documents haven't changed; a corpus update that changes chunk
  boundaries triggers a review of the affected evaluation entries rather than a silent
  score drift.

## Human-review protocol

Automated scoring (groundedness, retrieval relevance, traceability, multi-hop
faithfulness) catches regressions cheaply on every change, but it doesn't replace human
judgment entirely:

- A sample of automated-evaluation failures is human-reviewed before being accepted as a
  true regression, since an automated groundedness check can itself misjudge a citation.
- New evaluation-set entries go through human review before being trusted as a CI gate —
  an incorrectly labeled reference answer would otherwise silently fail every future
  change that's actually correct.
- Human review is the fallback for the failure modes below, where an automated metric is
  known to be a weaker signal than a person checking the citation chain directly.

## Known failure modes

- **Multi-hop under-synthesis.** For queries spanning multiple related entities, the
  answer sometimes cites only one of the relevant sources instead of synthesizing both —
  the automated multi-hop check is designed to catch this, but it's a harder property to
  score automatically than single-source groundedness, so it gets more human review
  weight.
- **Confident abstention vs. false negative.** Source-grounded generation is directed to
  say so explicitly when retrieved context doesn't answer the question, rather than
  guess — but retrieval sometimes surfaces a genuinely relevant chunk that gets scored as
  irrelevant by the pipeline, producing an unnecessary abstention. Distinguishing "the
  answer isn't in the corpus" from "retrieval missed it" is an ongoing tuning problem,
  not a solved one.
- **Reranking sensitivity to near-duplicate chunks.** When a knowledge base has several
  near-duplicate or superseded versions of similar documentation, reranking can surface
  a stale chunk ahead of the current one; provenance makes this visible in the citation
  rather than hidden, but it's still a real failure mode, not a theoretical one.

## What this case study does not publish

Specific evaluation-set queries, score thresholds, pass/fail numbers, and any
client-tied volume or accuracy figures are institutional metrics and aren't published
here. Publishing a plausible-sounding but unverifiable number would undermine the exact
thing this case study is trying to demonstrate — that claims here are backed by
something real, not just asserted. I'm glad to walk through actual results in a call.
