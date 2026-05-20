"""FastMCP 3.2 tool registration — glance utilities, RSS/Atom, weather, fleet probes."""

from __future__ import annotations

import os
from typing import Any

from fastmcp import FastMCP
from fastmcp.server import create_proxy

from glance_mcp.services import opml, probe, resolve, rss, utilities, weather

mcp = FastMCP(
    "glance-mcp",
    instructions=(
        "Dev utilities: UUID generation, hashing, base64, JSON format/validate, JWT decode, "
        "URL encode/decode, text stats, timestamp conversion, random values. "
        "Plus RSS/Atom fetch, Open-Meteo weather, fleet HTTP probes, redirect tracing, OPML import."
    ),
)

_bridge_proxies = []
bridge_urls = os.getenv("MCP_BRIDGE_URLS", "")
if bridge_urls:
    for url in bridge_urls.split(","):
        url = url.strip()
        if url:
            try:
                mcp.add_provider(create_proxy(url))
                _bridge_proxies.append(url)
            except Exception:
                pass


@mcp.tool()
async def rss_fetch_feed(feed_url: str, max_items: int = 25) -> dict[str, Any]:
    """RSS_FETCH_FEED — Download and parse an RSS or Atom feed (titles, links, summaries).

    PORTMANTEAU RATIONALE: RSS/Atom remains widely used (podcasts, blogs, newsrooms, GitHub releases).
    Agents use this to monitor sources without bespoke scrapers.

    Args:
        feed_url: HTTPS feed URL (Atom/RSS). Public internet by default; use GLANCE_RSS_ALLOW_PRIVATE_HOSTS=1 for LAN.
        max_items: Max entries to return (1–100).

    Returns:
        success, entries, feed_title, message; or error details.
    """
    try:
        return await rss.fetch_feed(feed_url, max_items=max_items)
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "entries": [],
            "feed_title": None,
        }


@mcp.tool()
async def open_meteo_forecast(
    latitude: float,
    longitude: float,
    timezone: str = "auto",
    forecast_days: int = 3,
) -> dict[str, Any]:
    """OPEN_METEO_FORECAST — Grid weather from Open-Meteo (no API key; HTTPS only).

    Args:
        latitude: WGS84 latitude.
        longitude: WGS84 longitude.
        timezone: IANA zone or \"auto\" (Open-Meteo resolves from coordinates).
        forecast_days: 1–16 days of daily/hourly context (API-limited).

    Returns:
        success, current/hourly blocks, timezone; or error.
    """
    try:
        return await weather.forecast(
            latitude,
            longitude,
            timezone=timezone,
            forecast_days=forecast_days,
        )
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


@mcp.tool()
async def fleet_http_probe(
    urls: list[str],
    timeout_seconds: float = 5.0,
    max_concurrency: int = 12,
) -> dict[str, Any]:
    """FLEET_HTTP_PROBE — Parallel GET for MCP /health or status URLs (localhost + LAN allowed).

    Blocks cloud metadata endpoints (169.254.169.254). Use for quick fleet dashboards.

    Args:
        urls: List of http(s) URLs (e.g. http://127.0.0.1:10746/health).
        timeout_seconds: Per-request timeout (0.5–60).
        max_concurrency: Parallel connection cap (1–32).

    Returns:
        success, results[] with ok, status_code, elapsed_ms, body_preview.
    """
    try:
        return await probe.probe_many(
            urls,
            timeout_s=timeout_seconds,
            max_concurrency=max_concurrency,
        )
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "results": [],
        }


@mcp.tool()
async def http_redirect_trace(
    url: str,
    max_hops: int = 15,
    timeout_seconds: float = 20.0,
    method: str = "head",
) -> dict[str, Any]:
    """HTTP_REDIRECT_TRACE — Follow http(s) redirects hop-by-hop; same allowlist as fleet probe.

    Use HEAD by default (lighter). Switch to GET if the server returns 405.

    Args:
        url: Starting URL.
        max_hops: Max redirect follows (1–30).
        timeout_seconds: Per-request timeout.
        method: \"head\" or \"get\".

    Returns:
        success, chain[] (url, status_code, location), final_url.
    """
    try:
        m = method.lower().strip()
        if m not in {"head", "get"}:
            return {"success": False, "error": "method must be head or get", "chain": []}
        return await resolve.trace_redirects(
            url,
            max_hops=max_hops,
            timeout_s=timeout_seconds,
            method=m,
        )
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "chain": [],
        }


