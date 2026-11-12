# NVIDIA Pilot — Initial Public-Source Scan (2026-11-12)

**Status:** Preliminary source inventory; not a complete dataset and not a forecast. Sources were located retrospectively on 2026-11-12. This is not evidence that the scanner was running live before that date. Collection timestamp is approximate to the research session on 2026-11-12, Ecuador time; exact retrieval times were not captured per page, so they must not be fabricated.

## Event anchor

NVIDIA's official announcement dated 2026-10-28 schedules the Q3 FY2027 results call for 2026-11-17 at 2:00 p.m. Pacific / 5:00 p.m. Eastern and says written CFO commentary will be posted after results are publicly announced at approximately 1:20 p.m. Pacific. For Ecuador on that date, 1:20 p.m. Pacific corresponds to approximately 4:20 p.m. Ecuador time. Reconfirm the exact release time immediately before the event.

Official event reference: https://nvidianews.nvidia.com/news/nvidia-sets-conference-call-for-third-quarter-financial-results-6928873

## Initial candidate records

| ID | Publication date | Source | Candidate observation | Classification/status | Point-in-time notes |
|---|---|---|---|---|---|
| NVDA-NEWS-001 | 2026-11-09 | Reuters, syndicated via Investing.com: https://www.investing.com/news/stock-market-news/wall-st-brokerages-ai-selloff-overdone-downplay-democrat-regulation-risks-5012564 | Some brokerages characterized the prior AI-stock selloff as excessive; the article highlighted NVIDIA's upcoming earnings and expected data-center revenue growth. | Reported claim; source located, original Reuters record should be preserved where available. | Published before the earnings event. Do not treat broker opinions as verified outcomes. |
| NVDA-NEWS-002 | 2026-11-10 | Reuters, syndicated via Investing.com: https://www.investing.com/news/stock-market-news/nvidia-selloff-deepens-adding-toai-jitters-5016732 | The article attributed technology weakness to inflation/rate expectations, leadership uncertainty around Jensen Huang, and complications around an Ohio data-center development. | Reported claim; requires extraction of original timestamps and claim-level corroboration. | Published before the earnings event. Separate macro drivers from company-specific narratives. |
| NVDA-NEWS-003 | 2026-11-11/12 | Reuters, syndicated via Investing.com: https://www.investing.com/news/economy-news/asian-stocks-fragile-nvidia-plummets-as-board-to-decide-ceos-fate-5020170 | Reuters reported that NVIDIA's board was considering Huang's future; the article described after-hours share weakness and uncertainty. | Reported claim; verify original article timestamp and preserve as a distinct version if updated. | Before earnings. This is a developing story; avoid treating reported deliberations as a final board decision. |
| NVDA-NEWS-004 | 2026-11-12 13:52 UTC (08:52 Ecuador, per Reuters page) | Reuters: https://www.reuters.com/business/retail-consumer/nvidia-ceo-jensen-huang-step-down-big-blow-ai-boom-2026-11-12/ | Reuters reported that Huang had resigned and Colette Kress would be interim CEO. | Confirmed company event after checking NVIDIA's official release: https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition . Reuters page timestamp is 13:52 UTC; preserve the source timestamp and record actual retrieval separately in the production dataset. | Major event inside the pre-earnings window. This is a key point-in-time boundary: records published before this timestamp must be kept distinct from reaction/analysis published afterward. |
| NVDA-NEWS-005 | 2026-11-12 | Associated Press: https://apnews.com/article/5403f152a601cf82ce939f1d24fffa0f | AP also reported Huang's resignation and Kress as interim CEO. | Corroborating news report; primary confirmation is the official NVIDIA release linked above. | Do not count outlet repetition as independent evidence if both reports derive from one underlying announcement. |
| NVDA-NEWS-006 | 2026-11-08 | NVIDIA Board statement: https://nvidianews.nvidia.com/news/statement-from-nvidia-board-of-directors | NVIDIA's board announced an independent investigation and stated it had no reason to believe national security or NVIDIA secrets had been compromised; the statement said the board had confidence in Huang and his leadership team. | Primary-source statement, date verified from official newsroom. | Outside the strict 2026-11-10 seven-day window, but useful as antecedent context. Do not mislabel it as inside-window evidence. |
| NVDA-NEWS-007 | 2026-11-08 | NVIDIA message to employees: https://nvidianews.nvidia.com/news/a-message-to-our-company | NVIDIA published a message attributed to Huang acknowledging personal misconduct and saying he remained committed to the company and would cooperate with the board investigation. | Primary-source company publication; exact time not captured. | Outside the strict seven-day window; contextual background only. |
| NVDA-FUND-001 | 2026-08-26 | NVIDIA Q2 FY2027 results: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/ | NVIDIA reported Q2 FY2027 revenue of $96.2 billion and data-center revenue of $89.0 billion; its Q3 outlook projected revenue of $108.0 billion ±2%, and did not assume data-center compute revenue from China. | Primary-source historical fundamental data. | Older than the event window; use only as pre-existing baseline context. Values must be checked against the official release before being used in calculations. |

## Preliminary interpretation (not a signal)

The candidate source set suggests two competing pre-event narratives that should be tested separately:

1. **Fundamental/AI-demand narrative:** the market was still focused on strong data-center demand and the upcoming quarterly report.
2. **Governance/leadership and policy-risk narrative:** reports about board scrutiny and leadership uncertainty may have become a dominant near-term driver, alongside macroeconomic and AI-capex concerns.

This is a narrative map, not proof that any factor caused the stock move. No sentiment score, event-return calculation, confidence score, or trade direction has been computed. Search snippets alone are not sufficient to confirm claims or establish exact publication times.

## Immediate verification tasks

- [ ] Open each original source and record the exact publication/update time and timezone.
- [x] Confirm the reported leadership change against NVIDIA's official newsroom release dated 2026-11-12: https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition . It states that Jensen Huang resigned effective immediately and Colette Kress was appointed interim CEO. The earlier board statement dated 2026-11-08 was not itself confirmation of the later transition.
- [ ] Capture NVDA and benchmark price/volume from a licensed source with session and timezone metadata.
- [ ] Collect social signals only if authorized historical access exists; otherwise mark the social input missing.
- [ ] Create a timestamped snapshot and freeze it before the 2026-11-17 results release.
- [ ] Preserve updates and corrections as new records; do not overwrite earlier claims.

## Verified event update

NVIDIA's official newsroom now confirms the CEO transition in a release dated 2026-11-12: Jensen Huang resigned as president, CEO, and board member effective immediately; Colette Kress was appointed interim CEO and CFO; and the board began searching for a permanent successor. Official source: https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition . The release also confirms that Q3 FY2027 results remain scheduled for 2026-11-17 at approximately 1:20 p.m. Pacific. This event must be treated as a confirmed, material governance event in the pilot dataset, while allegations and any alleged links to espionage or illicit chip shipments must remain separate claims with their own verification status.

## Limitations

- This is an initial source scan, not a complete seven-day archive.
- The search/retrieval process was retrospective; no live collection is claimed before 2026-11-12.
- Several articles may share wire copy or underlying sources; independent-source status has not been fully resolved.
- Exact article timestamps and current primary confirmation of the reported leadership change remain verification tasks.
- No financial advice or forecast is produced by this file.