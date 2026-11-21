import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError

from scanner.engine import differences, disagreements, make_snapshot, market_metrics
from scanner.records import bar, document, utc
from scanner.sources import SEC_URL, SourceError, fetch_sec, sec_documents


RETRIEVED = "2026-11-21T00:00:00-05:00"
CUTOFF = "2026-11-20T16:05:00-05:00"
START = "2026-11-16"
ACCESSION = "0001193125-26-467193"
SEC_LINK = "https://www.sec.gov/Archives/edgar/data/2046386/000119312526467193/mdln-20261116.htm"
FDA_LINK = "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfRes/res.cfm?id=223519"
EDGAR_EXCERPT = {
    # Manual transcription of verified filing metadata, in the documented API shape.
    "cik": "0002046386",
    "filings": {"files": [], "recent": {
        "accessionNumber": [ACCESSION], "form": ["8-K"], "primaryDocument": ["mdln-20261116.htm"],
        "filingDate": ["2026-11-18"], "reportDate": ["2026-11-16"],
        "acceptanceDateTime": ["2026-11-18T21:34:17Z"],
    }},
}
AGREEMENT = {
    "id": f"sec:{ACCESSION}", "publisher": "SEC EDGAR", "url": SEC_LINK,
    "published_at": "2026-11-18T16:34:17-05:00", "event_date": "2026-11-16",
    "license": "Public SEC filing summary.", "category": "capital", "verification": "primary_source",
    "source_type": "filing", "claim": "The agreement provides for a conditional USD 200 million repurchase.",
    "impact": "binding_terms",
}
RECALL = {
    "id": "fda:100182", "publisher": "FDA", "url": FDA_LINK,
    "published_date": "2026-11-20", "event_date": "2026-10-08",
    "license": "Public FDA record summary.", "category": "regulatory", "verification": "primary_source",
    "source_type": "regulator", "claim": "FDA posted a class II recall record for Medline procedure kits.",
}
FRIDAY_BAR = {
    "session": "2026-11-20", "event_at": "2026-11-20T16:00:00-05:00",
    "provider": "Stock Analysis", "publisher": "Stock Analysis", "currency": "USD", "adjustment": "as_traded",
    "url": "https://stockanalysis.com/stocks/mdln/history/", "license": "Limited research citation.",
    "close": "37.04", "volume": 9330912,
}
THURSDAY_BAR = {
    **FRIDAY_BAR, "session": "2026-11-19", "event_at": "2026-11-19T16:00:00-05:00",
    "close": "37.84", "volume": 10343961,
}


