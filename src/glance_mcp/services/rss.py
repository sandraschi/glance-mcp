"""RSS/Atom via feedparser + httpx size cap."""

from __future__ import annotations

import asyncio
import io
from typing import Any

import feedparser
import httpx

from glance_mcp.config import load_settings
from glance_mcp.net_safety import assert_safe_for_rss, normalize_url


def _parse_feed_bytes(data: bytes, url: str) -> dict[str, Any]:
    parsed = feedparser.parse(io.BytesIO(data))
    if getattr(parsed, "bozo", False) and not parsed.entries:
        err = getattr(parsed, "bozo_exception", None)
        return {
            "success": False,
            "error": f"Parse error: {err!s}" if err else "Parse error (malformed feed).",
            "entries": [],
            "feed_title": None,
        }
    feed_title = parsed.feed.get("title") if parsed.feed else None
    entries: list[dict[str, Any]] = []
    for e in parsed.entries[:500]:
        entries.append(
            {
                "title": e.get("title"),
                "link": e.get("link") or (e.get("links") or [{}])[0].get("href"),
                "published": e.get("published") or e.get("updated"),
                "summary": (e.get("summary") or "")[:8000],
                "id": e.get("id"),
            }
        )
    return {
        "success": True,
        "message": f"Parsed {len(entries)} entry/entries.",
        "feed_title": feed_title,
        "feed_link": parsed.feed.get("link") if parsed.feed else None,
        "entries": entries,
        "resolved_url": url,
    }


async def fetch_feed(
    feed_url: str,
    max_items: int = 25,
    *,
    user_agent: str = "glance-mcp/0.1 (+https://github.com/sandraschi/glance-mcp)",
) -> dict[str, Any]:
    """Download feed XML with size cap, then parse."""
    settings = load_settings()
    url = normalize_url(feed_url)
    assert_safe_for_rss(url, allow_private_hosts=settings.rss_allow_private_hosts)

    max_items = max(1, min(max_items, 100))
    max_bytes = settings.rss_max_bytes

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        follow_redirects=True,
        headers={"User-Agent": user_agent},
    ) as client:
        async with client.stream("GET", url) as resp:
            final_url = str(resp.url)
            if resp.status_code >= 400:
                body = await resp.aread()
                return {
                    "success": False,
                    "error": f"HTTP {resp.status_code}",
                    "entries": [],
                    "feed_title": None,
                    "body_preview": body[:500].decode("utf-8", errors="replace"),
                }
            chunks: list[bytes] = []
            total = 0
            async for chunk in resp.aiter_bytes():
                total += len(chunk)
                if total > max_bytes:
                    return {
                        "success": False,
                        "error": f"Feed response exceeded {max_bytes} bytes (cap).",
                        "entries": [],
                        "feed_title": None,
                    }
                chunks.append(chunk)
            data = b"".join(chunks)

    result = await asyncio.to_thread(_parse_feed_bytes, data, final_url)
    if result.get("success") and isinstance(result.get("entries"), list):
        result["entries"] = result["entries"][:max_items]
        result["message"] = f"Returning {len(result['entries'])} item(s) (max {max_items})."
    return result
