# Social Arbitrage Scanner

Evidence-first research system for detecting discrepancies between social attention, verified events, market expectations, and asset prices.

## Status
**Specification phase — no trading execution and no autonomous agents deployed.** Implementation is blocked until the owner approves requirements, architecture, data access/licensing, and acceptance criteria.

## Agent specifications
- [01 — Social Arbitrage Discovery](docs/agents/01-social-arbitrage-discovery.md)
- [02 — Quantitative Sentiment](docs/agents/02-quantitative-sentiment.md)
- [03 — News and Event Intelligence](docs/agents/03-news-event-intelligence.md)
- [04 — Crowd Psychology and Positioning](docs/agents/04-crowd-psychology-positioning.md)
- [05 — Quantitative Validation](docs/agents/05-quantitative-validation.md)
- [Coordinator](docs/architecture/coordinator.md)

## Core principles
1. Separate verified facts, inferences, and hypotheses.
2. Preserve source URLs, publication/event timestamps, retrieval timestamps, and provenance.
3. Treat unverified claims as unverified; never promote rumors to facts.
4. Allow disagreement and insufficient-evidence outcomes; do not force consensus.
5. Prevent look-ahead, survivorship, leakage, and overfitting in evaluation.
6. Do not place orders or present outputs as guaranteed financial advice.
7. Never claim access to private methods of people or companies without evidence.

## Proposed workflow
Requirements → design → owner approval → data/licensing review → prototype → validation → controlled expansion.

## Initial validation case
NVIDIA is a candidate case study, not a pre-decided bullish or bearish thesis. Any retrospective test must reconstruct what was knowable at each historical timestamp and exclude future information.

## Current deliverable
This repository currently contains design/specification documents only. No agent implementation, live data integration, backtest result, or trading capability is claimed.
