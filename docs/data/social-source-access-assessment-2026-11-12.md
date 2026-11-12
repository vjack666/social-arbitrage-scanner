# Social Source Access Assessment — NVIDIA Q3 FY2027 Pilot

**Assessment date:** 2026-11-12  
**Project:** Social Arbitrage Scanner  
**Status:** `spec_ready` for owner review; no collection implementation authorized or started.  
**Budget constraint:** free or already available access only.  
**Current access state:** user reports no social APIs configured. This review did not verify any API credentials, account approval, or connected social data source.

## Decision

**Do not implement or run a social collector yet.** Keep the social evidence input marked `missing` until a source is authorized and connected. Do not substitute search-engine snippets, manual browsing, unofficial scrapers, or today's public posts for a historical social dataset.

## Provider findings

### X API

Official references:
- API access and rules: https://help.x.com/en/rules-and-policies/x-api
- Search Posts documentation: https://github.com/xdevplatform/docs/blob/main/x-api/posts/search/introduction.mdx
- Developer platform: https://developer.x.com/

The official Search Posts documentation describes:
- recent search for the last 7 days, available to developers;
- full-archive search back to 2006, available to pay-per-use and Enterprise customers;
- developer account, Project/App, and keys/tokens as prerequisites.

**What this means for this pilot:** no X API is configured. The official documentation does not establish that this specific project currently has approved access or that full historical backfill is free. Recent-only access, even if available after account setup, cannot reconstruct social posts and retrieval state for decision timestamps before collection began. Exact pricing/credit terms and developer-console eligibility remain unverified.

**Next gate:** check current account eligibility and endpoint pricing directly in the official developer console/docs. No API calls or credentials should be used until access, permitted use, retention, and budget are approved.

### Reddit Data API

Official references:
- Developer access guidance updated 2026-05-28: https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data
- Data API Terms, last revised 2026-07-20: https://redditinc.com/policies/data-api-terms
- Technical guidance: https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki

Reddit's guidance says API use requires registered/authenticated access and compliance with its terms. It says commercial use requires explicit permission and a contract, while research use is directed to Reddit for Researchers. The terms also restrict use of user content for machine-learning/model training without explicit permission.

**What this means for this pilot:** approval and permitted use have not been established. The project's eventual commercial status is not confirmed, so we must not assume non-commercial eligibility. No Reddit data collection is authorized by this assessment.

**Next gate:** owner clarifies intended use (personal non-commercial research vs product/business), then pursues the appropriate official access/review route. Until approval, no scraping, unofficial dumps, or alternate accounts to bypass access restrictions.

### Stocktwits

Official references:
- Developer registration: https://api.stocktwits.com/developers
- Terms: https://stocktwits.com/about/legal/terms/

The developer page says new API registrations are not currently being accepted while APIs, documentation, and terms are reviewed. The terms prohibit automated scraping/data extraction unless expressly authorized.

**Decision:** exclude from phase one. Recheck only if an authorized access route becomes available.

## Point-in-time constraints

- The NVIDIA event is scheduled for 2026-11-17, approximately 1:20 p.m. Pacific / 4:20 p.m. Ecuador, subject to official updates.
- The desired pre-event dataset begins before the event, but no social API was configured during the earlier period.
- Data first collected later must not be backdated. It can support only snapshots at or after its verified retrieval/availability time.
- For every future record, preserve `published_at`, `event_at`, `retrieved_at`, original timezone string, `decision_timestamp`, source URL/ID, query, access tier, terms version, verification state, duplicate/reshare relationships, and known limitations.
- Distinguish a platform's post creation time from when the collector first observed it.
- Record corrections as new versions; do not rewrite prior snapshots.
- Do not store or reuse content beyond platform permissions or retention/deletion rules.

## Missing data and non-claims

- Social posts collected by this project: **none verified**.
- Social sentiment or post-volume metrics: **not available**.
- Author diversity, coordination signals, and narrative novelty: **not measured**.
- Historical social coverage for earlier pre-event decision timestamps: **not established**.
- API permissions, access tiers, and credentials: **not configured/verified**.
- No bullish/bearish signal or numeric score should be generated from absent social evidence.

## Recommended next steps

1. Owner confirms intended use: personal/non-commercial research or possible commercial product.
2. Owner confirms zero-cost-only means no paid X archive or other paid tier.
3. Check whether an approved X developer app already exists; if not, assess eligibility and current terms. Do not assume historical full-archive access is free.
4. For Reddit, use the official access/review route appropriate to the confirmed use case.
5. After a source is approved, define a small collection scope, retention policy, duplicate rules, and a testable acceptance checklist.
6. Only after explicit owner approval, implement a source adapter and prospective capture. Historical evaluation remains limited to evidence whose availability by each decision timestamp can be demonstrated.

## Acceptance criteria before implementation

- [ ] Authorized access is documented for each enabled source.
- [ ] Intended use and any commercial permission requirements are resolved.
- [ ] Free-tier and rate limits are documented; paid requests are disabled.
- [ ] Point-in-time timestamps and first-seen retrieval times are distinct.
- [ ] Duplicate/syndication/repost relationships can be represented without counting copies as independent evidence.
- [ ] Deleted content and retention rules have a compliant handling plan.
- [ ] Missing social data propagates as `missing/insufficient_evidence`, never as neutral sentiment or zero volume.
- [ ] Owner approves the design before implementation.
