# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Documentation

- **`glama.json`** — `description` aligned with README (holdall / at-a-glance framing).
- **README** — Hero and “Why glance?” framing (holdall for **at-a-glance** retrieval: feeds, weather, fleet, redirects, OPML); refreshed tables for tools and features.
- **PRD** — Vision aligned with that framing; **non-goals** clarified (reader product vs parse/list; no scrapers).
- **EXAMPLE_FEEDS** — Table structure repaired; **Browsers vs readers** + **web_sota** Feedly/Inoreader note.

## [0.2.0] — 2026-03-20

### Added

- **Tools:** `http_redirect_trace` (hop-by-hop redirects; HEAD/GET), `opml_list_feeds` (OPML → `xmlUrl` list via **defusedxml**).
- **REST:** `POST /api/resolve/trace`, `POST /api/opml/feeds`.
- **Web SPA:** sidebar items **Redirects** + **OPML**; curated feeds doc + GitHub metadata (see 0.1.0 notes).
- **Docs:** [docs/POLICY_NO_SCRAPE.md](docs/POLICY_NO_SCRAPE.md) — why TV Tropes / Anna’s Archive–style scrapers are out of scope.

### Changed

- **Web SPA:** RSS / probe **clickable links**; **retractable sidebar** + `localStorage`; raw JSON under `<details>`.

### Documentation

- Canonical repo: [sandraschi/glance-mcp](https://github.com/sandraschi/glance-mcp).

## [0.1.0] — 2026-03-20

### Added

- **FastMCP 3.1** tools: `rss_fetch_feed`, `open_meteo_forecast`, `fleet_http_probe`.
- **FastAPI** backend on **10776**: `/health`, OpenAPI `/docs`, MCP streamable HTTP **`/mcp`**, REST `/api/rss/fetch`, `/api/weather/forecast`, `/api/probe`.
- **Vite + React** SPA on **10777** (`web_sota/start.ps1`).
- **SSRF-aware** URL checks: RSS blocks private/loopback unless opted in; probes block cloud metadata IP.
- **`justfile`**, **`glama.json`**, `uv` + **ruff** + **pytest**.
