# Product requirements: glance-mcp

## Vision: what “glance” means

**Glance** is a **holdall** for **at-a-glance information retrieval** — not a knowledge base, not a scraper farm, not a calendar. It bundles small HTTP utilities so an agent can answer “what’s the headline story?”, “what’s the weather?”, “are my backends up?”, “where does this URL redirect?”, and “what feeds are in this OPML export?” **without** wiring five separate integrations.

**You understood it right:** the name is intentional shorthand for **quick situational awareness** (feeds, weather, health, redirects, OPML) rather than deep research or long-form storage.

## Overview

**glance-mcp** exposes those utilities as **FastMCP 3.1** tools plus a **FastAPI** façade (REST + streamable MCP at `/mcp`, fleet ports **10776** / **10777**). It targets single-user Cursor / fleet setups on Windows with **conservative outbound URL rules** (SSRF-minded RSS and probes).

## Goals

- Give agents **one** dependency-light server for:

  - **Feeds** — “What’s new in this feed?” (`rss_fetch_feed`)
  - **Weather** — “What’s the forecast at these coordinates?” (`open_meteo_forecast`, Open-Meteo, no API key)
  - **Fleet** — “Are my MCP backends up?” (`fleet_http_probe`, parallel GETs to `/health`-style URLs)
  - **Redirects** — “Where does this hop chain go?” (`http_redirect_trace`)
  - **OPML** — “List feed URLs from an export” (`opml_list_feeds`)

- Ship **FastMCP 3.1** + **FastAPI** with streamable MCP at `/mcp`, SPA **10777** proxying API **10776**.
- Default **safe** behavior: block RSS fetches to private/loopback unless configured; block cloud metadata IP for probes; no general-purpose HTML scraping (see [POLICY_NO_SCRAPE.md](POLICY_NO_SCRAPE.md)).

## Non-goals

- Replacing dedicated media, calendar, or knowledge MCPs.
- Full **reader product** (subscriptions, polling schedules, read-state sync) — **out of scope**; we parse and list, and link to Feedly/Inoreader for human subscribe flows.
- **Site-specific scrapers** (e.g. TV Tropes, paywalled archives) — out of scope.

## Success criteria

- Tools return structured `success` / `error` dicts; pytest + ruff pass.
- `GET /health` and SPA proxy work on registered fleet ports.
- README and curated feed docs stay accurate for **human** readers (hero story, subscribe links, policy boundaries).
