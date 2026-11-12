# NVIDIA Pilot — Evidence Register

**Status:** Initial public-source snapshot recorded for 2026-11-12. This is a retrospective web retrieval snapshot taken during this run, not a continuously collected live feed or a complete dataset.

**Decision timestamp:** 2026-11-12T12:24:26-05:00 (America/Guayaquil; 17:24:26Z).  
**Event anchor:** NVIDIA's official Q3 FY2027 results release is scheduled for 2026-11-17 at approximately 1:20 p.m. Pacific / 4:20 p.m. Ecuador time, with an earnings call at 2:00 p.m. Pacific / 5:00 p.m. Ecuador time. Recheck the official company notice before the event.

## Register fields

| Field | Required meaning |
|---|---|
| `record_id` | Stable unique ID |
| `source_type` | SEC filing, company release, news article, market data, social data, macro/context |
| `publisher` | Original publisher/provider, not just an aggregator |
| `title_or_claim` | Concise description of the item |
| `canonical_url` | Direct source URL or stable provider ID |
| `published_at` | Original publication timestamp and timezone, if available |
| `event_at` | Time the underlying event happened, if known |
| `retrieved_at` | Actual time our process retrieved the item |
| `decision_timestamp` | Snapshot cutoff against which eligibility is judged |
| `verification_status` | primary_source, corroborated, unverified, disputed, retracted, excluded |
| `duplicate_group` | ID linking syndications/reposts of the same underlying item |
| `eligible_for_snapshot` | yes/no, with reason |
| `claim_class` | verified_fact, reported_claim, measurement, inference |
| `notes_and_limitations` | Missing timestamps, licensing limits, sampling issues, corrections |
| `dataset_or_parser_version` | Reproducibility identifier |

## Snapshot log — 2026-11-12

| record_id | source_type | publisher | title_or_claim | canonical_url | published_at | event_at | retrieved_at | decision_timestamp | verification_status | duplicate_group | eligible_for_snapshot | claim_class | notes_and_limitations | dataset_or_parser_version |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NVDA-20261112-COMPANY-001 | company release | NVIDIA Newsroom | Jensen Huang resigned as President, CEO and board member effective immediately; Colette Kress appointed interim CEO; Harvey C. Jones appointed board chair; search for permanent CEO initiated | https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition | 2026-11-12; exact publication time not displayed on accessible page | Effective immediately; exact effective timestamp not displayed | 2026-11-12T12:24:26-05:00 | 2026-11-12T12:24:26-05:00 | primary_source | CEO_TRANSITION_20261112 | yes — primary source accessible during this run | verified_fact | Official release confirms the leadership transition and says results remain scheduled for Nov 17. Do not infer a more precise release time than the page provides. | evidence-register-v0.2 |
| NVDA-20261112-NEWS-001 | news article | Reuters | Market response and reported uncertainty following NVIDIA leadership news; article search result reports index moves and semiconductor/AI-sector context | https://www.reuters.com/business/nasdaq-futures-fall-nvidia-turmoil-rattles-ai-stocks-2026-11-12/ | 2026-11-12; exact publication time not available in the accessible result | Market observations in article include 9:45 a.m. ET; this is observation time, not publication time | 2026-11-12T12:24:26-05:00 | 2026-11-12T12:24:26-05:00 | unverified | CEO_TRANSITION_20261112 | yes, as a reported secondary account; not independent confirmation of the transition | reported_claim | Full Reuters page was not accessible in this retrieval; details here are limited to the returned article summary. Reported market observations may be time-sensitive and were not independently tick-verified. Any allegation reported in the story remains an allegation, not an established fact. | evidence-register-v0.2 |
| NVDA-20261111-MARKET-001 | market data | Yahoo Finance historical prices | NVDA regular-session close $173.73 on Nov 11; open $172.80, high $177.54, low $170.77; displayed volume 313,417,400 shares | https://finance.yahoo.com/quote/NVDA/history/ | Data session date 2026-11-11; provider's publication timestamp for the historical row not shown | 2026-11-11 regular session; close 4:00 p.m. ET as displayed on Yahoo Finance | 2026-11-12T12:24:26-05:00 | 2026-11-12T12:24:26-05:00 | corroborated | NVDA_CLOSE_20261111 | yes, as provisional historical market context | measurement | Historical data is available in the page, but provider terms/licensing for systematic storage and redistribution were not verified. Displayed volume differs from other accessible quote aggregators (roughly 339.0–339.2M); do not resolve discrepancy by averaging. Keep vendor-specific values separate pending primary exchange/provider verification. This is prior-session data, not the Nov 12 reaction to the leadership announcement. | evidence-register-v0.2 |
| NVDA-20261112-SEC-001 | SEC filing | SEC EDGAR | Search for a contemporaneous SEC filing covering the leadership transition | https://www.sec.gov/edgar/search/ | Not verified | Unknown | 2026-11-12T12:24:26-05:00 | 2026-11-12T12:24:26-05:00 | excluded | CEO_TRANSITION_20261112 | no — no specific filing was successfully retrieved and checked in this run | reported_claim | This row records a verification gap, not evidence that no filing exists. Find and verify the exact filing/accession before using it. | evidence-register-v0.2 |
| NVDA-20261112-SOCIAL-001 | social data | Not collected | Authorized social-source evidence unavailable in this run | — | — | — | 2026-11-12T12:24:26-05:00 | 2026-11-12T12:24:26-05:00 | excluded | — | no — no authorized social API/data access verified | measurement | No social sentiment, post counts, author-diversity metrics, or engagement metrics collected. Do not substitute search snippets or scraped metrics for authorized data. | evidence-register-v0.2 |

