# Data Source Strategy — v0.2

**Status:** Research and planning only. No API keys have been configured and no live ingestion has been implemented. Access, cost, and terms must be reconfirmed before use.

## Executive decision

Start with a low-cost, evidence-first research stack:
1. **SEC EDGAR** for primary company filings and structured financial facts.
2. **GDELT** for broad news/event discovery and time-stamped media attention.
3. **Alpha Vantage** as an initial market-data candidate for limited historical exploration, subject to rate limits and licensing.
4. **X API** only if an approved developer app is available and the budget/access model is explicitly approved. Recent search covers the last 7 days; full-archive search requires pay-per-use or Enterprise access.
5. **Reddit Data API** only after registration/authentication and required approval. Reddit says commercial use requires permission and a contract; research use is directed to Reddit for Researchers.
6. **Stocktwits** is not a phase-one dependency because its developer page says new API registrations are not currently being accepted.

Do not scrape sites or bypass platform controls when API access is unavailable. Publicly viewable content does not automatically grant permission for automated collection, storage, redistribution, or model training. No single source should be treated as complete or ground truth.

## Candidate source register

| Source | Best use | Access/cost observations | Proposed status |
|---|---|---|---|
| SEC EDGAR APIs | Primary filings, submissions, XBRL company facts | Public APIs do not require API keys. Automated access must follow SEC fair-access/security guidance. | Phase 1 — core |
| GDELT Project | News/event discovery, coverage and attention features | Describes its database and analysis service as free/open. Review terms; media-derived data can contain duplicates, delays, and machine-generated classifications. | Phase 1 — core |
| Alpha Vantage | Historical equity time series for exploratory analysis | Free-tier request limits and dataset-specific access apply; real-time and 15-minute delayed US equity data may be premium-only. Commercial use requires checking with provider. | Phase 1 — limited evaluation |
| X API | Public conversation, posts, trends, and social velocity | Official docs state recent search covers the last 7 days and is available to developers; full-archive search back to 2006 is pay-per-use/Enterprise. Requires approved developer account, Project/App, credentials, and compliance with developer terms. Exact cost depends on access and usage and must be checked before collection. | Phase 2 — conditional; not configured |
| Reddit Data API | Community discussion and emerging narratives | Requires registered/authenticated access and compliance with Data API terms. Reddit's May 2026 guidance says commercial use requires explicit permission and a contract; research is directed to Reddit for Researchers. Fees/limits depend on access and use. | Blocked pending access/use approval |
| Stocktwits API | Investor-community conversation | Developer page says new application registrations are not currently accepted while APIs and terms are reviewed. Terms prohibit unauthorized automated extraction/scraping. | Exclude from phase 1 |

## Official references

- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- SEC developer resources and fair access: https://www.sec.gov/about/developer-resources
- GDELT data and access: https://gdeltproject.org/data.html
- Alpha Vantage documentation: https://www.alphavantage.co/documentation/
- Alpha Vantage API limits and market-data notes: https://www.alphavantage.co/support/api-key/
- X API overview and rules: https://help.x.com/en/rules-and-policies/x-api
- X Search Posts documentation: https://github.com/xdevplatform/docs/blob/main/x-api/posts/search/introduction.mdx
- X developer platform: https://developer.x.com/
- Reddit developer access guidance (updated May 28, 2026): https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data
- Reddit Data API terms (last revised July 20, 2026): https://redditinc.com/policies/data-api-terms
- Reddit Data API technical guidance: https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki
- Stocktwits developer registration status: https://api.stocktwits.com/developers
- Stocktwits terms on automated extraction: https://stocktwits.com/about/legal/terms/

## Social-source assessment — 2026-11-12

No social API is configured for this project. No credentials, permissions, source connection, or collection job were verified in this review. Therefore **no social posts or social metrics were collected** and social-agent inputs must be marked missing, not zero or neutral.

### X
- Recent search: official documentation says it searches the last 7 days and is available to developers, subject to an approved developer account and app setup.
- Full archive: official documentation says archive search back to 2006 is available to pay-per-use and Enterprise customers.
- Implication for NVIDIA pilot: an affordable/free historical backfill covering the full pre-event window has not been established. New collection after setup could support prospective observations, but cannot recreate earlier snapshots that were not captured.
- Next check: inspect current developer-console eligibility and current endpoint pricing/credit rules before deciding whether recent-only collection fits the zero-cost budget. Do not create credentials in chat or start requests before owner approval.

### Reddit
- Reddit's official May 28, 2026 guidance states that Data API access requires approved developer access/authentication; commercial use requires explicit permission and a contract; its approved research path is Reddit for Researchers.
- The project's future commercial status is not yet settled, so the permitted use case cannot be assumed.
- Next check: clarify whether the project is strictly personal non-commercial experimentation or intended for a product/business, then request the appropriate access. Until approved, do not collect via unofficial scrapers or third-party dumps.

### Stocktwits
- Its developer registration page currently says new registrations are not being accepted during review of APIs, documentation, and terms.
- Its terms prohibit automated scraping/extraction unless expressly authorized.
- Next check: none for phase one unless the provider announces an authorized access route.

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

For social data specifically, also record the platform post ID when permitted, reply/repost/quote relationship where available, language, collection query, pagination/cursor, sampling method, and access tier. Avoid storing unnecessary personal data. Apply platform deletion/retention requirements. Do not use content for model training unless the relevant rights and permissions explicitly allow it.

## NVIDIA pilot: minimum source bundle

For a single historical decision time:
1. SEC filings and official company releases available by that time.
2. GDELT news/event records whose publication/first-seen timestamps precede the cutoff.
3. Price/volume history from a provider whose data rights, adjustments, and timestamp semantics are documented.
4. Social data only if authorized access and point-in-time historical coverage can be demonstrated.

If historical social data is unavailable or licensing is unclear, mark the relevant agent input as missing. Do not substitute today's search results for historical evidence. Prospective data collected after a cutoff must not be backdated into an earlier snapshot.

## Cost and access controls

Before enabling any paid source:
- estimate requests/day, records/request, and historical backfill volume;
- calculate expected monthly spend and set a provider-side and application-side cap where possible;
- log each request's cost or usage units;
- set a fail-closed budget threshold that pauses collection rather than silently exceeding budget;
- verify data redistribution, derived-data, storage, deletion, and model-training terms.

## Decision gates before implementation

- Confirm whether this remains personal research or may become a commercial product.
- Confirm acceptable monthly data budget (including zero-cost-only as an option).
- Approve the source shortlist and licensing/retention approach.
- Select the NVIDIA historical decision timestamp, forecast horizon, and outcome metric.
- Confirm access is actually granted; public web visibility is not API authorization.
- Only then design adapters and ingestion tasks.

## Current recommendation

Keep the first implementation plan on paper: SEC EDGAR + GDELT + limited Alpha Vantage evaluation. For social, do not implement a collector yet. First decide whether the project is personal/non-commercial or intended for commercial use, then check X developer eligibility for 7-day recent search under the free/existing-access constraint. Treat full historical X archive as unavailable unless an authorized tier is confirmed. Keep Reddit blocked until appropriate access/use permission is confirmed, and Stocktwits out of phase one. This is a provisional design, not a claim that access has been granted or data has been collected.