@mcp.tool()
async def opml_list_feeds(opml_xml: str) -> dict[str, Any]:
    """OPML_LIST_FEEDS — Parse OPML XML text; return outline rows with xmlUrl (Atom/RSS feed URLs).

    Safe XML via defusedxml. Use for importing subscription lists into rss_fetch_feed.

    Args:
        opml_xml: Full OPML file content (UTF-8).

    Returns:
        success, feeds[] with title, xmlUrl, htmlUrl, type.
    """
    try:
        return opml.list_feeds_from_opml(opml_xml)
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "feeds": [],
        }


# ── Dev utilities ─────────────────────────────────────────────────────────────


@mcp.tool()
async def generate_uuid(version: int = 4) -> dict[str, Any]:
    """UUID — Generate a UUID v4 (random) or v7 (time-ordered).

    Args:
        version: 4 for random UUID, 7 for time-ordered UUID (default 4).

    Returns:
        The generated UUID string plus hex and URN forms.
    """
    return await utilities.generate_uuid(version=version)


@mcp.tool()
async def hash_text(text: str, algorithm: str = "sha256") -> dict[str, Any]:
    """HASH — Hash a string using MD5, SHA1, SHA256, or SHA512.

    Args:
        text: The string to hash.
        algorithm: md5, sha1, sha256, or sha512 (default sha256).

    Returns:
        Hex digest and algorithm info.
    """
    return await utilities.hash_text(text, algorithm=algorithm)


@mcp.tool()
async def base64_encode(text: str) -> dict[str, Any]:
    """B64_ENCODE — Encode a string as base64.

    Args:
        text: The string to encode.

    Returns:
        Base64-encoded string.
    """
    return await utilities.base64_encode(text)


@mcp.tool()
async def base64_decode(encoded: str) -> dict[str, Any]:
    """B64_DECODE — Decode a base64 string back to text.

    Args:
        encoded: The base64 string to decode.

    Returns:
        Decoded text or error if invalid.
    """
    return await utilities.base64_decode(encoded)


@mcp.tool()
async def json_tool(text: str, operation: str = "validate") -> dict[str, Any]:
    """JSON — Validate, format, or minify a JSON string.

    Args:
        text: JSON string to process.
        operation: validate, format, or minify (default validate).

    Returns:
        Validation status, formatted/minified output, and size metrics.
    """
    return await utilities.json_tool(text, operation=operation)


@mcp.tool()
async def jwt_decode(token: str) -> dict[str, Any]:
    """JWT — Decode a JWT token without signature verification.

    Args:
        token: The JWT token string (3 dot-separated base64 sections).

    Returns:
        Decoded header, payload, and truncated signature.
    """
    return await utilities.jwt_decode(token)


@mcp.tool()
async def url_encode(text: str) -> dict[str, Any]:
    """URL_ENCODE — Percent-encode a string for use in URLs.

    Args:
        text: The string to encode.

    Returns:
        URL-encoded string.
    """
    return await utilities.url_encode(text)


@mcp.tool()
async def url_decode(encoded: str) -> dict[str, Any]:
    """URL_DECODE — Decode a percent-encoded URL string back to readable form.

    Args:
        encoded: The percent-encoded string.

    Returns:
        Decoded string.
    """
    return await utilities.url_decode(encoded)


@mcp.tool()
async def text_stats(text: str) -> dict[str, Any]:
    """STATS — Count characters, words, lines, and sentences in text.

    Args:
        text: The text to analyze.

    Returns:
        Character, word, line, sentence, and byte counts.
    """
    return await utilities.text_stats(text)


@mcp.tool()
async def timestamp_info(timestamp: float | None = None, timezone: str = "UTC") -> dict[str, Any]:
    """TIME — Convert a UNIX timestamp to human-readable date/time. Defaults to now.

    Args:
        timestamp: UNIX timestamp (seconds since epoch). Default: current time.
        timezone: Not used yet (UTC only currently). Reserved param.

    Returns:
        ISO 8601, UTC date/time components, weekday, and UNIX ms.
    """
    return await utilities.timestamp_info(timestamp)


@mcp.tool()
async def random_value(
    kind: str = "uuid",
    length: int = 16,
    min_val: int = 0,
    max_val: int = 100,
) -> dict[str, Any]:
    """RANDOM — Generate random values: uuid, hex, password, int, float.

    Args:
        kind: uuid, hex, password, int, or float (default uuid).
        length: Length for hex/password (default 16).
        min_val: Minimum for int/float (default 0).
        max_val: Maximum for int/float (default 100).

    Returns:
        The generated random value with metadata.
    """
    return await utilities.random_value(kind=kind, length=length, min_val=min_val, max_val=max_val)
