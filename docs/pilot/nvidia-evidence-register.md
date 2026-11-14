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

## Snapshot log — 2026-11-13

**Decision timestamp:** 2026-11-13T08:49:22-05:00 (America/Guayaquil; 13:49:22Z). Sources whose availability by this cutoff cannot be established are excluded from this snapshot, even if currently indexed with a Nov 13 date.

| record_id | source_type | publisher | title_or_claim | canonical_url | published_at | event_at | retrieved_at | decision_timestamp | verification_status | duplicate_group | eligible_for_snapshot | claim_class | notes_and_limitations | dataset_or_parser_version |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NVDA-20261113-SEC-001 | SEC filing | SEC EDGAR | NVIDIA Form 8-K, Item 5.02: board accepted Jensen Huang's resignation; Colette Kress appointed interim CEO; Harvey C. Jones appointed board chair | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm | Filing/report date 2026-11-12; exact SEC acceptance/publication time not shown on opened filing page | Filing states board action occurred 2026-11-11; no clock time given | 2026-11-13T08:49:22-05:00 | 2026-11-13T08:49:22-05:00 | primary_source | CEO_TRANSITION_20261112 | yes — SEC filing opened and contents checked | verified_fact | Accession identifier in URL: 0001045810-26-000082. The SEC filing lists date of earliest event reported as Nov 11, while the NVIDIA newsroom announcement is dated Nov 12. This is a date distinction, not necessarily a contradiction: board action date and public announcement date differ. Do not infer exact public availability time from the filing date alone. | evidence-register-v0.3 |
| NVDA-20261112-MARKET-002 | market data | Yahoo Finance historical prices | NVDA Nov 12 regular-session close $166.19; open $151.01, high $167.14, low $148.80; displayed volume 742,789,000 | https://finance.yahoo.com/quote/NVDA/history/ | Historical session row dated 2026-11-12; exact row publication time unavailable | Regular-session close 4:00 p.m. ET (21:00Z / 16:00 Ecuador) | 2026-11-13T08:49:22-05:00 | 2026-11-13T08:49:22-05:00 | corroborated | NVDA_CLOSE_20261112 | yes — historical session had closed before cutoff | measurement | Secondary public historical quote page; systematic storage/redistribution terms not verified. A second quote aggregator reports close $166.19 and volume 747,979,146, so price agrees but volume differs by about 5.19M shares. Preserve each provider's value; no independent exchange tape validation in this run. | evidence-register-v0.3 |
| QQQ-20261112-MARKET-001 | market data | Yahoo Finance historical prices | Invesco QQQ Trust close $688.17; open $680.32, high $694.56, low $679.83; displayed volume 36,718,000 | https://finance.yahoo.com/quote/QQQ/history/ | Historical session row dated 2026-11-12; exact row publication time unavailable | Regular-session close 4:00 p.m. ET | 2026-11-13T08:49:22-05:00 | 2026-11-13T08:49:22-05:00 | measurement | QQQ_CLOSE_20261112 | yes — historical session had closed before cutoff | measurement | QQQ is an ETF proxy for Nasdaq-100 exposure, not the index itself. Historical price page; terms for systematic reuse not verified. | evidence-register-v0.3 |
| SOXX-20261112-MARKET-001 | market data | Yahoo Finance historical prices | iShares Semiconductor ETF close $154.99; open $150.47, high $157.63, low $150.03; displayed volume 52,094,000 | https://finance.yahoo.com/quote/SOXX/history/ | Historical session row dated 2026-11-12; exact row publication time unavailable | Regular-session close 4:00 p.m. ET | 2026-11-13T08:49:22-05:00 | 2026-11-13T08:49:22-05:00 | measurement | SOXX_CLOSE_20261112 | yes — historical session had closed before cutoff | measurement | Sector ETF proxy, not a pure semiconductor index. Historical price page; terms for systematic reuse not verified. | evidence-register-v0.3 |
| NVDA-20261113-NEWS-001 | news article | Reuters | Article on Colette Kress as interim CEO and reported leadership/strategy issues | https://www.reuters.com/business/colette-kress-cfo-who-challenged-huangs-bets-is-nvidias-interim-ceo-2026-11-13/ | Search result dates it 2026-11-13; exact publication time unavailable | Not applicable; contains reported claims and analysis | 2026-11-13T08:49:22-05:00 | 2026-11-13T08:49:22-05:00 | excluded | CEO_TRANSITION_20261112 | no — cannot substantiate that this article was publicly available by the decision cutoff | reported_claim | Excluded under strict point-in-time rule. May be reviewed in a later snapshot if its publication time/availability is verified. Reported claims about strategy and relationships are not official company facts. | evidence-register-v0.3 |
| NVDA-20261113-SOCIAL-001 | social data | Not collected | Authorized social-source evidence unavailable in this run | — | — | — | 2026-11-13T08:49:22-05:00 | 2026-11-13T08:49:22-05:00 | excluded | — | no — no authorized social API/data access verified | measurement | No social sentiment, post counts, author-diversity metrics, or engagement metrics collected. | evidence-register-v0.3 |

