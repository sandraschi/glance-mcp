"""FastMCP 3.1 tool registration."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from glance_mcp.services import opml, probe, resolve, rss, weather

mcp = FastMCP(
    "glance-mcp",
    instructions=(
        "Public-surface utilities: RSS/Atom feed fetch, OPML→feed URL list, HTTP redirect chain trace, "
        "Open-Meteo weather (no API key), parallel GET probes for fleet /health endpoints."
    ),
)


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
