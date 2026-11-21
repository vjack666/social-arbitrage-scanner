"""Validate and normalize the evidence stored in a snapshot."""

from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
import re
from urllib.parse import urlsplit

ENTITY = {"name": "Medline Inc.", "ticker": "MDLN", "cik": "0002046386", "market": "XNAS"}
VERSION = "0.1.0"
CONTRACT = "0.1"
CATEGORIES = {"earnings", "capital", "regulatory", "listing", "product", "other"}
HIGH_IMPACT = {"binding_terms", "guidance", "process_status"}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def digest(value):
    return sha256(canonical(value).encode("utf-8")).hexdigest()


def utc(value):
    if not isinstance(value, str):
        raise ValueError("Timestamp must be an ISO 8601 string with an explicit offset")
    instant = datetime.fromisoformat(value)
    if instant.utcoffset() is None:
        raise ValueError("Timestamp requires an explicit UTC offset")
    return instant.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def today_utc():
    return utc(datetime.now(timezone.utc).isoformat())


def day(value):
    return date.fromisoformat(value).isoformat()


def text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return value.strip()


def reference(value):
    value = text(value, "source URL")
    url = urlsplit(value)
    if (url.scheme != "https" or not url.hostname or url.username or url.password
            or any(char.isspace() or char in "<>\\\\" for char in value)):
        raise ValueError("Source reference must be HTTPS without credentials")
    return value


def source_fields(row, retrieved_at):
    published_at = utc(row["published_at"]) if row.get("published_at") else None
    event_at = utc(row["event_at"]) if row.get("event_at") else None
    available_at = utc(row["available_at"]) if row.get("available_at") else published_at
    if published_at and available_at < published_at:
        raise ValueError("Availability precedes publication")
    retrieved_at = utc(row.get("retrieved_at") or retrieved_at)
    if retrieved_at > today_utc():
        raise ValueError("Retrieval cannot occur in the future")
    if available_at and available_at > retrieved_at:
        raise ValueError("Availability cannot be later than retrieval")
    return {
        "publisher": text(row["publisher"], "publisher"),
        "url": reference(row["url"]),
        "published_at": published_at,
        "published_date": day(row["published_date"]) if row.get("published_date") else None,
        "event_at": event_at,
        "event_date": day(row["event_date"]) if row.get("event_date") else None,
        "available_at": available_at,
        "retrieved_at": retrieved_at,
        "license": text(row["license"], "license"),
    }


def document(row, retrieved_at, channel):
    common = source_fields(row, retrieved_at)
    category = row["category"]
    state = row["verification"]
    if category not in CATEGORIES or state not in {"primary_source", "corroborated", "unverified", "disputed", "retracted"}:
        raise ValueError("Invalid document category or verification")
    impact = row.get("impact")
    if impact is not None and impact not in HIGH_IMPACT:
        raise ValueError("Invalid impact reason")
    event_id = text(row["id"], "event id") if row.get("id") else urlsplit(common["url"])._replace(fragment="").geturl()
    origin = text(row.get("origin") or event_id, "independent origin")
    claim = text(row["claim"], "claim")
    source_type = text(row["source_type"], "source type")
    primary = source_type in {"filing", "issuer_release", "regulator", "exchange"}
    if state == "primary_source" and not primary:
        raise ValueError("A primary-source claim requires a primary source type")
    return {
        **common, "kind": "document", "channel": channel, "id": event_id,
        "origin": origin, "category": category, "source_type": source_type,
        "verification": state, "claim": claim, "impact": impact,
        "source_version": text(row["source_version"], "source version") if row.get("source_version") else None,
        "notes": text(row["notes"], "notes") if row.get("notes") else None,
    }


def positive_decimal(raw):
    try:
        value = Decimal(str(raw))
    except InvalidOperation as error:
        raise ValueError("Prices must be finite positive decimals") from error
    if not value.is_finite() or value <= 0 or abs(value.adjusted()) > 10:
        raise ValueError("Price outside supported decimal range")
    return format(value.normalize(), "f")


def bar(row, retrieved_at):
    common = source_fields(row, retrieved_at)
    session = day(row["session"])
    if not common["event_at"] or datetime.fromisoformat(row["event_at"]).date().isoformat() != session:
        raise ValueError("A bar needs the local session-end timestamp")
    if common["available_at"] and common["available_at"] < common["event_at"]:
        raise ValueError("A daily bar cannot be known before its session ends")
    provider = text(row["provider"], "provider")
    adjustment = row["adjustment"]
    if adjustment not in {"as_traded", "split_adjusted", "total_return_adjusted", "unknown"}:
        raise ValueError("Unsupported market adjustment")
    currency = row["currency"]
    if not re.fullmatch("[A-Z]{3}", currency):
        raise ValueError("Currency must be an ISO three-letter code")
    prices = {key: positive_decimal(row[key]) if row.get(key) is not None else None
              for key in ("open", "high", "low", "close")}
    known = [Decimal(value) for value in prices.values() if value is not None]
    if not known:
        raise ValueError("A bar needs at least one price")
    if prices["low"] and Decimal(prices["low"]) != min(known):
        raise ValueError("Inconsistent daily low")
    if prices["high"] and Decimal(prices["high"]) != max(known):
        raise ValueError("Inconsistent daily high")
    volume = row.get("volume")
    if volume is not None and (type(volume) is not int or volume < 0):
        raise ValueError("Volume must be a nonnegative integer in shares")
    return {
        **common, **prices, "kind": "bar", "channel": "market_manual",
        "id": canonical([provider, session, currency, adjustment]), "origin": provider,
        "provider": provider, "session": session, "timezone": "America/New_York",
        "currency": currency, "adjustment": adjustment, "volume": volume,
        "notes": text(row["notes"], "notes") if row.get("notes") else None,
    }


def version_fields(row):
    """Exclude observation metadata that may differ on a retry."""
    return {key: value for key, value in row.items() if key not in {"retrieved_at"}}
