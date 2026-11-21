"""Collect a local Medline snapshot, compare it, or render it without network."""

import argparse
from contextlib import closing
from datetime import datetime
import json
from pathlib import Path
import sqlite3
import sys

from .engine import assessment, connect, load, make_snapshot, reserve_sec, save
from .records import canonical, day, today_utc, utc
from .sources import SourceError, fetch_sec, manual_rows, sec_documents


def collect(db, args):
    cutoff = utc(args.cutoff)
    cutoff_date = datetime.fromisoformat(args.cutoff).date().isoformat()
    start = day(args.start)
    if start > cutoff_date or cutoff > today_utc():
        raise ValueError("The window must be ordered and cannot end in the future")
    if args.baseline:
        baseline = load(db, args.baseline)
        if baseline["cutoff"] > cutoff or baseline["start"] != start:
            raise ValueError("Baseline must share the start and precede the cutoff")
    coverage = {
        "sec": {"status": "disabled", "detail": "No EDGAR submissions import selected."},
        "documents_manual": {"status": "missing", "detail": "No document input supplied."},
        "market_manual": {"status": "missing", "detail": "No authorized market input supplied."},
    }
    records = []
    if args.input:
        records, channels = manual_rows(args.input, today_utc())
        for channel in channels:
            count = sum(row["channel"] == channel for row in records)
            coverage[channel] = {
                "status": "ok" if count else "missing", "detail": f"{count} manually supplied records."
            }
    if args.sec or args.sec_json:
        try:
            if args.sec:
                payload, retrieved_at = fetch_sec(lambda: reserve_sec(db))
                method = "live EDGAR API"
            else:
                payload = json.loads(args.sec_json.read_text(encoding="utf-8"))
                retrieved_at = utc(args.sec_retrieved_at)
                if retrieved_at > today_utc():
                    raise ValueError("SEC retrieval cannot occur in the future")
                method = "local EDGAR API export"
            rows, archive_overlap = sec_documents(payload, retrieved_at, start)
            records.extend(rows)
            detail = f"{len(rows)} supported filing records from {method} before applying the cutoff."
            if archive_overlap:
                detail += " Older EDGAR archive pages overlap the requested window."
            coverage["sec"] = {"status": "partial" if archive_overlap else "ok", "detail": detail}
        except SourceError as error:
            coverage["sec"] = {"status": "error", "detail": str(error)}
        except (OSError, ValueError, KeyError, TypeError):
            coverage["sec"] = {"status": "error", "detail": "EDGAR data could not be read or validated."}
    snapshot = make_snapshot(records, coverage, start, cutoff, cutoff_date, today_utc(), args.baseline)
    for channel in ("market_manual", "documents_manual"):
        if coverage[channel]["status"] == "ok" and not any(
            row["channel"] == channel for bucket in ("on_time", "retrospective") for row in snapshot[bucket]
        ):
            coverage[channel] = {"status": "missing", "detail": "No supplied observations in the window."}
    return save(db, snapshot)


def md_text(value):
    value = " ".join(str(value).split())
    for character in "\\`*_{}[]<>":
        value = value.replace(character, "\\" + character)
    return value