class ScannerTests(unittest.TestCase):
    def test_sec_parser_preserves_accession_and_time(self):
        rows, overlap = sec_documents(EDGAR_EXCERPT, RETRIEVED, START)
        self.assertFalse(overlap)
        self.assertEqual(rows[0]["id"], AGREEMENT["id"])
        self.assertEqual(rows[0]["url"], SEC_LINK)
        self.assertEqual(rows[0]["published_at"], "2026-11-18T21:34:17.000000Z")
        self.assertEqual(rows[0]["event_date"], "2026-11-16")

    def test_sec_parser_rejects_wrong_company_and_truncated_columns(self):
        wrong_company = {**EDGAR_EXCERPT, "cik": "0001045810"}
        with self.assertRaisesRegex(ValueError, "does not belong"):
            sec_documents(wrong_company, RETRIEVED, START)
        bad = json.loads(json.dumps(EDGAR_EXCERPT))
        bad["filings"]["recent"]["form"] = []
        with self.assertRaises(ValueError):
            sec_documents(bad, RETRIEVED, START)

    def test_sec_does_not_make_unidentified_request(self):
        with patch.dict(os.environ, {"SEC_USER_AGENT": ""}):
            with self.assertRaisesRegex(SourceError, "genuine contact"):
                fetch_sec(lambda: self.fail("No request should be reserved"))

    def test_sec_access_rejection_is_not_retried(self):
        opener = Mock()
        opener.open.side_effect = HTTPError(SEC_URL, 403, "Forbidden", None, None)
        reserve = Mock()
        with patch.dict(os.environ, {"SEC_USER_AGENT": "Local test scanner example@example.invalid"}):
            with self.assertRaisesRegex(SourceError, "SEC HTTP 403"):
                fetch_sec(reserve, opener=opener)
        reserve.assert_called_once_with()
        opener.open.assert_called_once()
        self.assertEqual(opener.open.call_args.args[0].full_url, SEC_URL)

    def test_cutoff_excludes_future_events_and_keeps_date_only_in_annex(self):
        precise = document(AGREEMENT, RETRIEVED, "documents_manual")
        uncertain = document(RECALL, RETRIEVED, "documents_manual")
        friday = bar(FRIDAY_BAR, RETRIEVED)
        baseline = make_snapshot(
            [precise, uncertain, friday], {}, START, utc("2026-11-19T16:05:00-05:00"),
            "2026-11-19", utc(RETRIEVED),
        )
        current = make_snapshot([precise, uncertain, friday], {}, START, utc(CUTOFF), "2026-11-20", utc(RETRIEVED))
        self.assertEqual(baseline["excluded_outside_window"], 2)
        self.assertEqual(current["on_time"], [precise])
        self.assertEqual({row["kind"] for row in current["retrospective"]}, {"document", "bar"})
        self.assertIsNone(uncertain["published_at"])

    def test_exact_duplicates_collapse_and_references_share_origin(self):
        sec = document(AGREEMENT, RETRIEVED, "documents_manual")
        mirror = document({
            **AGREEMENT, "publisher": "Medline IR",
            "url": "https://medline.gcs-web.com/static-files/1b27c671-3a60-45fe-a899-2bbf8f0dfeea",
        }, RETRIEVED, "documents_manual")
        snapshot = make_snapshot([mirror, sec, sec], {}, START, utc(CUTOFF), "2026-11-20", utc(RETRIEVED))
        self.assertEqual(len(snapshot["on_time"]), 2)
        [change] = differences([sec], snapshot["on_time"])
        self.assertEqual(change["status"], "updated")
        self.assertEqual(change["independent_origins"], [sec["id"]])
        self.assertEqual(change["classifications"], ["high"])

    def test_baseline_history_and_uncertainty_are_preserved(self):
        primary = document(AGREEMENT, RETRIEVED, "documents_manual")
        review = document({
            **AGREEMENT, "verification": "disputed", "notes": "Test the review path.",
        }, RETRIEVED, "documents_manual")
        [changed] = differences([primary], [review])
        self.assertEqual(changed["status"], "corrected")
        self.assertEqual(changed["classifications"], ["needs_review"])
        self.assertTrue(changed["has_uncertainty"])
        self.assertEqual(changed["before"], [primary])
        self.assertEqual(differences([primary, review], [primary])[0]["status"], "partial_coverage")
        self.assertEqual(differences([primary], [])[0]["status"], "not_observed")

    def test_real_provider_variance_and_market_comparison(self):
        prices = [
            bar(THURSDAY_BAR, RETRIEVED), bar(FRIDAY_BAR, RETRIEVED), bar({
                **FRIDAY_BAR, "provider": "Stocknear", "publisher": "Stocknear",
                "url": "https://www.stocknear.com/stocks/MDLN/history", "volume": 9285793,
            }, RETRIEVED),
        ]
        [conflict] = disagreements(prices)
        self.assertEqual(conflict["field"], "volume")
        self.assertEqual({item["value"] for item in conflict["reported"]}, {9285793, 9330912})
        result = market_metrics(prices)
        friday = next(row for row in result if row["session"] == "2026-11-20" and row["provider"] == "Stock Analysis")
        self.assertEqual(friday["close_change_pct"], "-2.11")
        self.assertIsNone(friday["volume_ratio_20_observed"])
        self.assertIsNone(friday["anomaly"])

    def test_rejects_inconsistent_bar_and_naive_timestamp(self):
        with self.assertRaisesRegex(ValueError, "daily low"):
            bar({**FRIDAY_BAR, "low": "37.65"}, RETRIEVED)
        with self.assertRaisesRegex(ValueError, "explicit UTC offset"):
            utc("2026-11-18T16:34:17")

    def test_fractional_cutoff_has_correct_order(self):
        self.assertLess(utc("2026-11-20T21:00:01Z"), utc("2026-11-20T21:00:01.001Z"))

    def test_historical_sec_fragment_never_claims_archive_coverage(self):
        filings = {**EDGAR_EXCERPT["filings"], "files": [{"filingTo": "2026-11-17"}]}
        _, overlap = sec_documents({**EDGAR_EXCERPT, "filings": filings}, RETRIEVED, START)
        self.assertTrue(overlap)

    def test_cli_idempotence_provenance_and_offline_report(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            local = root / "medline.json"
            local.write_text(json.dumps({"documents": [AGREEMENT, RECALL], "prices": [THURSDAY_BAR, FRIDAY_BAR]}))
            database = root / "history.sqlite3"
            command = [sys.executable, "-m", "scanner", "--db", str(database)]
            data = ["--start", START, "--input", str(local)]
            baseline = subprocess.check_output(command + ["collect", *data, "--cutoff", "2026-11-19T16:05:00-05:00"]).decode().strip()
            run = command + ["collect", *data, "--cutoff", CUTOFF, "--baseline", baseline]
            snapshot = subprocess.check_output(run).decode().strip()
            self.assertEqual(snapshot, subprocess.check_output(run).decode().strip())
            compare = command + ["compare", "--snapshot", snapshot]
            raw = subprocess.check_output(compare)
            report = json.loads(raw)
            self.assertEqual(raw, subprocess.check_output(compare))
            self.assertEqual(report["manifest"]["baseline"], baseline)
            self.assertEqual(report["changes"][0]["status"], "unchanged")
            self.assertEqual(len(report["evidence"]), 1)
            self.assertEqual(report["evidence"][0]["source_ids"], [report["sources"][0]["source_id"]])
            md = command + ["report", "--snapshot", snapshot]
            markdown = subprocess.check_output(md)
            self.assertEqual(markdown, subprocess.check_output(md))
            self.assertIn(b"Retrospective observations", markdown)
            self.assertIn(b"-2.11", markdown)

    def test_cli_source_failure_is_reported_without_filling_gaps(self):
        with TemporaryDirectory() as directory:
            command = [sys.executable, "-m", "scanner", "--db", str(Path(directory) / "partial.sqlite3")]
            with patch.dict(os.environ, {"SEC_USER_AGENT": ""}):
                snapshot = subprocess.check_output(command + ["collect", "--cutoff", CUTOFF, "--start", START, "--sec"])
            report = json.loads(subprocess.check_output(command + ["compare", "--snapshot", snapshot.decode().strip()]))
        self.assertEqual(report["manifest"]["coverage"]["sec"]["status"], "error")
        self.assertEqual(report["manifest"]["coverage"]["market_manual"]["status"], "missing")
        self.assertEqual(report["manifest"]["coverage_status"], "partial")
        self.assertEqual(report["evidence"], [])
        self.assertEqual(report["direction"], "insufficient_evidence")
