# Design trade-offs

This note explains consequences of the architecture already described in this case study. It is not a production trace, an experiment report, or a claim that undisclosed alternatives were benchmarked.

| Design choice | Intended benefit | Cost / failure mode | Evidence needed to evaluate the choice |
| --- | --- | --- | --- |
| BM25 + vector retrieval + reranking | Cover exact identifiers and paraphrases | More stages, latency, candidate-merging complexity | Same query set and corpus revision; retrieval recall and answer support versus each single-retriever baseline |
| Parent-document recovery | Restore context around a matched fragment | Irrelevant context and larger token budgets | Answer-support checks with/without expansion, using identical retrieved seeds |
| GraphRAG for related entities | Retrieve evidence spanning documents | Entity/link extraction errors and graph maintenance | A separately labelled multi-hop subset and comparison with ordinary hybrid retrieval |
| Async workers + Redis | Move background work away from request handling | Queue delay, retries, duplicate work, partial failures | Queue-age distributions, retry traces, and recovery behavior under a defined workload |
| Multiple LLM providers | Allow routing choices and reduce reliance on one endpoint | Provider differences in output contracts and quality | Provider-specific contract tests and evaluation results; fallback and failure traces |
| Deterministic ingestion with provenance | Make source transformations inspectable and testable | Parser/OCR/version changes can alter outputs | Input hashes, parser/config revisions, chunk/source mappings, regression fixtures |

## Example review question

Consider an **illustrative** query asking which configuration flag changes a retry policy. BM25 can recover the exact flag name, vector retrieval can find paraphrased policy text, and parent recovery can restore a caveat from the surrounding section. Each stage also introduces a possible failure: a stale flag, a semantically similar but unrelated policy, or an oversized parent section.

A useful evaluation would compare the same query and corpus snapshot across retrieval variants, inspect the cited passage, and record both support and latency. No synthetic answer or invented production measurement is presented here.

## What a source citation establishes

A citation lets a reader inspect the retrieved evidence. It does not by itself establish that the answer follows from that evidence, that the source is current, or that the retrieval was complete. These are separate evaluation questions; see [evaluation](evaluation.md) and [limitations](limitations.md).
