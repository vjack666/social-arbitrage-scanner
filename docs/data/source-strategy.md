# Data Source Strategy — v0.1

**Status:** Research and planning only. No API keys have been configured and no live ingestion has been implemented. Costs and access conditions must be reconfirmed before production use.

## Executive decision

Start with a low-cost, evidence-first research stack:
1. **SEC EDGAR** for primary company filings and structured financial facts.
2. **GDELT** for broad news/event discovery and time-stamped media attention.
3. **Alpha Vantage** as an initial market-data candidate for limited historical exploration, subject to rate limits and licensing.
4. **X API** only after measuring expected volume and setting a strict spend limit.
5. **Reddit API** only after obtaining the required approval and confirming the intended use is permitted.
6. **Stocktwits** is not a phase-one dependency because its developer page currently says new API registrations are not being accepted.

Do not scrape sites or bypass platform controls when API access is unavailable. No single source should be treated as complete or ground truth.

## Candidate source register

| Source | Best use | Access/cost observations | Proposed status |
|---|---|---|---|
| SEC EDGAR APIs | Primary filings, submissions, XBRL company facts | SEC says data.sec.gov APIs are public and do not require API keys. Automated access must follow SEC fair-access/security guidance. | Phase 1 — core |
| GDELT Project | News/event discovery, coverage and attention features | GDELT describes its database and analysis service as free/open. Review citation and dataset terms; data is media-derived and can contain duplicates, delays, and machine-generated classifications. | Phase 1 — core |
| Alpha Vantage | Historical equity time series for exploratory analysis | Its support page says the free service offers 25 API requests/day for most datasets. Real-time and 15-minute delayed US equity data are premium-only; commercial use requires contacting sales. Confirm dataset-specific terms before use. | Phase 1 — limited evaluation |
| X API | Public conversation, posts, trends, and social velocity | Official developer platform currently advertises credit-based pay-per-use pricing without fixed monthly costs. Actual endpoint costs and access must be checked before collection; enforce a hard spend cap. | Phase 2 — conditional |
| Reddit Data API | Community discussion and emerging narratives | Reddit's May 2026 guidance says explicit approval is required before API access. Commercial use requires permission and a contract; research use is directed to its Reddit for Researchers program. Fees/limits depend on access and use. | Blocked pending approval |
| Stocktwits API | Investor-community conversation | Its developer page currently says new application registrations are not being accepted while APIs and terms are reviewed. Its terms prohibit unauthorized scraping/data mining. | Exclude from phase 1 |

## Official references

- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- SEC developer resources and fair access: https://www.sec.gov/about/developer-resources
- GDELT data and access: https://gdeltproject.org/data.html
- Alpha Vantage documentation: https://www.alphavantage.co/documentation/
- Alpha Vantage API limits and market-data notes: https://www.alphavantage.co/support/api-key/
- X Developer Platform and pricing model: https://developer.x.com/
- Reddit developer access guidance (updated May 28, 2026): https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data
- Reddit Data API terms: https://redditinc.com/policies/data-api-terms
- Stocktwits developer registration status: https://api.stocktwits.com/developers
- Stocktwits terms on automated extraction: https://stocktwits.com/about/legal/terms/

## Collection and evidence rules

For every fetched item, retain where legally permitted:
- provider and source ID;
- canonical URL or stable reference;
- publication time, underlying event time if known, and retrieval time;
- timezone and original timestamp string;
- content fingerprint for duplicate detection, where permitted;
- raw/normalized payload reference and parser version;
- access method, license/terms version, retention limit, and cost metadata;
- verification status and links to corroborating sources.

Do not invent missing timestamps. Keep `published_at`, `event_at`, `retrieved_at`, and the simulated `decision_timestamp` separate. For historical tests, include an item only if it was available by the decision timestamp; preserve corrections as new versions.

## NVIDIA pilot: minimum source bundle

For a single historical decision time:
1. SEC filings and official company releases available by that time.
2. GDELT news/event records whose publication/first-seen timestamps precede the cutoff.
3. Price/volume history from a provider whose data rights, adjustments, and timestamp semantics are documented.
4. Social data only if authorized access and point-in-time historical coverage can be demonstrated.

If historical social data is unavailable or licensing is unclear, mark the relevant agent input as missing. Do not substitute today's search results for historical evidence.

## Cost and access controls

Before enabling any paid source:
- estimate requests/day, records/request, and historical backfill volume;
- calculate expected monthly spend and set a provider-side and application-side cap where possible;
- log each request's cost or usage units;
- set a fail-closed budget threshold that pauses collection rather than silently exceeding budget;
- verify data redistribution, derived-data, storage, and deletion terms.

## Decision gates before implementation

- Confirm whether this remains personal research or may become a commercial product.
- Confirm acceptable monthly data budget (including zero-cost-only as an option).
- Approve the source shortlist and licensing/retention approach.
- Select the NVIDIA historical decision timestamp, forecast horizon, and outcome metric.
- Only then design adapters and ingestion tasks.

## Current recommendation

Proceed on paper with SEC EDGAR + GDELT + limited Alpha Vantage evaluation. Keep X conditional on measured cost, Reddit blocked pending explicit approval, and Stocktwits out of phase 1. This is a provisional design, not a claim that access has been granted or that any data has been collected.