## Evidence-quality review — 2026-11-13

### Confirmed facts
- The SEC Form 8-K was found and opened. It reports the board action on Nov 11, gives Nov 11 as the earliest event date, and is signed/dated Nov 12. This independently verifies the transition through a regulatory filing in addition to NVIDIA's official release. It does not establish the precise public-disclosure time.
- NVIDIA's official newsroom release dated Nov 12 continues to schedule results for Nov 17 at approximately 1:20 p.m. PT and the call at 2:00 p.m. PT.
- The Nov 12 regular-session close was $166.19 for NVDA, $688.17 for QQQ, and $154.99 for SOXX according to the cited historical quote pages.

### Measurement and comparison
- NVDA closed down 4.34% on Nov 12 according to the historical quote page; QQQ closed down approximately 0.32% and SOXX down approximately 0.26% according to their respective displayed closing changes. This is consistent with NVDA underperforming these two proxies on that session; it does not establish causality or predict the earnings reaction.
- NVDA volume was unusually high in the displayed vendor data (about 743–748M shares across two quote pages). Because provider values differ and no exchange-level tape or licensing terms were verified, treat volume as indicative and vendor-specific.
- The Nov 12 close is post-announcement market reaction to the leadership news, so it is valid as a new Nov 13 pre-earnings snapshot observation, but must not be inserted retroactively into the Nov 12 decision snapshot.

### Reported claims and hypotheses
- Allegations about espionage, personal relationships, or chip shipments are not established by the SEC filing or the official transition release. They remain separate reported claims and require claim-specific corroboration.
- Any hypothesis that the transition will change customer commitments, strategy, product roadmaps, or earnings guidance is untested. NVIDIA's stated expectation of operational continuity is a company statement, not independent proof of future outcomes.

### Macro and missing data
- The U.S. Bureau of Labor Statistics calendar lists the October 2026 Producer Price Index release for Nov 13 at 8:30 a.m. Eastern Time (8:30 a.m. Ecuador time; both UTC−5 on this date). At the 8:49 a.m. Ecuador cutoff, the scheduled time had passed, but the official BLS PPI landing page still displayed September 2026 as the latest numbers and November 13 as the next release. The October results therefore were not verified as publicly posted on the official page during this run; no October value or surprise is recorded. This may reflect a publication delay or page refresh lag, not a conclusion about whether release occurred elsewhere.
- No authorized social dataset is available; social evidence remains missing.
- No documented provider license/terms for systematic storage or redistribution were verified.
- No validated API ingestion, parser, automated deduplication pipeline, or quantitative sentiment score was run.

### Point-in-time and duplicate controls
- CEO transition records share duplicate group CEO_TRANSITION_20261112. The SEC filing and NVIDIA newsroom release are distinct primary records for the same event; they corroborate the transition but do not count as separate underlying events.
- The Reuters article dated Nov 13 is excluded because its exact publication/availability time relative to the cutoff could not be verified.
- The Nov 12 market close observations are newly added to this Nov 13 snapshot only; the earlier Nov 12 snapshot remains unchanged.

## Next verification tasks
1. Retrieve the actual BLS PPI release and record its exact publication time, headline/core values, revisions, and consensus comparison only where the source supports them.
2. Verify the earnings schedule again against NVIDIA's official notice.
3. Continue a vendor-separated NVDA/QQQ/SOXX time series and investigate the NVDA volume discrepancy.
4. Document provider terms before treating market data as suitable for systematic ingestion or redistribution.
5. Keep social evidence missing until authorized access and permitted use are documented.
6. Keep earnings results and post-event evaluation in a separate dataset, not the pre-event snapshots.

