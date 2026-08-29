# Example

A fully synthetic input/output example, illustrating the *shape* of a traceable answer
— fictional company, fictional documents, fictional content. Nothing below is real
data, a real query, or a real answer from the production system.

## Synthetic source documents (ingested)

**`retry-policy.md`** (fictional internal doc, "Acme Platform Docs")
> The ingestion worker retries a failed job up to 3 times with exponential backoff
> (base 2s). After the third failure the job moves to the dead-letter queue and an
> alert fires.

**`queue-config.md`** (fictional internal doc, "Acme Platform Docs")
> The ingestion worker consumes from the `ingest-jobs` queue. Queue depth alerts are
> configured to fire above 500 pending jobs.

## Synthetic query

> "What happens to a job that keeps failing, and does anything watch for a backed-up
> queue?"

## Retrieval

Hybrid retrieval (BM25 + vector search) surfaces both source chunks above — BM25
catches the exact term "queue" shared across both documents; vector search catches the
semantic match between "keeps failing" and "retries ... After the third failure."
Reranking orders `retry-policy.md` first since it's the more direct match for "keeps
failing."

## Generated answer (source-grounded)

> A job that keeps failing is retried up to 3 times with exponential backoff (2s base
> delay); after the third failure it moves to the dead-letter queue and triggers an
> alert **[retry-policy.md]**. Separately, the queue it runs on has its own alerting: an
> alert fires if the `ingest-jobs` queue backs up past 500 pending jobs
> **[queue-config.md]**.

Every clause is attributed to the specific fictional source it came from — reproducing
the traceability property described in [`docs/architecture.md`](../docs/architecture.md)
and [`docs/methodology.md`](../docs/methodology.md), without any real system's data.
