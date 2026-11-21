"""Structured SEC metadata and manually sourced documents and market data."""

from datetime import date
import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .records import ENTITY, bar, day, document, today_utc

SEC_URL = f"https://data.sec.gov/submissions/CIK{ENTITY['cik']}.json"
FAIR_ACCESS = "https://www.sec.gov/about/developer-resources#fair-access"
SEC_CATEGORIES = {
    "8-K": "other", "10-K": "earnings", "10-Q": "earnings", "424B3": "capital", "424B4": "capital",
    "424B5": "capital", "S-1": "capital", "S-3": "capital", "FWP": "capital", "SC 13D": "capital",
    "SC 13G": "capital", "SCHEDULE 13D": "capital", "SCHEDULE 13G": "capital",
}


class SourceError(Exception):
    """A safe message suitable for a local report."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_sec(reserve_request, opener=None):
    identity = os.environ.get("SEC_USER_AGENT", "").strip()
    if not re.fullmatch(r"[ -~]+ [^\s@]+@[^\s@]+\.[^\s@]+", identity):
        raise SourceError("Configure SEC_USER_AGENT with an organization or name and a genuine contact email.")
    request = Request(SEC_URL, headers={"User-Agent": identity, "Accept": "application/json"})
    reserve_request()
    client = opener or build_opener(NoRedirect())
    try:
        with client.open(request, timeout=15) as response:
            if response.headers.get_content_type() != "application/json":
                raise SourceError("SEC did not return JSON.")
            raw = response.read(4 * 1024 * 1024 + 1)
            if len(raw) > 4 * 1024 * 1024:
                raise SourceError("SEC response exceeds the size limit.")
            return json.loads(raw), today_utc()
    except HTTPError as error:
        raise SourceError(f"SEC HTTP {error.code}. Collection stopped for this source.") from error
    except (URLError, TimeoutError, ValueError) as error:
        raise SourceError("SEC request failed or returned invalid JSON.") from error


def sec_documents(payload, retrieved_at, start):
    if str(payload["cik"]).zfill(10) != ENTITY["cik"]:
        raise ValueError("SEC file does not belong to Medline")
    filings = payload["filings"]
    recent = filings["recent"]
    keys = ("accessionNumber", "form", "primaryDocument", "filingDate", "reportDate", "acceptanceDateTime")
    columns = [recent[key] for key in keys]
    if any(not isinstance(column, list) for column in columns):
        raise ValueError("Expected column arrays in SEC submissions")
    rows = []
    for accession, form, filename, filed, event, accepted in zip(*columns, strict=True):
        if day(filed) < start:
            continue
        category = SEC_CATEGORIES.get(form.removesuffix("/A"))
        if category is None:
            continue
        if not re.fullmatch(r"\d{10}-\d{2}-\d{6}", accession) or not re.fullmatch(r"[\w.-]+\.html?", filename, re.ASCII):
            raise ValueError("Unexpected SEC accession or primary document filename")
        identifier = f"sec:{accession}"
        rows.append(document({
            "id": identifier, "origin": identifier, "publisher": "SEC EDGAR",
            "url": f"https://www.sec.gov/Archives/edgar/data/{int(ENTITY['cik'])}/{accession.replace('-', '')}/{filename}",
            "published_at": accepted or None, "published_date": filed, "event_date": event or None,
            "license": f"Public filing metadata under SEC Fair Access. {FAIR_ACCESS}",
            "category": category, "verification": "primary_source", "source_type": "filing",
            "claim": f"EDGAR recorded Medline Form {form}, accession {accession}.",
            "notes": "Registry metadata. The document's substantive assertions require human review.",
        }, retrieved_at, "sec"))
    archived_overlap = any(day(item["filingTo"]) >= start for item in filings.get("files", []))
    return rows, archived_overlap


def manual_rows(path, retrieved_at):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) - {"documents", "prices"}:
        raise ValueError("Expected a JSON object containing documents and/or prices")
    documents = payload.get("documents")
    prices = payload.get("prices")
    if any(value is not None and not isinstance(value, list) for value in (documents, prices)):
        raise ValueError("Documents and prices must be JSON arrays")
    rows = [document(row, retrieved_at, "documents_manual") for row in documents or []]
    rows.extend(bar(row, retrieved_at) for row in prices or [])
    return rows, {key for key, value in (("documents_manual", documents), ("market_manual", prices))
                  if value is not None}
