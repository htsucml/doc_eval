"""Answer normalization helpers shared across metrics and reporting."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
import re


NOT_FOUND_CANONICAL = "not_found"

_NOT_FOUND_VALUES = {
    "",
    "n/a",
    "na",
    "none",
    "null",
    "nil",
    "not found",
    "not_found",
    "not available",
    "unavailable",
    "unknown",
    "missing",
    "no answer",
    "cannot determine",
    "can't determine",
}

_DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%m/%d/%Y",
    "%m-%d-%Y",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%b %d %Y",
    "%B %d %Y",
    "%d %b %Y",
    "%d %B %Y",
    "%b %d, %Y",
    "%B %d, %Y",
    "%d %b, %Y",
    "%d %B, %Y",
)

_NUMERIC_ANSWER_TYPES = {"integer", "float", "number", "currency", "amount", "percentage"}
_CODE_ANSWER_TYPES = {"code", "serial", "serial_number", "id", "identifier"}


def normalize_text(text: str | None) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip()).casefold()


def is_not_found_response(text: str | None) -> bool:
    compact = normalize_text(text).replace("_", " ")
    return compact in {value.replace("_", " ") for value in _NOT_FOUND_VALUES}


def normalize_not_found(text: str | None) -> str | None:
    return NOT_FOUND_CANONICAL if is_not_found_response(text) else None


def normalize_serial(text: str | None) -> str | None:
    compact = re.sub(r"[^A-Za-z0-9]+", "", str(text or "")).upper()
    return compact or None


def normalize_date(text: str | None) -> str | None:
    raw = str(text or "").strip()
    if not raw:
        return None
    cleaned = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", raw, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned.replace(".", " ")).strip()
    cleaned = re.sub(r"\s+,", ",", cleaned)
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(cleaned, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def parse_decimal(text: str | None) -> Decimal | None:
    raw = str(text or "").strip()
    if not raw:
        return None
    negative = raw.startswith("(") and raw.endswith(")")
    cleaned = raw.replace(",", "")
    cleaned = re.sub(r"(?i)\b(?:usd|eur|gbp|jpy|twd|ntd|cad|aud)\b", "", cleaned)
    cleaned = cleaned.replace("NT$", "").replace("$", "").replace("€", "").replace("£", "").replace("¥", "")
    cleaned = cleaned.replace("%", "")
    match = re.search(r"[-+]?\d*\.?\d+", cleaned)
    if not match:
        return None
    token = match.group(0)
    if negative and not token.startswith("-"):
        token = f"-{token}"
    try:
        return Decimal(token)
    except InvalidOperation:
        return None


def _format_decimal(value: Decimal) -> str:
    rendered = format(value.normalize(), "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered or "0"


def normalize_amount(text: str | None) -> str | None:
    value = parse_decimal(text)
    if value is None:
        return None
    return _format_decimal(value)


def normalize_answer(text: str | None, answer_type: str | None = None) -> str:
    not_found = normalize_not_found(text)
    if not_found is not None:
        return not_found

    if answer_type == "date":
        normalized_date = normalize_date(text)
        if normalized_date is not None:
            return normalized_date

    if answer_type in _NUMERIC_ANSWER_TYPES:
        normalized_amount = normalize_amount(text)
        if normalized_amount is not None:
            return normalized_amount

    if answer_type in _CODE_ANSWER_TYPES:
        normalized_serial = normalize_serial(text)
        if normalized_serial is not None:
            return normalized_serial

    return normalize_text(text)


def is_numeric_answer_type(answer_type: str | None) -> bool:
    return answer_type in _NUMERIC_ANSWER_TYPES


def is_anls_applicable(answer_type: str | None) -> bool:
    return answer_type not in _NUMERIC_ANSWER_TYPES and answer_type != "abstain"
