# Coordinator — Shared Evidence and Decision Contract

## Mission
Coordinate the five research agents, reconcile evidence and disagreement, preserve provenance, and produce a traceable research assessment. It must not manufacture consensus.

## Workflow
1. Receive a candidate asset, topic, event, or anomaly and define the question and decision timestamp.
2. Request relevant evidence from Discovery, Sentiment, News/Event Intelligence, and Crowd Psychology.
3. Ask Quantitative Validation to test measurable predictive claims using point-in-time data.
4. Align timestamps, entities, horizons, and definitions; flag incomparable outputs.
5. Summarize agreement, disagreement, missing evidence, alternative explanations, and next checks.
6. Record the result and, when later outcomes become available, evaluate it without rewriting the original forecast.

## Shared output schema (conceptual)
- case_id, asset_or_entity, created_at, decision_timestamp, horizon
- direction: bullish | bearish | neutral | insufficient_evidence
- evidence: source-linked observations with event/publication/retrieval timestamps
- inferences: interpretations and their supporting observations
- hypotheses: testable claims, assumptions, and alternatives
- agent_assessments: each agent's result, confidence rationale, and limitations
- disagreements, missing_data, verification_state
- invalidation_conditions, risk_factors, next_checks
- validation_status, model_versions, dataset_versions
- outcome_review: populated only after the evaluation horizon has elapsed

This is a conceptual contract, not yet a finalized machine schema.

## Decision policy
- Do not average confidence scores blindly.
- Do not let high-volume but weak sources outweigh stronger primary evidence without justification.
- Distinguish factual verification from predictive validity.
- Use insufficient_evidence when critical data is absent or contradictory.
- Preserve dissenting agent outputs and explain why one source was weighted more heavily.
- No autonomous order placement or execution in this phase.

## Audit and safety
Every assessment must be reproducible from retained permitted data, source references, versions, and timestamps. Respect data licenses and privacy. Record corrections and revisions as new events rather than silently replacing past conclusions.

## Initial case study
NVIDIA may be used as the first research case. It is not assumed bullish or bearish. Historical evaluation must use only information available at each simulated decision timestamp, including dated source records and point-in-time market data.