## Evidence-quality review

### Confirmed facts
- NVIDIA's own newsroom release confirms the leadership transition, interim CEO, board chair appointment, CEO search, and the scheduled earnings date. This is the controlling source for the transition.
- The same release says the earnings release remains scheduled for Nov 17 at approximately 1:20 p.m. PT, followed by the call at 2:00 p.m. PT.

### Reported claims and interpretations — not established facts
- News reports describe market uncertainty and allegations surrounding the departure. The allegations are not confirmed by the official NVIDIA release and must remain separately labeled reported claims unless independently substantiated by credible primary evidence.
- Claims about likely future strategy, customer financing, export-control exposure, or the direction of NVDA shares are interpretations/hypotheses, not verified facts.

### Market data quality
- The Nov 11 close is a pre-announcement baseline. Do not mix it with post-announcement trading or later after-hours/overnight prices in this pre-event snapshot.
- Vendor volume values conflict: Yahoo Finance displays 313.4M shares, while other accessible aggregators show approximately 339.0–339.2M. These may reflect differing data conventions or a vendor error; the reason is unresolved. Do not manufacture a single reconciled figure.
- Provider access/licensing terms have not been verified for systematic ingestion or redistribution. Treat this as manually accessed public page data pending a documented provider decision.

### Missing data
- No verified SEC accession/filing record was captured.
- No authorized social-source dataset is available; social evidence is missing.
- No point-in-time price/volume series for NVDA versus Nasdaq-100 and a semiconductor benchmark was collected. No reproducible macro/sector dataset was assembled in this run.
- No API-based collection, parser, deduplication job, or quantitative score was run. This register documents manually retrieved public sources only.

### Duplicate and point-in-time controls
- The official NVIDIA release is the primary record for the leadership transition. Reuters coverage is grouped under the same event and must not count as independent confirmation of that same fact.
- Decision cutoff is 2026-11-12T12:24:26-05:00. No information first published after this cutoff belongs in this snapshot. Later corrections must be appended as new records/versioned updates, not silently substituted into this record.
- The market close record is for Nov 11 and is explicitly labeled as historical baseline, not as a reaction to the Nov 12 news.

## Next verification tasks
1. Retrieve and record the exact SEC filing/accession, if one exists, and compare its timestamp/content with NVIDIA's official release.
2. Verify the official earnings event notice again before Nov 17.
3. Obtain documented price/volume from an exchange or provider whose timestamp conventions and access terms are known; preserve provider-specific records rather than blending conflicting volume figures.
4. Build a timestamped NVDA/Nasdaq-100/semiconductor-sector comparison using only observations available by each snapshot cutoff.
5. Keep social evidence marked missing until an authorized access path and permitted use are documented.
6. Keep Nov 17 earnings results and post-event price reaction in a separate evaluation dataset, never in the pre-event snapshot.

## Review checklist

- [x] Primary NVIDIA source opened and URL checked.
- [x] Publication date recorded; exact time left unspecified where the source does not display it.
- [x] Timezone preserved for the decision timestamp and market observation times.
- [x] Event time kept separate from publication time.
- [x] Snapshot cutoff stated.
- [x] Secondary coverage linked to the underlying event; not counted as independent confirmation of the same fact.
- [ ] SEC filing/accession independently retrieved and checked.
- [ ] Market data provider terms reviewed for systematic storage/reuse.
- [ ] Social access authorization verified.
- [ ] NVDA versus index/sector time series collected and validated.

## Important

A page found today with a historical publication date can support a retrospective reconstruction only where its timestamp and historical availability can be substantiated. Label it as retrieved retrospectively, not as collected live at the time. Search snippets and inaccessible article bodies are partial evidence and must be marked accordingly.
