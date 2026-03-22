"""Parallel HTTP GET health checks."""

from __future__ import annotations

import asyncio
import time
from typing import Any

import httpx

from glance_mcp.net_safety import assert_safe_for_probe, normalize_url


async def _one(
    url: str,
    *,
    client: httpx.AsyncClient,
) -> dict[str, Any]:
    try:
        u = normalize_url(url)
        assert_safe_for_probe(u)
    except Exception as e:
        return {"url": url, "ok": False, "error": str(e), "status_code": None, "elapsed_ms": None}
    t0 = asyncio.get_event_loop().time()
    try:
        r = await client.get(u, follow_redirects=True)
        elapsed_ms = int((asyncio.get_event_loop().time() - t0) * 1000)
        body_preview = (r.text or "")[:800]
        return {
            "url": u,
            "ok": 200 <= r.status_code < 400,
            "status_code": r.status_code,
            "elapsed_ms": elapsed_ms,
            "content_length": len(r.content),
            "body_preview": body_preview,
        }
    except Exception as e:
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        return {
            "url": url,
            "ok": False,
            "error": str(e),
            "status_code": None,
            "elapsed_ms": elapsed_ms,
        }


async def probe_many(
    urls: list[str],
    *,
    timeout_s: float = 5.0,
    max_concurrency: int = 12,
) -> dict[str, Any]:
    """GET each URL; return structured per-URL results."""
    if not urls:
        return {"success": False, "error": "urls list is empty.", "results": []}
    if len(urls) > 64:
        return {"success": False, "error": "Max 64 URLs per batch.", "results": []}
    timeout_s = max(0.5, min(timeout_s, 60.0))
    max_concurrency = max(1, min(max_concurrency, 32))
    sem = asyncio.Semaphore(max_concurrency)

    async def wrapped(u: str) -> dict[str, Any]:
        async with sem:
            return await _one(u, client=client)

    limits = httpx.Limits(max_connections=max_concurrency + 2)
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(timeout_s),
        limits=limits,
        headers={
            "User-Agent": "glance-mcp/0.1 health-probe (+https://github.com/sandraschi/glance-mcp)",
        },
    ) as client:
        results = await asyncio.gather(*[wrapped(u) for u in urls])
    ok_n = sum(1 for r in results if r.get("ok"))
    return {
        "success": True,
        "message": f"{ok_n}/{len(results)} probe(s) OK.",
        "results": list(results),
    }
