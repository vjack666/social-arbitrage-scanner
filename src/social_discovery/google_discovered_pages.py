"""Google-discovered public-page reader.

This module does NOT scrape Google result pages. Use Google in a browser to discover
URLs, then pass those public URLs to this reader. It checks robots.txt, fetches only
the supplied pages, and never bypasses logins, paywalls, or access controls.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import ipaddress
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import socket
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener
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


def _validate_public_url(url: str) -> None:
    """Reject non-HTTP URLs, credentials, and hosts resolving to non-public IPs."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError(f"Only absolute HTTP(S) URLs are allowed: {url!r}")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URLs containing embedded credentials are not allowed")
    host = parsed.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
        raise ValueError("Local hostnames are not allowed")
    try:
        literal_ip = ipaddress.ip_address(host)
    except ValueError:
        literal_ip = None
    if literal_ip is not None:
        if not literal_ip.is_global:
            raise ValueError("Non-public IP addresses are not allowed")
        return
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80))}
    except OSError as exc:
        raise ValueError(f"Could not resolve public hostname: {host}") from exc
    if not addresses or any(not ipaddress.ip_address(address.split("%")[0]).is_global for address in addresses):
        raise ValueError("Hostname resolves to a non-public IP address")


class _PublicRedirectHandler(HTTPRedirectHandler):
    """Re-check every redirect target to reduce server-side request forgery risk."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urljoin(req.full_url, newurl)
        _validate_public_url(target)
        return super().redirect_request(req, fp, code, msg, headers, target)


def _open_public(request: Request):
    _validate_public_url(request.full_url)
    return build_opener(_PublicRedirectHandler()).open(request, timeout=TIMEOUT_SECONDS)


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
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            key = (values.get("property") or values.get("name") or values.get("itemprop")).lower()
            value = values.get("content", "").strip()
            if key and value:
                self.meta.setdefault(key, value)
        if tag == "link" and "canonical" in values.get("rel", "").lower():
            href = values.get("href", "").strip()
            if href:
                self.canonical = href

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        if tag in SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        cleaned = re.sub(r"\s+", " ", data).strip()
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
    text = re.sub(r"\s+", " ", " ".join(parser.text_parts)).strip()
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
        with _open_public(request) as response:
            raw = response.read(256_000).decode("utf-8", errors="replace")
        rp.parse(raw.splitlines())
        return rp.can_fetch(USER_AGENT, url)
    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        # Fail closed: if access rules cannot be checked, skip the page.
        return False


def read_public_page(url: str) -> dict[str, Any]:
    _validate_public_url(url)
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
        with _open_public(request) as response:
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
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
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
        try:
            result = read_public_page(url)
        except ValueError as exc:
            result = {
                "url": url,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "status": "blocked",
                "content": "",
                "evidence_note": str(exc),
            }
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
