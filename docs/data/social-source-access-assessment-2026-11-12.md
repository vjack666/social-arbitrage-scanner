# Social Source Access Assessment — NVIDIA Q3 FY2027 Pilot

**Assessment date:** 2026-11-12  
**Declared use:** Personal, non-commercial research.  
**Budget:** Zero cost or valid existing access only.  
**Status:** spec_ready for owner review; implementation not authorized or started.  
**Access state:** User reports no social APIs configured. No credentials, approvals, entitlements, or source connections were verified.

## Decision

Keep social collection blocked; do not implement a collector yet. No zero-cost social API entitlement is currently established for this project. Social evidence must remain missing, not neutral/zero and not a bullish or bearish signal. Do not scrape, automate browser access, use unofficial dumps, or bypass access controls.

## X API

Official references:
- API overview/rules: https://help.x.com/en/rules-and-policies/x-api
- Developer platform/pricing: https://developer.x.com/
- Pricing documentation: https://docs.x.com/x-api/getting-started/pricing
- Developer guidelines: https://github.com/xdevplatform/docs/blob/main/developer-guidelines.mdx

The current official developer platform lists post reads at $0.005 per resource fetched under credit-based pay-per-use. Free scaled access is described for qualifying public-utility apps; this project has not been shown to qualify. Recent search cannot reconstruct historical capture timestamps, and full-archive access is not established as free.

**Decision:** do not call the API under the strict zero-cost rule unless the owner confirms an already-valid approved entitlement or credits covering the planned reads. No payment card, purchase, auto-recharge, or paid access without explicit approval.

## Reddit

Official references:
- Developer access guidance (updated 2026-05-28): https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data
- Reddit for Researchers (updated 2026-10-05): https://support.reddithelp.com/hc/en-us/articles/49381918834964-Reddit-for-Researchers-Program
- Public Content Policy: https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy

Reddit's current guidance says the only authorized avenue for research using Reddit data is Reddit for Researchers (RFR). RFR is free for approved non-commercial academic projects but requires accredited-university affiliation, institutional email, a detailed proposal, ethics review/exemption and institutional sponsor. Its dataset is delayed by six months and excludes deleted content.

The owner has declared personal non-commercial research, but no qualifying academic affiliation or sponsor is established. RFR eligibility is therefore not established. Do not use ordinary Data API signup or scraping as a workaround. No Reddit collection unless eligibility and approval are established.

## Stocktwits

Official references:
- Developer registration: https://api.stocktwits.com/developers
- Terms: https://stocktwits.com/about/legal/terms/

New API registrations are currently not accepted according to the developer page. Terms prohibit automated extraction unless expressly authorized. Exclude from phase one.

## Current source status

| Source | Zero-cost route established? | Decision |
|---|---|---|
| X API | No; existing entitlement/credits not checked or confirmed | Block until verified |
| Reddit | No; RFR eligibility and approval not established | Block |
| Stocktwits | No new API registrations currently | Exclude |
| Social posts/metrics in this project | None verified | Mark missing |

## NVIDIA pilot and point-in-time integrity

- This review collected no social posts or metrics; it is an access-policy review only.
- No historical social dataset has been verified for earlier pre-event decision timestamps.
- Data first collected later must not be backdated. Keep publication, event, retrieval/first-seen, original timezone, UTC timestamp and decision timestamp separate.
- Record source ID/URL, query, access tier, terms version, parser version, duplicate/repost/quote relationships, verification state and coverage limitations where permitted.
- Preserve corrections as new versions. Follow provider deletion, retention, redistribution and model-use rules.
- Missing social input must propagate as missing/insufficient_evidence, never as neutral sentiment or zero attention.

## Next technical steps

1. Access check only: owner may inspect their X developer console for an approved app and valid free entitlement/credits. Do not share credentials in chat or buy credits.
2. If no qualifying X entitlement exists, leave X blocked and proceed without social data under the zero-cost constraint.
3. Do not apply to Reddit RFR unless academic eligibility, sponsorship and ethics requirements can genuinely be met.
4. Keep Stocktwits excluded until an authorized API route opens.
5. Continue specification work only: fields, duplicate/repost handling, missing-data propagation, deletion/retention handling and acceptance tests.
6. Before coding, present the proposed adapter design, $0 cost proof, access evidence and acceptance tests for explicit owner approval.

## Acceptance criteria before implementation

- [ ] Approved source access is documented and permitted for this use.
- [ ] Planned use costs $0; no paid fallback or auto-recharge is enabled.
- [ ] Endpoint limits, retention, deletion, model-use and redistribution terms are documented.
- [ ] Publication, event, retrieval/first-seen and decision timestamps are distinct.
- [ ] Duplicates, syndications, reposts and quotes are not counted as independent corroboration.
- [ ] Missing social data propagates as missing/insufficient_evidence.
- [ ] Historical data is used only if availability by each decision timestamp can be demonstrated.
- [ ] Owner approves the design before implementation.