## Review checklist

- [x] Primary NVIDIA source opened and URL checked.
- [x] Publication date recorded; exact time left unspecified where the source does not display it.
- [x] Timezone preserved for decision timestamps and market observation times.
- [x] Event time kept separate from publication time.
- [x] Snapshot cutoffs stated and prior snapshots retained.
- [x] SEC Form 8-K retrieved and checked.
- [x] Duplicate relationships recorded for the same underlying leadership event.
- [ ] Actual PPI release values verified.
- [ ] Market data provider terms reviewed for systematic storage/reuse.
- [ ] Social access authorization verified.
- [ ] NVDA versus index/sector time series fully validated.

## Important

A page found later with a historical publication date can support retrospective reconstruction only where its timestamp and historical availability can be substantiated. Label it as retrieved retrospectively, not as collected live at the time. Search snippets and inaccessible article bodies are partial evidence and must be marked accordingly.


## Snapshot log — 2026-11-14

**Decision timestamp:** 2026-11-14T08:52:29-05:00 (America/Guayaquil; 13:52:29Z). Weekend review. The latest completed regular U.S. equity session is Friday, Nov 13. Market rows below are historical provider pages retrieved during this run; they are not live quotes. This snapshot includes only pages found accessible by this decision cutoff.

| record_id | source_type | publisher | title_or_claim | canonical_url | published_at | event_at | retrieved_at | decision_timestamp | verification_status | duplicate_group | eligible_for_snapshot | claim_class | notes_and_limitations | dataset_or_parser_version |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NVDA-20261114-SEC-001 | SEC filing | SEC EDGAR | Form 8-K confirms board action dated Nov 11: resignation of Jensen Huang, interim CEO Colette Kress, Harvey C. Jones as chair | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/0001045810-26-000082-index.htm | SEC accepted 2026-11-12 08:52:41 UTC (03:52:41 Ecuador); filed Nov 12 | Board action stated as Nov 11; effective immediately | 2026-11-14T08:52:29-05:00 | 2026-11-14T08:52:29-05:00 | primary_source | CEO_TRANSITION_20261112 | yes | verified_fact | Regulatory primary source. The acceptance timestamp is explicitly UTC in SEC header; converted to Ecuador time (UTC−5). Confirms official transition, not the truth of allegations in unrelated news reports. | evidence-register-v0.4 |
| NVDA-20261114-COMPANY-001 | company release | NVIDIA Newsroom | Earnings release remains scheduled for Nov 17 at approximately 1:20 p.m. PT; call at 2:00 p.m. PT | https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition | Page dated 2026-11-12; exact publication time not displayed | Planned results release Nov 17 approx. 1:20 p.m. PT (4:20 p.m. Ecuador); call 2 p.m. PT (5 p.m. Ecuador) | 2026-11-14T08:52:29-05:00 | 2026-11-14T08:52:29-05:00 | primary_source | NVDA_Q3_FY27_EVENT | yes | verified_fact | Rechecked in this run. Schedule remains subject to official update. | evidence-register-v0.4 |
| PPI-20261114-MACRO-001 | macro/context | U.S. Bureau of Labor Statistics | October 2026 PPI: final demand +0.3% m/m seasonally adjusted; +6.5% y/y unadjusted; final demand less foods, energy, and trade services +0.5% m/m and +4.9% y/y | https://www.bls.gov/news.release/archives/ppi_11132026.htm | Release states embargo until 2026-11-13 08:30 a.m. ET (13:30 UTC / 08:30 Ecuador) | October 2026 price data | 2026-11-14T08:52:29-05:00 | 2026-11-14T08:52:29-05:00 | primary_source | US_PPI_OCT_2026 | yes — official archived release confirms publication date/time | measurement | Corrects the previous run's open verification task: this release was subsequently found on the official BLS archive. No consensus estimate is recorded because it was not verified from an authoritative source in this run. Macro context only, not a direct NVDA signal. | evidence-register-v0.4 |
| NVDA-20261113-MARKET-001 | market data | StockAnalysis historical prices | NVDA close $162.85; open $169.91, high $170.00, low $158.39; volume 366,463,971 shares | https://stockanalysis.com/stocks/nvda/history/ | Session date 2026-11-13; provider publication timestamp not shown | Regular session close 4:00 p.m. ET (21:00 UTC / 16:00 Ecuador) | 2026-11-14T08:52:29-05:00 | 2026-11-14T08:52:29-05:00 | measurement | NVDA_CLOSE_20261113 | yes | measurement | Public historical page. Yahoo Finance shows same close but volume 363,819,700, a difference of about 2.64M shares. Preserve vendor-specific volume values; no exchange tape validation or provider license review was completed. | evidence-register-v0.4 |
| QQQ-20261113-MARKET-001 | market data | Yahoo Finance historical prices | QQQ close $679.89; intraday OHLC shown on provider page | https://finance.yahoo.com/quote/QQQ/history/ | Session date 2026-11-13; provider publication timestamp not shown | Regular session close 4:00 p.m. ET | 2026-11-14T08:52:29-05:00 | 2026-11-14T08:52:29-05:00 | measurement | QQQ_CLOSE_20261113 | yes | measurement | QQQ is an ETF proxy for Nasdaq-100, not the index itself. The English page's historical row was not present in the retrieved snippet; the displayed close is visible in the provider page header. Vendor access terms for systematic reuse remain unverified. | evidence-register-v0.4 |
| SOXX-20261113-MARKET-001 | market data | Yahoo Finance historical prices | SOXX close $149.30; open $153.32, high $154.37, low $144.64; volume 47,793,700 shares | https://finance.yahoo.com/quote/SOXX/history/ | Session date 2026-11-13; provider publication timestamp not shown | Regular session close 4:00 p.m. ET | 2026-11-14T08:52:29-05:00 | 2026-11-14T08:52:29-05:00 | measurement | SOXX_CLOSE_20261113 | yes | measurement | Semiconductor-sector ETF proxy, not a pure index. Provider terms for systematic reuse remain unverified. | evidence-register-v0.4 |
| NVDA-20261113-NEWS-001 | news article | Reuters | Reported sector selloff and uncertainty about NVIDIA leadership and financing strategy | https://www.reuters.com/business/neoclouds-ai-stocks-slide-again-nvidia-turmoil-rattles-sector-2026-11-13/ | Dated 2026-11-13; exact publication time not displayed in accessible result | U.S. market session 2026-11-13; article reports Nasdaq-100 down 2% and semiconductor index down 5.1% | 2026-11-14T08:52:29-05:00 | 2026-11-14T08:52:29-05:00 | corroborated for general market narrative; article body not fully inspected | CEO_TRANSITION_20261112; AI_SECTOR_SELL_OFF_20261113 | yes as a dated secondary report available at retrieval; not independent confirmation of the CEO transition | reported_claim | Exact article publication time and full-body verification unavailable from the accessible result. Reported index moves are not independently validated here. Any allegation within this or related coverage remains a reported claim, not an established fact. | evidence-register-v0.4 |
| NVDA-20261114-SOCIAL-001 | social data | Not collected | Authorized social-source evidence unavailable | — | — | — | 2026-11-14T08:52:29-05:00 | 2026-11-14T08:52:29-05:00 | excluded | — | no | measurement | No authorized social API access or license verified. No social sentiment, post counts, author-diversity or engagement metrics collected. | evidence-register-v0.4 |

