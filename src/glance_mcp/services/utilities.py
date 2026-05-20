"""Pure utility functions — no external deps, no API keys, no network."""
# ruff: noqa: S311 — non-cryptographic random is acceptable for these tools

from __future__ import annotations

import base64
import hashlib
import json
import random
import string
import time
import uuid
from datetime import UTC, datetime
from typing import Any


async def generate_uuid(version: int = 4) -> dict[str, Any]:
    """Generate a UUID (v4 random or v7 time-ordered)."""
    if version == 7:
        val = uuid.uuid7()
    else:
        val = uuid.uuid4()
    return {
        "success": True,
        "uuid": str(val),
        "version": version,
        "hex": val.hex,
        "urn": f"urn:uuid:{val}",
    }


async def hash_text(text: str, algorithm: str = "sha256") -> dict[str, Any]:
    """Hash a string using MD5, SHA1, SHA256, or SHA512."""
    alg = algorithm.lower()
    data = text.encode("utf-8")
    if alg == "md5":
        h = hashlib.md5(data)  # noqa: S324
    elif alg == "sha1":
        h = hashlib.sha1(data)  # noqa: S324
    elif alg == "sha256":
        h = hashlib.sha256(data)
    elif alg == "sha512":
        h = hashlib.sha512(data)
    else:
        return {"success": False, "error": f"Unsupported algorithm: {algorithm}. Use md5, sha1, sha256, sha512."}
    return {"success": True, "algorithm": alg, "hex": h.hexdigest(), "input_length": len(text)}


async def base64_encode(text: str) -> dict[str, Any]:
    """Base64-encode a string."""
    encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
    return {"success": True, "encoded": encoded, "original_length": len(text)}


async def base64_decode(encoded: str) -> dict[str, Any]:
    """Decode a base64 string."""
    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
        return {"success": True, "decoded": decoded}
    except Exception as e:
        return {"success": False, "error": f"Invalid base64: {e}"}


async def json_tool(text: str, operation: str = "validate") -> dict[str, Any]:
    """Validate, format, or minify JSON."""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON: {e}", "position": e.pos}

    if operation == "validate":
        return {"success": True, "valid": True, "type": type(parsed).__name__}
    elif operation == "format":
        formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
        return {"success": True, "formatted": formatted,
                "original_length": len(text), "formatted_length": len(formatted)}
    elif operation == "minify":
        minified = json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)
        return {"success": True, "minified": minified, "original_length": len(text), "minified_length": len(minified)}
    else:
        return {"success": False, "error": f"Unknown operation: {operation}. Use validate, format, or minify."}


async def jwt_decode(token: str) -> dict[str, Any]:
    """Decode a JWT token without signature verification."""
    parts = token.split(".")
    if len(parts) != 3:
        return {"success": False, "error": "Invalid JWT format — expected 3 dot-separated sections"}
    try:
        header = json.loads(base64.urlsafe_b64decode(parts[0] + "==").decode("utf-8"))
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "==").decode("utf-8"))
        return {"success": True, "header": header, "payload": payload, "signature": parts[2][:20] + "..."}
    except Exception as e:
        return {"success": False, "error": f"Failed to decode JWT: {e}"}


async def url_encode(text: str) -> dict[str, Any]:
    """URL-percent-encode a string."""
    from urllib.parse import quote
    return {"success": True, "encoded": quote(text, safe=""), "original": text}


async def url_decode(encoded: str) -> dict[str, Any]:
    """Decode a URL-percent-encoded string."""
    from urllib.parse import unquote
    return {"success": True, "decoded": unquote(encoded), "original": encoded}


async def text_stats(text: str) -> dict[str, Any]:
    """Count characters, words, lines, sentences in text."""
    lines = text.splitlines()
    words = text.split()
    sentences = sum(1 for c in text if c in ".!?")
    return {
        "success": True,
        "characters": len(text),
        "characters_no_spaces": len(text.replace(" ", "")),
        "words": len(words),
        "lines": len(lines),
        "sentences": sentences,
        "bytes": len(text.encode("utf-8")),
    }


async def timestamp_info(timestamp: float | None = None, timezone: str = "UTC") -> dict[str, Any]:
    """Convert a UNIX timestamp to human-readable date/time. Defaults to now."""
    ts = timestamp if timestamp is not None else time.time()
    dt = datetime.fromtimestamp(ts, tz=UTC)
    return {
        "success": True,
        "timestamp": ts,
        "iso_8601": dt.isoformat(),
        "utc_date": dt.strftime("%Y-%m-%d"),
        "utc_time": dt.strftime("%H:%M:%S"),
        "utc_datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "year": dt.year,
        "month": dt.month,
        "day": dt.day,
        "hour": dt.hour,
        "minute": dt.minute,
        "weekday": dt.strftime("%A"),
        "unix_ms": int(ts * 1000),
    }


async def random_value(
    kind: str = "uuid",
    length: int = 16,
    min_val: int = 0,
    max_val: int = 100,
) -> dict[str, Any]:
    """Generate random values: uuid, hex, password, int, float, bytes."""
    k = kind.lower()
    if k == "uuid":
        return {"success": True, "kind": "uuid", "value": str(uuid.uuid4())}
    elif k == "hex":
        return {"success": True, "kind": "hex", "value": random.randbytes(length).hex(), "length": length}
    elif k == "password":
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return {"success": True, "kind": "password",
                "value": "".join(random.choice(chars) for _ in range(length)),
                "length": length}
    elif k == "int":
        return {"success": True, "kind": "int", "value": random.randint(min_val, max_val),
                "range": [min_val, max_val]}
    elif k == "float":
        return {"success": True, "kind": "float",
                "value": random.uniform(min_val, max_val),
                "range": [min_val, max_val]}
    else:
        return {"success": False, "error": f"Unknown kind: {kind}. Use uuid, hex, password, int, float."}
