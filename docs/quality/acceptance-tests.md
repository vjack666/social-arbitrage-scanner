# Acceptance Tests v0.1

**Status:** Proposed specification tests. They are not automated and have not been run. Runtime implementation must wait for owner approval.

## A. Shared contract tests

| ID | Test | Pass condition |
|---|---|---|
| AC-001 | Required fields | Every agent output contains all required shared fields or explicitly reports why an optional collection is empty. |
| AC-002 | Evidence provenance | Every factual or reported claim links to source IDs; broken or missing references are flagged. |
| AC-003 | Fact/inference separation | Verified facts, reported claims, measurements, inferences, and hypotheses are distinguishable. |
| AC-004 | Timestamp integrity | Event, publication, retrieval, and decision timestamps are distinct when known; unknown values are not invented. |
| AC-005 | Unverified claim handling | Uncorroborated claims remain labeled unverified and cannot be promoted to confirmed facts by repetition alone. |
| AC-006 | Confidence rationale | Every confidence label includes a rationale; numeric probability is forbidden unless the calibration method is documented. |
| AC-007 | Uncertainty path | Missing, weak, or contradictory evidence can produce `insufficient_evidence`. |
| AC-008 | Invalidation | Every non-empty hypothesis includes conditions that would weaken or invalidate it. |
| AC-009 | Disagreement preservation | Coordinator output retains material agent disagreements and identifies shared sources. |
| AC-010 | Auditability | Each result records contract version, agent/model version where applicable, and dataset/source references. |

## B. Agent-specific tests

### Discovery
- AC-D01: A topic spike is compared with a stated baseline and time window.
- AC-D02: Entity linkage is labeled uncertain when evidence does not support a direct relationship.
- AC-D03: Virality alone does not trigger a trading recommendation.

### Quantitative Sentiment
- AC-S01: Duplicate/reposted content handling is documented.
- AC-S02: Metrics report sample size, window, language/source coverage, and known model limitations.
- AC-S03: Sentiment performance is compared with a simple baseline before predictive claims are accepted.

### News and Event Intelligence
- AC-N01: Material claims include primary-source checks where feasible.
- AC-N02: Publication time and event time are not conflated.
- AC-N03: Corrections, retractions, and conflicting reports remain visible in the audit trail.

### Crowd Psychology and Positioning
- AC-C01: Behavioral interpretations cite observable indicators.
- AC-C02: Short-squeeze hypotheses require reliable positioning/borrow/liquidity evidence; otherwise output says the evidence is missing.
- AC-C03: At least one plausible counter-scenario is recorded.

### Quantitative Validation
- AC-V01: Historical features obey the point-in-time cutoff.
- AC-V02: Train/validation/test or walk-forward splits are chronological and documented.
- AC-V03: The final holdout is not reused for model tuning.
- AC-V04: Baselines, transaction costs where relevant, sample size, uncertainty, and negative results are reported.
- AC-V05: Reproduction instructions identify data versions and configuration.

## C. Coordinator tests

- AC-CO01: The coordinator does not blindly average agent confidence scores.
- AC-CO02: Multiple agents citing the same underlying article are not counted as independent confirmations.
- AC-CO03: Contradictions and missing data are visible in the final assessment.
- AC-CO04: The coordinator does not convert a research assessment into an order or claim that a trade is guaranteed to profit.

## D. NVIDIA case-study test plan

This is a plan, not a claim that data has already been collected.

1. Select one historical decision timestamp before examining the outcome.
2. Freeze a list of source records that were available by that timestamp.
3. Record event, publication, and retrieval timestamps separately.
4. Run the conceptual output contract for each relevant agent; mark unavailable inputs explicitly.
5. Store the coordinator's original conclusion before observing the evaluation horizon's outcome.
6. After the horizon passes, score the forecast using a predeclared target and compare it with simple baselines.
7. Report missing data, source dependence, uncertainty, and any protocol deviations.

## E. Release gates

Do not begin implementation until:
1. The owner approves the shared data contract.
2. The owner approves these acceptance tests and clarifies any disputed definitions.
3. Data sources, licenses, retention, cost, and rate limits are reviewed.
4. The initial NVIDIA question, decision timestamp, horizon, and outcome metric are defined.
5. A design review confirms that the system can run in research-only mode with no order execution.

## F. Current status

All items above are proposed. They have not been executed as automated tests, and no empirical performance is claimed.