## Evidence-quality review — 2026-11-14

### Confirmed facts
- SEC EDGAR provides a primary Form 8-K for the transition (accession 0001045810-26-000082), accepted at 2026-11-12 08:52:41 UTC. NVIDIA's official newsroom release remains the controlling company source for confirming the transition and scheduled results event.
- NVIDIA's official release still schedules Q3 FY2027 results for Nov 17 at approximately 1:20 p.m. Pacific and the earnings call at 2:00 p.m. Pacific.
- BLS's archived official October PPI release states the embargo lifted at 8:30 a.m. ET on Nov 13. Final demand rose 0.3% m/m and 6.5% y/y; core-style final demand less foods, energy and trade services rose 0.5% m/m and 4.9% y/y. This resolves the previous snapshot's missing-PPI task, without retroactively changing that snapshot.
- Historical market pages show Nov 13 closes: NVDA $162.85, QQQ $679.89 and SOXX $149.30. These are provider-reported close values, not a validated licensed market dataset.

### Measurements and contradictions
- NVDA's Nov 13 close was down 2.01% per the historical pages; SOXX was down 3.67%. QQQ's close of $679.89 versus $688.17 on Nov 12 implies a decline of about 1.20%. These are descriptive price changes only; they do not establish causality.
- NVDA volume differs between StockAnalysis (366.46M) and Yahoo Finance (363.82M). Keep both values and investigate conventions; do not average.
- Reuters describes broad AI/semiconductor weakness and questions about vendor financing. Because the full article body and exact publication timestamp were not available from the retrieved result, use only as a secondary reported narrative, not as independently verified numerical evidence.
- Some media reports contain allegations involving personal relationships, espionage or chip shipments. Those remain distinct reported claims. Neither the SEC filing nor NVIDIA's official transition release establishes them as facts.

