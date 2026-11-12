# Data Source Strategy — v0.3

**Status:** Research/planning only. No social API credentials, approvals, entitlements, or live ingestion have been verified. No social collector is authorized.

## Owner constraints

- Declared use: personal, non-commercial research.
- Budget: zero cost or already-valid access only.
- No unauthorized scraping, browser automation, unofficial dumps, or bypassing platform controls.
- No implementation until the owner approves the design.

## Social source decision

### X API — blocked unless existing no-cost entitlement is verified

Official references:
- API overview/rules: https://help.x.com/en/rules-and-policies/x-api
- Developer platform/current pricing: https://developer.x.com/
- Pricing docs: https://docs.x.com/x-api/getting-started/pricing
- Developer guidelines: https://github.com/xdevplatform/docs/blob/main/developer-guidelines.mdx

The current official developer platform lists post reads at $0.005 per resource fetched under credit-based pay-per-use. It describes free scaled access for qualifying public-utility apps; no evidence establishes that this personal market-research project qualifies. Recent search is time-limited and cannot reconstruct earlier collection timestamps; full historical access is not established as free.

**Decision:** do not use X unless the owner confirms an already-approved app and valid free entitlement/credits that cover the planned reads. Do not add payment methods, buy credits, or enable auto-recharge. If no qualifying free entitlement exists, X remains unavailable under the zero-cost constraint.

### Reddit — blocked; RFR eligibility not established

Official references:
- Developer access guidance (updated 2026-05-28): https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data
- Reddit for Researchers (updated 2026-10-05): https://support.reddithelp.com/hc/en-us/articles/49381918834964-Reddit-for-Researchers-Program
- Public Content Policy: https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy

Reddit's current guidance says the only authorized avenue for research using Reddit data is Reddit for Researchers (RFR). RFR is free for approved non-commercial academic projects but requires accredited-university affiliation, institutional email, research proposal, ethics review/exemption, and institutional sponsor. Its dataset has a six-month delay and excludes deleted content.

The owner has declared personal non-commercial research, but no qualifying academic affiliation or sponsor is established. Therefore RFR eligibility is not established. Do not use ordinary API signup or scraping to work around the research policy. No Reddit collection unless eligibility and approval are genuinely established.

### Stocktwits — excluded

Official references:
- Developer registration: https://api.stocktwits.com/developers
- Terms: https://stocktwits.com/about/legal/terms/

The developer page says new API registrations are not currently accepted. Terms prohibit automated extraction unless expressly authorized. Exclude from phase one.

## Other candidate sources

- SEC EDGAR: candidate non-social source; public APIs without API keys, subject to fair-access rules. https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- GDELT: candidate non-social news/event discovery source; review terms, duplicates and machine-classification limitations. https://gdeltproject.org/data.html
- Alpha Vantage: limited market-data evaluation only; free-tier limits and dataset-specific terms apply. https://www.alphavantage.co/documentation/

## NVIDIA pilot impact

- No social posts or social metrics have been collected or verified for this project.
- No historical social dataset has been established for earlier pre-event decision timestamps.
- Mark social input as missing/insufficient evidence, never neutral, zero, bullish, or bearish.
- Data collected later must not be backdated. Separate publication time, event time, retrieval/first-seen time, timezone, UTC-normalized time, and decision timestamp.
- Record source ID/URL, query, access tier, terms version, verification state, duplicate/repost/quote relationships and limitations where permitted.
- Preserve corrections as new versions. Follow platform deletion, retention, redistribution and model-use rules. Do not train models on platform content without explicit rights.

## Gates before implementation

1. Verify approved access and $0 cost for every enabled source.
2. Document endpoint limits, purpose permissions, retention/deletion, model-use and redistribution terms.
3. Specify fields, timestamp semantics, sampling, duplicate handling and missing-data propagation.
4. Define testable acceptance criteria and demonstrate point-in-time integrity.
5. Obtain explicit owner approval of the design before creating adapters or ingestion code.

## Current recommendation

Keep social ingestion blocked. First check whether the owner already has an approved X app with valid free entitlement/credits; do not purchase access. Do not use Reddit unless RFR eligibility and approval can be demonstrated. Keep Stocktwits excluded. Continue specification work only. This is an access assessment, not a claim of access or collected data.