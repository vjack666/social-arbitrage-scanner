"""Immutable SQLite snapshots and deterministic evidence comparisons."""

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
import json
import sqlite3
from statistics import median
import time

from .records import CONTRACT, ENTITY, VERSION, canonical, digest, version_fields


def connect(path):
    db = sqlite3.connect(path, timeout=15)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS snapshots (id TEXT PRIMARY KEY, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS throttle (source TEXT PRIMARY KEY, last_request REAL NOT NULL);
    """)
    return db


def reserve_sec(db):
    # Serialize reservations across invocations sharing this database.
    db.execute("BEGIN IMMEDIATE")
    try:
        previous = db.execute("SELECT last_request FROM throttle WHERE source='sec'").fetchone()
        if previous:
            time.sleep(max(0, min(1, 1 - (time.time() - previous[0]))))
        db.execute("INSERT OR REPLACE INTO throttle VALUES ('sec', ?)", (time.time(),))
        db.commit()
    except BaseException:
        db.rollback()
        raise


def make_snapshot(rows, coverage, start, cutoff, cutoff_date, collected_at, baseline=None):
    sections = {"on_time": {}, "retrospective": {}}
    outside = set()
    for row in rows:
        key = digest(version_fields(row))
        local_date = row.get("session") or row["published_date"]
        # A document without a filing date may still have a verified timestamp.
        if not local_date and row["published_at"]:
            local_date = row["published_at"][:10]
        deadline = row["available_at"]
        if (local_date and (local_date < start or (not deadline and local_date > cutoff_date))) or (
            row["event_at"] and row["event_at"] > cutoff
        ) or (
            row["event_date"] and row["event_date"] > cutoff_date
        ) or (deadline and deadline > cutoff):
            outside.add(key)
            continue
        observed_by_cutoff = (deadline or row["retrieved_at"]) <= cutoff
        bucket = "on_time" if observed_by_cutoff else "retrospective"
        saved = sections[bucket].get(key)
        if saved is None or row["retrieved_at"] < saved["retrieved_at"]:
            sections[bucket][key] = row
    payload = {
        "scanner_version": VERSION, "contract_version": CONTRACT, "entity": ENTITY,
        "start": start, "cutoff": cutoff, "cutoff_date": cutoff_date, "collected_at": collected_at,
        "baseline": baseline, "coverage": coverage, "excluded_outside_window": len(outside),
        **{bucket: [records[key] for key in sorted(records)] for bucket, records in sections.items()},
    }
    return payload


def save(db, snapshot):
    # Identical input and cutoff can be retried; retain the first captured retrieval metadata.
    stable = {key: value for key, value in snapshot.items() if key != "collected_at"}
    for bucket in ("on_time", "retrospective"):
        stable[bucket] = [version_fields(row) for row in snapshot[bucket]]
    snapshot_id = digest(stable)
    with db:
        db.execute("INSERT OR IGNORE INTO snapshots VALUES (?, ?)", (snapshot_id, canonical(snapshot)))
    return snapshot_id


def load(db, snapshot_id):
    record = db.execute("SELECT payload FROM snapshots WHERE id=?", (snapshot_id,)).fetchone()
    if record is None:
        raise ValueError(f"Unknown snapshot: {snapshot_id}")
    return json.loads(record[0])


def group(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["kind"], row["id"])].append(row)
    return groups


def variants(rows):
    return {digest(version_fields(row)) for row in rows}


def materiality(row):
    if row["kind"] == "bar":
        return "market_measurement"
    if row["verification"] == "retracted":
        return "retracted"
    if row["impact"] and row["verification"] == "primary_source":
        return "high"
    if row["verification"] in {"unverified", "disputed"} or row["impact"]:
        return "needs_review"
    return "review"


def differences(previous, current):
    old = group(previous)
    new = group(current)
    changes = []
    for (kind, identifier) in sorted(old.keys() | new.keys()):
        before = old.get((kind, identifier), [])
        after = new.get((kind, identifier), [])
        earlier = variants(before)
        latest = variants(after)
        if not before:
            status = "new"
        elif not after:
            status = "not_observed"
        elif earlier == latest:
            status = "unchanged"
        elif earlier < latest:
            status = "updated"
        elif latest < earlier:
            status = "partial_coverage"
        elif kind == "bar" or any(row["verification"] == "retracted" for row in after):
            status = "corrected"
        else:
            old_sources = {(row["origin"], row["url"]) for row in before}
            new_sources = {(row["origin"], row["url"]) for row in after}
            status = "corrected" if old_sources & new_sources else "updated"
        changes.append({
            "kind": kind, "id": identifier, "status": status,
            "has_uncertainty": status in {"not_observed", "partial_coverage"} or any(
                row.get("verification") in {"disputed", "unverified", "retracted"} for row in after
            ),
            "independent_origins": sorted({row["origin"] for row in after}),
            "classifications": sorted({materiality(row) for row in after}),
            "before": before, "after": after,
        })
    return changes


def disagreements(rows):
    groups = defaultdict(list)
    for row in rows:
        if row["kind"] == "bar":
            groups[(row["session"], row["currency"], row["adjustment"])].append(row)
    results = []
    for (session, currency, adjustment), bars in sorted(groups.items()):
        if adjustment == "unknown":
            continue
        for field in ("close", "volume"):
            known = [row for row in bars if row[field] is not None]
            if len({row[field] for row in known}) > 1:
                results.append({
                    "session": session, "currency": currency, "adjustment": adjustment, "field": field,
                    "reported": [{"provider": r["provider"], "value": r[field], "url": r["url"]} for r in known],
                })
    return results


def market_metrics(rows):
    by_series = defaultdict(list)
    for row in rows:
        if row["kind"] == "bar":
            by_series[(row["provider"], row["currency"], row["adjustment"])].append(row)
    results = []
    for (provider, currency, adjustment), bars in sorted(by_series.items()):
        by_date = defaultdict(list)
        for row in bars:
            by_date[row["session"]].append(row)
        sessions = sorted(by_date)
        for index, session in enumerate(sessions):
            current = by_date[session]
            if len(current) != 1 or adjustment == "unknown":
                continue
            bar = current[0]
            prior = by_date[sessions[index - 1]] if index else []
            close_change = None
            if len(prior) == 1 and bar["close"] and prior[0]["close"]:
                close_change = (Decimal(bar["close"]) / Decimal(prior[0]["close"]) - 1) * 100
            past = [by_date[key] for key in sessions[max(0, index - 20):index]]
            volume_ratio = None
            if bar["volume"] is not None and len(past) == 20 and all(
                len(day) == 1 and day[0]["volume"] is not None for day in past
            ):
                baseline = median(Decimal(day[0]["volume"]) for day in past)
                if baseline:
                    volume_ratio = Decimal(bar["volume"]) / baseline
            close_anomaly = None if close_change is None else abs(close_change) >= 5
            volume_anomaly = None if volume_ratio is None else volume_ratio >= 2
            flags = (close_anomaly, volume_anomaly)
            results.append({
                "provider": provider, "currency": currency, "adjustment": adjustment, "session": session,
                "close_change_pct": rounded(close_change), "volume_ratio_20_observed": rounded(volume_ratio),
                "anomaly": True if True in flags else (None if None in flags else False),
            })
    return results


def rounded(value):
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)) if value is not None else None


def assessment(db, snapshot_id, baseline=None):
    current = load(db, snapshot_id)
    baseline = baseline or current["baseline"]
    previous = load(db, baseline) if baseline else None
    if previous and (previous["cutoff"] > current["cutoff"] or previous["start"] != current["start"]):
        raise ValueError("Baseline must have the same start and a cutoff no later than the current snapshot")
    on_time = current["on_time"]
    annex = current["retrospective"]
    source_records = {}
    evidence = []
    for row in on_time:
        source_id = digest(version_fields(row))
        source_records[source_id] = {
            "source_id": source_id, "publisher": row["publisher"], "source_type": row.get("source_type", "market_data"),
            "url_or_reference": row["url"], "published_at": row["published_at"], "event_at": row["event_at"],
            "published_date": row["published_date"], "event_date": row["event_date"],
            "available_at": row["available_at"],
            "retrieved_at": row["retrieved_at"], "verification_state": row.get("verification", "unverified"),
            "access_and_license_note": row["license"], "content_fingerprint": source_id,
        }
        claim = row.get("claim") or f"{ENTITY['ticker']} {row['session']}: close {row['close']}, volume {row['volume']}."
        classification = "measurement" if row["kind"] == "bar" else (
            "verified_fact" if row["verification"] == "primary_source" else "reported_claim"
        )
        evidence.append({
            "evidence_id": source_id, "claim": claim, "classification": classification,
            "source_ids": [source_id], "observed_at": row["event_at"], "method": row["channel"],
            "limitations": [row["notes"]] if row.get("notes") else [],
        })
    unavailable = [key for key, info in current["coverage"].items() if info["status"] != "ok"]
    return {
        "contract_version": CONTRACT, "scanner_version": VERSION, "case_id": f"MDLN:{snapshot_id}",
        "agent_id": "medline-local-scanner", "created_at": current["collected_at"],
        "decision_timestamp": current["cutoff"], "asset_or_entity": ENTITY, "horizon": "unspecified",
        "sources": list(source_records.values()), "evidence": evidence, "inferences": [], "hypotheses": [],
        "direction": "insufficient_evidence", "validation_status": "not_tested", "invalidation_conditions": [],
        "confidence": {"level": "undetermined", "rationale": "Document and bar classifications are descriptive."},
        "risks_and_limits": [
            "Retrospective records have no verified availability by the cutoff and are excluded from point-in-time evidence.",
            "Market comparisons use observed bars. Missing sessions can widen the interval or limit the volume baseline.",
            "Research coverage depends on the source register and manually supplied inputs.",
        ] + (["No records have verified availability by the cutoff."] if not evidence else [])
          + [f"Coverage gap: {channel}." for channel in unavailable],
        "manifest": {
            "snapshot": snapshot_id, "snapshot_payload_sha256": digest(current),
            "baseline": baseline, "baseline_payload_sha256": digest(previous) if previous else None,
            "coverage_status": "partial" if unavailable else "complete_for_configured_sources",
            "start": current["start"], "coverage": current["coverage"],
            "baseline_coverage": previous["coverage"] if previous else None,
            "excluded_outside_window": current["excluded_outside_window"],
        },
        "changes": differences(previous["on_time"] if previous else [], on_time),
        "retrospective_changes": differences(previous["retrospective"] if previous else [], annex),
        "market_conflicts": disagreements(on_time),
        "retrospective_market_conflicts": disagreements(on_time + annex),
        "market_metrics": market_metrics(on_time),
        "retrospective_market_metrics": market_metrics(on_time + annex),
    }