### Point-in-time controls and limitations
- Decision cutoff is 2026-11-14T08:52:29-05:00. Friday's completed regular-session market close is eligible as the latest pre-event snapshot observation. It must not be inserted into the earlier Nov 12 or Nov 13 snapshots.
- The PPI result was published Nov 13 at 08:30 ET and was accessible during this Nov 14 run. The earlier Nov 13 run's failure to find it is preserved as a collection gap; this entry is a later correction, not a rewrite of the earlier state.
- Social evidence is missing because no authorized source access was verified.
- Market provider licensing terms for systematic storage/redistribution remain unverified; no API ingestion or automated sentiment score was run.
- No numeric bullish/bearish score or trade recommendation is produced.

## Next verification tasks — 2026-11-14
1. Recheck NVIDIA's official earnings schedule before Nov 17.
2. Continue provider-separated NVDA/QQQ/SOXX daily data; resolve volume differences against a documented exchange/provider source and review reuse terms.
3. Check for new company filings and official statements, preserving publication/acceptance timestamps.
4. Keep claims about espionage or chip shipments isolated until each has independent, credible evidence.
5. Keep authorized social evidence marked missing unless access and permitted use are documented.
6. Evaluate earnings results and post-event market reaction in a separate evaluation dataset after the event; never backfill them into these pre-event snapshots.

## Review checklist — 2026-11-14

- [x] NVIDIA primary release rechecked.
- [x] SEC filing and acceptance timestamp verified.
- [x] Official BLS October PPI release retrieved; previous gap corrected as a new dated record.
- [x] Friday Nov 13 closes captured as provider-specific historical observations.
- [x] Volume discrepancy preserved rather than blended.
- [x] Snapshot cutoff and retrieval timezone recorded.
- [ ] Provider terms for systematic market-data use verified.
- [ ] Social access authorization verified.
- [ ] Full Reuters article body and publication timestamp verified.
- [ ] Sector/index price series validated from an authorized documented provider.


## Snapshot addendum — Elon Musk commentary — 2026-11-14

**Decision timestamp:** 2026-11-14T14:20:00-05:00 (America/Guayaquil; 19:20:00Z), based on the current run time supplied to the assistant. This is an addendum to the Nov 14 snapshot, not a rewrite of earlier snapshots. The items below are reported comments; no authorized X/social-data collection was performed.

