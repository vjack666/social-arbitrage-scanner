# NVIDIA Earnings Pilot — Point-in-Time Protocol v0.1

**Status:** Study protocol only. No complete dataset has been collected and no forecast has been generated.

## Event anchor

- Asset: NVIDIA Corporation (NASDAQ: NVDA)
- Event: Q3 fiscal 2027 results release
- Officially announced date: Tuesday, 2026-11-17
- Expected results publication: approximately 1:20 p.m. Pacific Time, equivalent to 4:20 p.m. Ecuador time on that date, subject to confirmation from the live official release.
- Earnings call: 2:00 p.m. Pacific / 5:00 p.m. Eastern. The call is a separate event from the results release.
- Primary event reference: https://nvidianews.nvidia.com/news/nvidia-sets-conference-call-for-third-quarter-financial-results-6928873

## Windows

- Pre-event research window: 2026-11-10 00:00 through 2026-11-17 16:19:59 Ecuador time, with each record judged using its actual publication/availability timestamp. This is a seven-calendar-day window ending immediately before the currently announced approximate release time; the final cutoff must be adjusted if NVIDIA changes the release time.
- Decision snapshots: create one snapshot at each documented collection cycle, and a final pre-release snapshot immediately before the results release. Never combine a later observation into an earlier snapshot.
- Post-event evaluation window: from the verified release timestamp through 1 trading day, 5 trading days, and 20 trading days afterward. These observations are evaluation-only and must not be features in the pre-event forecast.

## Research questions

1. Did public information show a measurable change in narratives or expectations before the announcement?
2. Were social attention changes broad across independent authors/sources, or concentrated in repeated/syndicated content?
3. Did the evidence provide information beyond simple price/volume and sector/market baselines?
4. Could an analyst using only the timestamped pre-event information have identified a testable signal?

## Assets and baselines

- Primary asset: NVDA.
- Context benchmarks: Nasdaq-100 (use a documented tradable proxy or index series), a semiconductor-sector benchmark (document exact ticker/provider), and broad US equities (document exact ticker/provider).
- Do not mix price series with different session, adjustment, or timestamp conventions without explicit normalization.

## Source policy

- Prefer NVIDIA investor relations, SEC filings, and primary-source statements for company facts.
- Use GDELT for news discovery, then verify material claims against the original publisher or primary source.
- Market data must include provider, interval, timezone, corporate-action adjustment policy, and license.
- Social data may be used only when access and use are authorized. If historical coverage or licensing is unclear, mark it missing; do not replace historical posts with today's search results.

## Point-in-time rules

For every item retain `published_at`, `event_at` if known, `retrieved_at`, `decision_timestamp`, original timezone, canonical URL/source ID, verification state, and parser/dataset version. Do not infer a missing timestamp. The item can be used in a decision snapshot only if it was publicly available by that snapshot's decision timestamp. Later edits/corrections are separate versions and cannot silently rewrite prior snapshots.

## Predeclared outcomes

Report descriptive outcomes rather than claiming predictive value from one event. Measure NVDA total price change from the last regular-session close before release to the first regular-session close after release, and from that close through +1, +5, and +20 trading sessions. Also record the first regular-session open and intraday high/low for gap and volatility context. Use adjusted prices where appropriate and document exact timestamps. Compare each result with the chosen benchmarks over matching windows.

A single earnings event is a case study, not sufficient statistical evidence for a general trading edge. Any predictive claim requires a broader, preregistered multi-event historical test with costs and untouched out-of-sample periods.

## Dataset status labels

- `planned`: source/window is specified, no records collected.
- `collected_unverified`: records gathered but not yet checked.
- `verified`: source and timestamps checked.
- `excluded`: unusable, duplicated, outside the point-in-time cutoff, or license/access unclear; reason required.

## Release gates

1. Confirm official event timing at collection time.
2. Approve the data source and licensing register.
3. Record actual collection start time honestly; historical retrieval is not live collection.
4. Complete provenance and duplicate checks.
5. Freeze the final pre-event snapshot before reading the results.
6. Evaluate post-event outcomes separately and retain the original snapshot unchanged.

## Current limitations

This protocol does not itself collect or archive feeds, guarantee historical social data access, or run a backtest. The announced event date/time can change. No direction, score, or profitability claim is made.