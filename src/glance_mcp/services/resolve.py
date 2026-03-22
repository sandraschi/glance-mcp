"""HTTP redirect chain tracing (same safety rules as fleet probe)."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import httpx

from glance_mcp.net_safety import assert_safe_for_probe
from glance_mcp.net_safety import normalize_url

_REDIRECT_STATUSES = frozenset({301, 302, 303, 307, 308})


async def trace_redirects(
    url: str,
    *,
    max_hops: int = 15,
    timeout_s: float = 20.0,
    method: str = "head",
) -> dict[str, Any]:
    """Follow redirects manually; record each hop (URL + status)."""
    max_hops = max(1, min(max_hops, 30))
    m = method.lower().strip()
    if m not in {"head", "get"}:
        return {"success": False, "error": "method must be 'head' or 'get'."}

    try:
        first = normalize_url(url)
        assert_safe_for_probe(first)
    except Exception as e:
        return {"success": False, "error": str(e), "chain": []}

    chain: list[dict[str, Any]] = []
    current = first
    timeout = httpx.Timeout(timeout_s)

    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=False,
        headers={"User-Agent": "glance-mcp/0.2 (+https://github.com/sandraschi/glance-mcp)"},
    ) as client:
        for hop in range(max_hops):
            try:
                assert_safe_for_probe(current)
            except Exception as e:
                chain.append({"url": current, "error": str(e), "hop": hop})
                return {
                    "success": False,
                    "error": str(e),
                    "chain": chain,
                    "final_url": current,
                    "hop_count": len(chain),
                }

            req = client.head if m == "head" else client.get
            try:
                r = await req(current)
            except Exception as e:
                chain.append(
                    {
                        "url": current,
                        "status_code": None,
                        "error": str(e),
                        "hop": hop,
                    }
                )
                return {
                    "success": False,
                    "error": str(e),
                    "chain": chain,
                    "final_url": current,
                    "hop_count": len(chain),
                }

            entry: dict[str, Any] = {
                "hop": hop,
                "url": str(r.request.url),
                "status_code": r.status_code,
            }
            if r.status_code in _REDIRECT_STATUSES:
                loc = r.headers.get("location")
                entry["location"] = loc
                chain.append(entry)
                if not loc:
                    return {
                        "success": True,
                        "message": "Redirect without Location header.",
                        "chain": chain,
                        "final_url": str(r.request.url),
                        "hop_count": len(chain),
                    }
                current = urljoin(str(r.request.url), loc.strip())
                continue

            chain.append(entry)
            return {
                "success": True,
                "message": f"Resolved after {len(chain)} hop(s).",
                "chain": chain,
                "final_url": str(r.request.url),
                "hop_count": len(chain),
            }

    return {
        "success": False,
        "error": f"Exceeded max_hops ({max_hops}).",
        "chain": chain,
        "final_url": current,
        "hop_count": len(chain),
    }