def markdown(report):
    manifest = report["manifest"]
    lines = [
        "# Medline research scanner",
        "",
        f'- Decision cutoff: {report["decision_timestamp"]}',
        f'- Snapshot: `{manifest["snapshot"]}`',
        f'- Baseline: `{manifest["baseline"] or "none"}`',
        f'- Outside-window records excluded: {manifest["excluded_outside_window"]}',
        f'- Coverage status: {manifest["coverage_status"]}',
        "",
        "## Source coverage",
        "",
    ]
    for channel, info in sorted(manifest["coverage"].items()):
        lines.append(f'- {md_text(channel)} · **{info["status"]}** · {md_text(info["detail"])}')
    for key, title in (("changes", "Point-in-time evidence"), ("retrospective_changes", "Retrospective observations")):
        lines.extend(["", f"## {title}", ""])
        if not report[key]:
            lines.append("No observations in this section.")
        for change in report[key]:
            lines.append(f'- **{change["status"]}** · {md_text(change["id"])}')
            rows = change["after"] or change["before"]
            for row in rows:
                claim = row.get("claim") or f'{row["session"]} · close {row["close"]} {row["currency"]} · volume {row["volume"]}'
                evidence_type = row.get("verification", "measurement")
                lines.append(f'  - {md_text(evidence_type)} · {md_text(claim)}')
                lines.append(f'    - Source: [{md_text(row["publisher"])}](<{row["url"]}>)')
                event = row["event_at"] or row["event_date"] or "unknown"
                published = row["published_at"] or row["published_date"] or "unknown"
                lines.append(f'    - Event/session: {event} · published: {published}')
                available = row["available_at"] or "unknown"
                lines.append(f'    - Available: {available} · retrieved: {row["retrieved_at"]}')
                if row.get("notes"):
                    lines.append(f'    - {md_text(row["notes"])}')
            if not change["after"]:
                lines.append("  - Prior evidence retained. Current absence may reflect coverage.")
            elif change["status"] == "partial_coverage":
                lines.append("  - Some prior references were absent from current coverage and are retained in the baseline.")
            elif change["classifications"]:
                lines.append(f'  - Research classification: {", ".join(change["classifications"])}')
    for key, title in (("market_conflicts", "Point-in-time market discrepancies"),
                       ("retrospective_market_conflicts", "Retrospective market discrepancies")):
        lines.extend(["", f"## {title}", ""])
        if not report[key]:
            lines.append("No comparable discrepancies observed in the supplied data.")
        for conflict in report[key]:
            values = ", ".join(f'{md_text(item["provider"])} {item["value"]}' for item in conflict["reported"])
            lines.append(f'- {conflict["session"]} · {conflict["field"]} · {values}')
    lines.extend(["", "## Market comparisons", ""])
    for key, label in (("market_metrics", "point-in-time"), ("retrospective_market_metrics", "retrospective")):
        for row in report[key]:
            price = row["close_change_pct"] if row["close_change_pct"] is not None else "unavailable"
            volume = row["volume_ratio_20_observed"] if row["volume_ratio_20_observed"] is not None else "unavailable"
            anomaly = row["anomaly"] if row["anomaly"] is not None else "undetermined"
            lines.append(f'- {label} · {row["session"]} · {md_text(row["provider"])} · '
                         f'close change (%) {price} · volume ratio {volume} · anomaly {anomaly}')
    lines.extend(["", "## Uncertainty", ""] + [f"- {item}" for item in report["risks_and_limits"]])
    return "\n".join(lines) + "\n"


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True, help="Local SQLite file")
    commands = parser.add_subparsers(dest="command", required=True)
    collect_parser = commands.add_parser("collect")
    collect_parser.add_argument("--start", required=True)
    collect_parser.add_argument("--cutoff", required=True)
    collect_parser.add_argument("--baseline")
    collect_parser.add_argument("--input", type=Path)
    collection = collect_parser.add_mutually_exclusive_group()
    collection.add_argument("--sec", action="store_true")
    collection.add_argument("--sec-json", type=Path)
    collect_parser.add_argument("--sec-retrieved-at")
    for command in ("compare", "report"):
        display = commands.add_parser(command)
        display.add_argument("--snapshot", required=True)
        display.add_argument("--baseline")
        if command == "report":
            display.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    if args.command == "collect" and bool(args.sec_json) != bool(args.sec_retrieved_at):
        parser.error("--sec-json and --sec-retrieved-at must be used together")
    return args


def main():
    args = arguments()
    try:
        if args.command == "collect":
            args.db.parent.mkdir(parents=True, exist_ok=True)
            with closing(connect(args.db)) as db:
                print(collect(db, args))
        else:
            uri = args.db.resolve().as_uri() + "?mode=ro"
            with closing(sqlite3.connect(uri, uri=True)) as db:
                result = assessment(db, args.snapshot, args.baseline)
            matches = args.command == "compare" or args.format == "json"
            output = canonical(result) + "\n" if matches else markdown(result)
            sys.stdout.buffer.write(output.encode("utf-8"))
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as error:
        print(f"Scanner error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
