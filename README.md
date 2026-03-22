# glance-mcp

<div align="center">

**At-a-glance information in one MCP**

*A small **holdall** for feeds, weather, fleet health, redirects, and OPML — so agents and tools can skim the world without juggling five integrations.*

</div>

---

## Why “glance”?

**Glance** is the product idea in one word: **quick situational awareness**, not deep archives. This server is a **holdall** — one place to **retrieve** things you’d otherwise glance at in passing: **what’s new in a syndicated feed**, **what’s the forecast here**, **are my localhost MCPs healthy**, **where does this URL redirect**, **which URLs are in this OPML export**. It is **not** a replacement for knowledge-base MCPs, scrapers, or a full feed reader; it’s the lightweight HTTP façade that gets you those answers fast.

---

## You might use this if…

| | |
|--:|--|
| **You want** | One MCP to **skim RSS/Atom**, **check Open-Meteo weather** (no API key), **probe parallel `/health` URLs**, **trace redirects**, and **parse OPML → feed list** — with conservative SSRF rules. |
| **You don’t need** | A second brain, a scraper for arbitrary sites, or subscription management — see [docs/POLICY_NO_SCRAPE.md](docs/POLICY_NO_SCRAPE.md). |

**Repo:** [github.com/sandraschi/glance-mcp](https://github.com/sandraschi/glance-mcp) · **`glama.json`** at repo root.

---

## What’s inside

| Area | What it does |
|------|----------------|
| **Feeds** | RSS/Atom via `feedparser`, size-capped download; curated examples in [docs/EXAMPLE_FEEDS.md](docs/EXAMPLE_FEEDS.md). Raw feeds look like XML in a browser — the **web UI** lists entries and offers **Feedly / Inoreader** subscribe links. |
| **Weather** | Open-Meteo `https://api.open-meteo.com/v1/forecast` — WGS84 lat/lon, no vendor key. |
| **Fleet** | Parallel GET to your MCP health URLs (loopback/LAN; blocks cloud metadata IP). |
| **Redirects** | Hop-by-hop redirect trace (HEAD/GET). |
| **OPML** | Extract `xmlUrl` list from subscription export XML (defused parsing). |

---

## MCP tools

| Tool | Role |
|------|------|
| `rss_fetch_feed` | Feed URL + `max_items` (1–100) |
| `open_meteo_forecast` | `latitude`, `longitude`, `timezone`, `forecast_days` |
| `fleet_http_probe` | `urls[]`, `timeout_seconds`, `max_concurrency` |
| `http_redirect_trace` | Redirect chain for a URL |
| `opml_list_feeds` | OPML → list of feed URLs |

REST mirrors: `POST /api/rss/fetch`, `/api/weather/forecast`, `/api/probe`, `/api/resolve/trace`, `/api/opml/feeds` (same ideas as the SPA).

---

## Run

**Stdio (Cursor / Claude):**

```powershell
uv sync
uv run glance-mcp
```

**HTTP + MCP at `/mcp` (fleet / bridge):**

```powershell
uv run glance-mcp --serve
```

- **API:** `http://127.0.0.1:10776` — `/health`, `/docs`, MCP `http://127.0.0.1:10776/mcp`
- **Env:** `GLANCE_MCP_HOST`, `GLANCE_MCP_PORT` (default **10776**), `GLANCE_MCP_HTTP_PATH` (default `/mcp`)

**Full SPA (Vite **10777**):**

```powershell
.\web_sota\start.ps1
```

Opens `http://127.0.0.1:10777/` (proxies `/api` and `/health` to **10776**). UI: **Feeds**, **Weather**, **Fleet probe**, **Redirects**, **OPML**; sidebar collapses and state is saved in `localStorage`.

---

## Config

| Env | Default | Description |
|-----|---------|-------------|
| `GLANCE_MCP_HOST` | `127.0.0.1` | Bind address |
| `GLANCE_MCP_PORT` | `10776` | FastAPI port |
| `GLANCE_MCP_HTTP_PATH` | `/mcp` | Mount path for streamable MCP |
| `GLANCE_RSS_MAX_BYTES` | `3145728` | Max feed download size |
| `GLANCE_RSS_ALLOW_PRIVATE_HOSTS` | `0` | Set `1` to allow RFC1918/loopback RSS URLs |

---

## Developer

```powershell
uv sync --extra dev
uv run ruff check .
uv run ruff format .
uv run pytest tests -v
```

**Tasks:** `just --list` — `run`/`serve`, `stdio`, `lint`/`check`, `format`/`fmt`, `test`, `install`, `install-web`, `web`/`start`, `clean`, `health`.

**Product notes:** [docs/PRD.md](docs/PRD.md) · **Changelog:** [CHANGELOG.md](CHANGELOG.md).

---

## License

MIT