| record_id | source_type | publisher | title_or_claim | canonical_url | published_at | event_at | retrieved_at | decision_timestamp | verification_status | duplicate_group | eligible_for_snapshot | claim_class | notes_and_limitations | dataset_or_parser_version |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NVDA-20261114-MUSK-001 | news report of social post | Reuters | Musk said NVIDIA could lose “critical” deals without Jensen Huang, arguing that important arrangements depended on personal trust and were in some cases “a handshake with Jensen, not a written contract” | https://www.reuters.com/business/musk-says-nvidia-will-lose-critical-deals-without-jensen-huang-2026-11-14/ | 2026-11-14 14:50:01 UTC (09:50:01 Ecuador, UTC−5), as reported in the Reuters result | Musk's X post reported as occurring Saturday, Nov 14; exact original post time not independently verified | 2026-11-14T14:20:00-05:00 | 2026-11-14T14:20:00-05:00 | corroborated as a Reuters report; original post not independently accessed | MUSK_ON_HUANG_LEADERSHIP_20261114 | yes — Reuters result was available before cutoff | reported_claim | Musk's assessment/opinion, not verified evidence that contracts will be lost. Reuters is one underlying report; syndications of it are duplicates, not independent confirmation. NVIDIA/SEC primary sources describe a resignation; do not rewrite that as “ousted” absent primary evidence. No direct X collection or social metrics. | evidence-register-v0.5 |
| NVDA-20261113-MUSK-002 | news report of social post | Yahoo Finance / cited article by Badar Shaikh | Musk replied “That would be an honor” to a suggestion that he hire Jensen Huang | https://finance.yahoo.com/technology/ai/articles/elon-musk-says-honor-hire-193005822.html | 2026-11-13 14:30 ET (19:30 UTC) as displayed by Yahoo Finance; exact original X post time reported as Nov 12, 2026 | X exchange reportedly occurred Nov 12; exact time not verified | 2026-11-14T14:20:00-05:00 | 2026-11-14T14:20:00-05:00 | secondary_report; quote reproduced by outlet, original post not independently accessed | MUSK_ON_HUANG_LEADERSHIP_20261114 | yes — secondary report was available before cutoff | reported_claim | This is an expression of willingness/opinion, not a formal job offer, employment negotiation, or confirmed hiring plan. The Yahoo item and any syndications of the same report must not be counted as independent sources. No authorized social data was collected. | evidence-register-v0.5 |
| NVDA-20260925-MUSK-003 | news report of social post | The Motley Fool via Yahoo Finance | Musk reportedly said xAI/SpaceX's Colossus 2 could add substantial NVIDIA GPU capacity by year-end and described NVIDIA chips as the exclusive choice for SpaceX going forward | https://finance.yahoo.com/markets/stocks/articles/elon-musk-just-gave-nvidia-002000003.html | 2026-09-27 00:20 UTC approx. based on displayed Yahoo timestamp; underlying original post dates reported as Sep 25, exact post times not independently verified | Statements reportedly made Sep 25, 2026 | 2026-11-14T14:20:00-05:00 | 2026-11-14T14:20:00-05:00 | secondary_report; original post not independently accessed | MUSK_NVIDIA_DEMAND_CONTEXT_20260925 | yes — historical context only, published before this cutoff | reported_claim | Historical demand context, not proof of a binding purchase order, shipment, recognized revenue, or the company's Q3 FY2027 guidance. Musk leads companies that are NVIDIA customers and also has AI-compute interests; treat as interested-party commentary. Do not count reprints as independent confirmation. | evidence-register-v0.5 |

### Elon Musk commentary — evidence-quality interpretation

**Reported statements**
- On Nov 14, Musk publicly criticized the leadership change in commercial terms: he argued that some important customer relationships depended on Jensen Huang's personal trust and could be at risk. Reuters reported the statement; the original X post was not independently retrieved in this run.
- A separate report says Musk responded “That would be an honor” when a user suggested hiring Huang. This is not a formal offer or evidence of a hiring process.
- Earlier commentary attributed to Musk described ambitious expansion of Colossus 2 and a preference for NVIDIA chips. This is potentially relevant demand context, but remains a customer/partner executive's public statement, not audited purchase or shipment data.

**What it may mean for the pilot (inference, not fact)**
- Leadership transition may introduce uncertainty around relationship-dependent customer commitments. This is a hypothesis to test against NVIDIA's official disclosures, subsequent customer statements, and disclosed revenue/customer concentration—not a confirmed loss of business.
- Musk's reported positive comments and stated NVIDIA compute plans can be a countervailing qualitative demand signal, but cannot establish order size, timing, shipment completion, or revenue recognition.
- These statements are not independent confirmations of one another: they concern related leadership/customer themes, and secondary outlets may reproduce the same underlying X posts.

**Missing / limitations**
- No authorized direct X access, API terms, original post IDs, full engagement counts, author-network data, or social sentiment dataset was collected.
- Exact original X publication times were not verified. The Reuters report timestamp is used only as the news publisher's timestamp; it is not substituted for the original post time.
- No numeric score or directional trading recommendation is derived from these comments.
- Continue separating the official NVIDIA/SEC leadership record from unverified allegations about espionage or chip shipments. Musk's comments do not substantiate those allegations.

### Next verification tasks
1. Retrieve the original Musk X posts through an authorized access path and record post IDs, exact timestamps/timezones, edit/deletion state, and applicable access terms; otherwise retain the social-evidence-missing caveat.
2. Search NVIDIA's official filings and earnings materials for customer concentration, commitments, demand visibility, and any disclosed risks related to leadership or customer relationships.
3. Look for direct statements from NVIDIA and relevant customer companies; deduplicate articles that reproduce the same post.
4. Keep all earnings results and post-event price action outside the pre-event evidence snapshot.
