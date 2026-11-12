# NVIDIA Pilot — Evidence Register

**Status:** Empty template. A row must not be marked collected or verified until an actual source record has been retrieved and checked. Do not use this file as evidence that data collection has already occurred.

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

## Empty log

No source records have been entered yet.

| record_id | source_type | publisher | title_or_claim | canonical_url | published_at | event_at | retrieved_at | decision_timestamp | verification_status | duplicate_group | eligible_for_snapshot | claim_class | notes_and_limitations | dataset_or_parser_version |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Review checklist

- [ ] Original source opened and URL checked.
- [ ] Publication time recorded from the source, not inferred from search ranking.
- [ ] Timezone converted only after preserving the original timestamp.
- [ ] Event time kept separate from publication time.
- [ ] Item was available before the applicable decision timestamp.
- [ ] Syndicated duplicates grouped and not counted as independent evidence.
- [ ] Material company claims corroborated against primary sources where feasible.
- [ ] Access and license terms reviewed before storage or reuse.
- [ ] Excluded records retain a reason rather than being silently deleted.

## Important

A page found today with a historical publication date can be used in a retrospective reconstruction only if the publication timestamp and historical availability can be substantiated. It must be labeled as retrieved retrospectively, not as collected live at the time.