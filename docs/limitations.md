# Limitations

Published upfront, not as a caveat buried at the end — honest constraints strengthen
credibility rather than weaken it.

## What this repository intentionally does not include

- **Source code.** This is an architecture/methodology write-up, not the platform
  itself. There is deliberately no `src/` directory.
- **Client identity and internal names.** Service names, internal URLs, team names, and
  anything that would identify the client or their infrastructure are generalized or
  omitted.
- **Proprietary data.** No real documents, logs, or outputs from the production system
  appear here. Any example in [`examples/`](../examples/) is synthetic.
- **Specific LLM providers.** Multi-provider routing is described as a pattern; which
  providers are actually used is an operational/commercial detail, not disclosed.
- **Evaluation numbers.** Score thresholds and result figures are institutional metrics
  — see [`evaluation.md`](evaluation.md) for why they're withheld rather than
  approximated.
- **Runtime benchmarks.** Latency, cost-per-query, and throughput figures are not
  published here for the same reason.

## Structural limitation of this format

This is a write-up, not the running system — a reader can verify what's stated here
against public sources (the arXiv preprint, ORCID, and journal publication linked from
the [GitHub profile](https://github.com/denis-samatov) cover the research side of the
work), but can't independently inspect this platform's code or its actual production
metrics, because it's closed-source institutional work. That's a real constraint on how
much this document alone can prove — it's disclosed here rather than glossed over, and
the honest next step for anyone who wants more than this document can offer is a
conversation, not a bigger claim.

## Why publish limitations at all

A reviewer who finds an unstated limitation on their own reads it as something you
missed or hid. Stating it yourself reads as engineering maturity.
