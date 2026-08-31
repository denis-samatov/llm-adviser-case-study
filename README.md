# LLM Adviser — Case Study

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Role:** Technical Lead · **Team:** 5 engineers · **Status:** in production
**Last reviewed:** 2026-08-30

LLM Adviser is an agentic engineering knowledge platform: it turns scattered internal
documentation into deterministic, traceable answers for engineers. This repository is a
sanitized case study of the architecture and design decisions — the platform itself is
closed-source institutional work, so no client code, data, or proprietary logic is
published here. See [`docs/limitations.md`](docs/limitations.md) for exactly what that
excludes.

## Problem

Engineering knowledge tends to live scattered across wikis, design docs, and code
comments, and a plain keyword search or a naive RAG chatbot over that corpus gives
answers that are either hard to find (keyword search misses paraphrased questions) or
hard to trust (a generic RAG pipeline can hallucinate a plausible-sounding answer with
no way to check it against the source). LLM Adviser is built around a narrower
promise than "a chatbot for your docs": every answer traces back to the specific source
it came from, and the pipeline that produces it is deterministic enough to be tested
like any other production system, not just spot-checked by hand.

## What I built (role & scope)

- Designed the platform architecture end to end: deterministic document processing,
  traceable outputs, asynchronous execution, and a clean domain/infrastructure boundary.
- Led a team of 5 engineers — architecture decisions, code review, solution review,
  and delivery ownership.
- Designed the reusable ingestion/retrieval components: OCR, provenance preservation,
  hybrid retrieval, parent-document recovery, GraphRAG, reranking, and source-grounded
  generation.
- Built the execution layer: FastAPI, async workers, Redis, multi-provider LLM routing,
  automated evaluation, observability, and CI quality gates.

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the component breakdown and data
flow — described as patterns (e.g. "async workers + Redis + multi-provider LLM routing"),
not as concrete service names or endpoints.

## Methodology

See [`docs/methodology.md`](docs/methodology.md) for how deterministic document
processing and source-grounded generation are actually implemented.

## Evaluation

See [`docs/evaluation.md`](docs/evaluation.md) for how quality is measured. Score
thresholds and result figures are institutional metrics and aren't published here — the
methodology is real, the numbers aren't invented to fill a gap.

## Limitations & what's intentionally excluded

See [`docs/limitations.md`](docs/limitations.md) — published upfront, not as a caveat
buried at the end.

## Stack

FastAPI · Redis · async workers · multi-provider LLM routing · hybrid retrieval ·
GraphRAG · reranking

---

*This is a sanitized write-up of institutional work. I'm happy to walk through the real
architecture, trade-offs, and results in a call —
[Telegram @SamatovDS](https://t.me/SamatovDS) ·
[denissamatov470@gmail.com](mailto:denissamatov470@gmail.com).*
