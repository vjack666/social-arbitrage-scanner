"""Google-discovered public-page reader.

This module does NOT scrape Google result pages. Use Google in a browser to discover
URLs, then pass those public URLs to this reader. It checks robots.txt, fetches only
the supplied pages, and never bypasses logins, paywalls, or access controls.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urljoin, urlparse
from urllib.request import Request, urlopen
import urllib.robotparser

USER_AGENT = "SocialArbitrageScannerResearch/0.1 (+personal non-commercial research)"
TIMEOUT_SECONDS = 12
MAX_BYTES = 1_500_000
SKIP_TAGS = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form"}


def google_search_url(query: str) -> str:
    """Build a normal browser search URL; this function does not call Google."""
    query = query.strip()
    if not query:
        raise ValueError("query must not be empty")
    return "https://www.google.com/search?q=" + quote_plus(query)


class _PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.meta: dict[str, str] = {}
        self.canonical: str | None = None
        self._in_title = False
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {k.lower(): (v or "") for k, v in attrs}
        if tag.lower() in SKIP_TAGS:
            self._skip_depth += 1
        if tag.lower() == "title":
            self._in_title = True
        if tag.lower() == "meta":
            key = (values.get("property") or values.get("name") or values.get("itemprop")).lower()
            value = values.get("content", "").strip()
            if key and value:
                self.meta.setdefault(key, value)
        if tag.lower() == "link" and "canonical" in values.get("rel", "").lower():
            href = values.get("href", "").strip()
            if href:
                self.canonical = href

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False
        if tag.lower() in SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        cleaned = re.sub(r"\\s+", " ", data).strip()
        if not cleaned:
            return
        if self._in_title:
            self.title_parts.append(cleaned)
        if not self._skip_depth:
            self.text_parts.append(cleaned)


def parse_html(html: str, page_url: str) -> dict[str, Any]:
    """Extract accessible page text and metadata without inferring missing dates."""
    parser = _PageParser()
    parser.feed(html)
    meta = parser.meta
    title = " ".join(parser.title_parts).strip()
    description = meta.get("og:description") or meta.get("description") or ""
    published = (
        meta.get("article:published_time")
        or meta.get("datepublished")
        or meta.get("pubdate")
        or meta.get("date")
        or ""
    )
    canonical = urljoin(page_url, parser.canonical) if parser.canonical else page_url
    text = re.sub(r"\\s+", " ", " ".join(parser.text_parts)).strip()
    return {
        "url": page_url,
        "canonical_url": canonical,
        "title": title or None,
        "description": description or None,
        "published_at": published or None,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "content": text,
        "content_chars": len(text),
        "status": "ok" if len(text) >= 200 else "partial",
        "evidence_note": (
            "Page content extracted; claims remain unverified."
            if len(text) >= 200
            else "Only partial content was accessible; do not treat as full-page evidence."
        ),
    }


def _robots_allows(url: str) -> bool:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        request = Request(robots_url, headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read(256_000).decode("utf-8", errors="replace")
        rp.parse(raw.splitlines())
        return rp.can_fetch(USER_AGENT, url)
    except (HTTPError, URLError, TimeoutError, OSError):
        # Fail closed: if access rules cannot be checked, skip the page.
        return False


def read_public_page(url: str) -> dict[str, Any]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Only absolute HTTP(S) URLs are allowed: {url!r}")
    if not _robots_allows(url):
        return {
            "url": url,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "status": "blocked",
            "content": "",
            "evidence_note": "Skipped because robots.txt disallows access or could not be checked.",
        }
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            content_type = response.headers.get_content_type()
            if content_type not in {"text/html", "application/xhtml+xml"}:
                return {
                    "url": url,
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "status": "unsupported_content_type",
                    "content": "",
                    "evidence_note": f"Skipped non-HTML content type: {content_type}",
                }
            raw = response.read(MAX_BYTES + 1)
            truncated = len(raw) > MAX_BYTES
            html = raw[:MAX_BYTES].decode(response.headers.get_content_charset() or "utf-8", errors="replace")
            result = parse_html(html, response.geturl())
            result["truncated"] = truncated
            if truncated:
                result["status"] = "partial"
                result["evidence_note"] = "Content truncated at configured byte limit; partial evidence only."
            return result
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        return {
            "url": url,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "status": "fetch_error",
            "content": "",
            "evidence_note": f"Fetch failed without bypassing access controls: {type(exc).__name__}",
        }


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--query", help="Print a Google browser search URL; does not query Google automatically.")
    cli.add_argument("--url", action="append", default=[], help="Public result URL copied from Google; may be repeated.")
    cli.add_argument("--out", help="Optional JSON output path.")
    args = cli.parse_args(argv)

    if args.query:
        print("Open this URL in a browser and select public result pages:")
        print(google_search_url(args.query))
    if not args.url:
        if not args.query:
            cli.error("provide --query and/or at least one --url")
        return 0

    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for url in args.url:
        result = read_public_page(url)
        key = result.get("canonical_url") or result.get("url")
        if key in seen:
            continue
        seen.add(key)
        results.append(result)

    output = json.dumps(results, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(output + "\n", encoding="utf-8")
        print(f"Wrote {len(results)} result(s) to {args.out}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
