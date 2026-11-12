# Shared Data Contract v0.1

**Status:** Draft for owner review. This is a conceptual contract, not an implemented or validated runtime schema. No production data has been populated.

## 1. Purpose

Provide a common, auditable envelope so the five research agents and coordinator can exchange observations without confusing facts, interpretations, hypotheses, or recommendations.

## 2. Required record fields

Every agent result must contain the following logical fields:

| Field | Required | Meaning |
|---|---:|---|
| `contract_version` | Yes | Version of this contract, initially `0.1`. |
| `case_id` | Yes | Stable identifier for the research case. |
| `agent_id` | Yes | Producer agent identifier. |
| `created_at` | Yes | UTC timestamp when the record was generated. |
| `decision_timestamp` | Yes | Point in time the assessment claims to represent. |
| `asset_or_entity` | Yes | Entity under analysis; use a stable identifier when available. |
| `horizon` | Yes | Explicit evaluation horizon or `unspecified`. |
| `sources` | Yes | Source records supporting the observations. Empty only when no source is available, which must be explained. |
| `evidence` | Yes | Observations, each labeled and linked to sources. May be empty only with an explicit reason. |
| `inferences` | Yes | Interpretations derived from evidence; may be empty. |
| `hypotheses` | Yes | Testable claims and alternatives; may be empty. |
| `direction` | Yes | `bullish`, `bearish`, `neutral`, or `insufficient_evidence`. |
| `confidence` | Yes | Calibrated numeric score only if a defined method exists; otherwise qualitative level plus rationale. |
| `risks_and_limits` | Yes | Data gaps, assumptions, bias risks, and alternative explanations. |
| `invalidation_conditions` | Yes | Observations that would weaken or invalidate the hypothesis. |
| `validation_status` | Yes | `not_tested`, `in_progress`, `passed`, `failed`, or `inconclusive`. |
| `recommendation` | Conditional | Research follow-up only by default. Any trading-related recommendation is out of scope until separately approved and validated. |

## 3. Source object

Each source should include:
- `source_id`: stable ID within the case.
- `publisher` and `source_type`: e.g. company filing, official release, news outlet, public social post, market-data provider.
- `url_or_reference`: direct URL or a permitted stable reference.
- `published_at`: publication timestamp, if known.
- `event_at`: time the underlying event occurred, if known.
- `retrieved_at`: collection timestamp.
- `content_fingerprint`: optional hash or duplicate-detection key where lawful and practical.
- `verification_state`: `primary_source`, `corroborated`, `unverified`, `disputed`, or `retracted`.
- `access_and_license_note`: relevant access, retention, or license constraints.

Never invent a missing timestamp. Use null/unknown and state the limitation.

## 4. Evidence object

Each evidence item should include:
- `evidence_id`
- `claim`: concise, falsifiable statement of what was observed.
- `classification`: `verified_fact`, `reported_claim`, or `measurement`.
- `source_ids`: one or more source IDs.
- `observed_at` and applicable measurement window.
- `method`: how the observation was extracted or calculated.
- `limitations`: uncertainty, sampling gaps, or quality warnings.

A source can support a reported claim without proving that claim true. A measurement is not automatically causal evidence.

## 5. Inference and hypothesis objects

An inference should include its supporting evidence IDs, reasoning summary, assumptions, and alternative explanations.

A hypothesis should include:
- `hypothesis_id`
- testable statement
- expected direction, if any
- horizon and outcome definition
- evidence and inference IDs used
- confidence rationale
- invalidation conditions
- proposed test or observation needed to resolve uncertainty

Do not encode a narrative as a fact. Do not treat agreement between agents as independent corroboration if they rely on the same underlying source.

## 6. Confidence policy

- Do not invent precise probabilities before calibration is defined and evaluated.
- Qualitative labels must include a short rationale and evidence-quality note.
- Confidence in source verification is distinct from confidence in predictive value.
- Confidence is not a probability of profit unless a valid calibration study demonstrates that interpretation.

## 7. Time and point-in-time integrity

- Store timestamps in UTC using ISO 8601; preserve original source timezone when available.
- Keep publication time, event time, retrieval time, and decision timestamp distinct.
- A historical assessment may use only information available by its decision timestamp.
- Later corrections must be recorded as new versions/events; do not silently rewrite earlier records.
- Missing or ambiguous timestamps must be visible in the result.

## 8. Disagreement and insufficient evidence

Agents must be allowed to disagree. The coordinator preserves each agent's original assessment, identifies shared versus independent evidence, and explains any weighting. Use `insufficient_evidence` when material inputs are absent, unreliable, or contradictory.

## 9. NVIDIA case-study policy

NVIDIA is a test subject, not a preselected bullish or bearish thesis. Before populating this contract with a historical case, select a decision timestamp and reconstruct source availability at that time. Do not include future prices, later headlines, later corrections, or outcomes in the evidence used to create the original assessment. Any example without verified data must be explicitly marked `illustrative_only`.

## 10. Change control

Changes to required fields, enumerations, timestamp semantics, or confidence interpretation require a contract-version increment, a migration note, and updated acceptance tests. Implementation is blocked until the owner approves this contract.
