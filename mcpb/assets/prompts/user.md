# glance-mcp User Guide

A comprehensive set of development utilities and data-gathering tools: RSS/Atom feed fetching, Open-Meteo weather forecasts (no API key), parallel HTTP health probes for fleet monitoring, redirect chain tracing, OPML feed list parsing, UUID generation, text hashing, base64 encode/decode, JSON validation/formatting/minification, JWT token decoding, URL encoding/decoding, text statistics, UNIX timestamp conversion, and random value generation.

No API keys are required for any tool. Everything works out of the box.

## Table of Contents

1. Installation
2. Tutorials (13 walkthroughs)
3. REST API Reference
4. Configuration Reference
5. Troubleshooting
6. FAQ

---

## Installation

### Prerequisites
- Python 3.11 or higher
- `uv` package manager

### Quick Start (3 commands)

```bash
# Clone the repository
git clone https://github.com/sandraschi/glance-mcp.git
cd glance-mcp

# Install all dependencies with uv
uv sync

# Run in stdio mode (default — for Cursor, Claude Desktop)
uv run python -m glance_mcp
```

### HTTP Mode (for REST API access)

```bash
uv run python -m glance_mcp --serve
# Server starts at http://127.0.0.1:10776
# MCP streamable HTTP port at /mcp
# Health check at /health
# Swagger UI at /docs
```

### MCPB Bundle Installation

```bash
mcpb install glance-mcp-v0.2.0.mcpb
```

### Verifying Installation

```bash
# Check that the server starts and tools are registered
uv run python -c "import glance_mcp; print('OK')"

# Test in HTTP mode
uv run python -m glance_mcp --serve &
sleep 2
curl http://127.0.0.1:10776/health
```

## Tutorials

### Tutorial 1: Fetch RSS/Atom Feeds

Get the latest headlines from Hacker News:

```
rss_fetch_feed(feed_url="https://news.ycombinator.com/rss", max_items=5)
```

The response includes the feed title, each story's title, link, published date, and summary. Use this to monitor news, blogs, podcasts, and GitHub release feeds without needing any API keys.

**Pro tip**: Chain this with other MCP tools. For example, use the response from `rss_fetch_feed` as input to `browser-mcp`'s `browse_items` for deep article reading.

### Tutorial 2: Check Weather Forecast

Get a multi-day weather forecast for any location:

```
open_meteo_forecast(latitude=48.2, longitude=16.37, forecast_days=5)
```

This fetches current conditions (temperature, humidity, weather code, wind speed), hourly forecasts, and daily summaries from the Open-Meteo API. No API key needed — Open-Meteo is a free, open-source service.

**Pro tip**: The `weather_code` field uses WMO weather codes. Code 0 = clear, 1-3 = partly cloudy, 45-48 = foggy, 51-57 = drizzle, 61-67 = rain, 71-77 = snow, 95-99 = thunderstorm.

### Tutorial 3: Fleet Health Dashboard

Check if multiple MCP servers are running simultaneously:

```
fleet_http_probe(
  urls=[
    "http://127.0.0.1:10746/health",
    "http://127.0.0.1:10776/health",
    "http://127.0.0.1:10780/health"
  ],
  timeout_seconds=3.0
)
```

Each URL is probed in parallel up to `max_concurrency` (default 12). Results include HTTP status code, response time in milliseconds, content length, and a preview of the response body. Failed probes include the error message.

### Tutorial 4: Trace URL Redirects

See every hop in a redirect chain:

```
http_redirect_trace(url="https://tinyurl.com/example", method="head")
```

This follows each redirect individually, recording the URL, status code, and Location header at each hop. Use this to debug shortened URLs, CDN redirects, or multi-step redirect chains. Start with HEAD (lighter), switch to GET if the server returns 405.

### Tutorial 5: Parse OPML Feed Subscriptions

Import an OPML file exported from Feedly, Inoreader, or any RSS reader:

```
opml_list_feeds(opml_xml="""<?xml version="1.0"?>
<opml version="2.0">
  <head><title>My Feeds</title></head>
  <body>
    <outline text="Technology">
      <outline text="HN" type="rss" xmlUrl="https://news.ycombinator.com/rss" htmlUrl="https://news.ycombinator.com/"/>
      <outline text="Ars Technica" type="rss" xmlUrl="https://feeds.arstechnica.com/arstechnica/index"/>
    </outline>
    <outline text="News">
      <outline text="NYT" type="rss" xmlUrl="https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"/>
    </outline>
  </body>
</opml>""")
```

The tool parses the OPML safely (defusedxml) and returns all outlines that have an `xmlUrl` attribute, preserving the hierarchy where possible. Use the returned feeds as input to `rss_fetch_feed`.

### Tutorial 6: Generate UUIDs

```
# Random UUID (v4) — suitable for most use cases
generate_uuid(version=4)

# Time-ordered UUID (v7) — sortable by creation time
generate_uuid(version=7)
```

Both return the UUID string, hex representation, and URN format. UUID v7 is useful for database primary keys as the values are monotonically increasing.

### Tutorial 7: Hash Strings

```
# SHA-256 (default) — recommended for most use cases
hash_text(text="my_password", algorithm="sha256")

# MD5 — useful for checksums, but not cryptographically secure
hash_text(text="large_file_content", algorithm="md5")

# SHA-512 — strongest built-in option
hash_text(text="sensitive_data", algorithm="sha512")
```

### Tutorial 8: Encode/Decode Base64

```
# Encode credentials for HTTP Basic Auth
base64_encode(text="username:password")

# Decode the result
base64_decode(encoded="dXNlcm5hbWU6cGFzc3dvcmQ=")
```

### Tutorial 9: JSON Operations

Validate, format, and minify JSON strings:

```
# Validate — checks if the JSON is syntactically correct
json_tool(text='{"key": "value", "nested": {"a": 1}}', operation="validate")

# Format — pretty-prints with indentation
json_tool(text='{"key":"value","nested":{"a":1}}', operation="format")

# Minify — removes all whitespace
json_tool(text='{\n  "key": "value"\n}', operation="minify")
```

### Tutorial 10: Decode JWT Tokens

Inspect the header and payload of a JWT without signature verification:

```
jwt_decode(token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3j3gJg5s5gQ7v_dr7w")
```

Returns the decoded header (algorithm, type), payload (claims), and a truncated signature preview.

### Tutorial 11: URL Encode/Decode

```
# Encode special characters for URL parameters
url_encode(text="search query with spaces & symbols")

# Decode percent-encoded strings back to readable text
url_decode(encoded="search+query+with+spaces+%26+symbols")
```

### Tutorial 12: Text Analysis

Get detailed text statistics:

```
text_stats(text="The quick brown fox jumps over the lazy dog. It was a dark and stormy night!")
```

Returns character count, character count without spaces, word count, line count, sentence count, and UTF-8 byte count.

### Tutorial 13: Timestamps and Random Values

```
# Current time breakdown
timestamp_info()

# Specific UNIX timestamp
timestamp_info(timestamp=1718000000)

# Random password
random_value(kind="password", length=20)

# Random integer in range
random_value(kind="int", min_val=1, max_val=100)

# Random hex string
random_value(kind="hex", length=32)
```

## REST API Reference

In HTTP mode, all tools are accessible via FastAPI REST endpoints:

| Endpoint | Method | Tool | Request Body |
|----------|--------|------|-------------|
| `/health` | GET | Health check | — |
| `/` | GET | Service info | — |
| `/api/rss/fetch` | POST | `rss_fetch_feed` | `{"feed_url": "...", "max_items": 25}` |
| `/api/weather/forecast` | POST | `open_meteo_forecast` | `{"latitude": 48.2, "longitude": 16.37, "forecast_days": 3}` |
| `/api/probe` | POST | `fleet_http_probe` | `{"urls": [...], "timeout_seconds": 5.0, "max_concurrency": 12}` |
| `/api/resolve/trace` | POST | `http_redirect_trace` | `{"url": "...", "max_hops": 15, "method": "head"}` |
| `/api/opml/feeds` | POST | `opml_list_feeds` | `{"opml_xml": "..."}` |
| `/api/uuid` | GET | `generate_uuid` | Query: `version=4` |
| `/api/hash` | POST | `hash_text` | Query: `text`, `algorithm` |
| `/api/base64/encode` | POST | `base64_encode` | Query: `text` |
| `/api/base64/decode` | POST | `base64_decode` | Query: `encoded` |
| `/api/json` | POST | `json_tool` | Query: `text`, `operation` |
| `/api/jwt/decode` | GET | `jwt_decode` | Query: `token` |
| `/api/time` | GET | `timestamp_info` | Query: `timestamp` (optional) |

## HTTP Mode Deployment Guide

Running glance-mcp in HTTP mode enables programmatic REST access, CI/CD integration, and webhook-friendly endpoints.

### Starting the HTTP Server

```bash
# Default: port 10776, bind 127.0.0.1
uv run python -m glance_mcp --serve

# Custom port via environment
$env:GLANCE_MCP_PORT=10999; uv run python -m glance_mcp --serve

# From any directory
uv run --directory /path/to/glance-mcp python -m glance_mcp --serve
```

### Verifying the Server

```bash
# Health check
curl http://127.0.0.1:10776/health

# Service info
curl http://127.0.0.1:10776/

# Swagger UI (interactive API docs)
# Open http://127.0.0.1:10776/docs in a browser
```

### Example REST Calls

```bash
# Fetch an RSS feed
curl -X POST http://127.0.0.1:10776/api/rss/fetch \
  -H "Content-Type: application/json" \
  -d '{"feed_url": "https://news.ycombinator.com/rss", "max_items": 3}'

# Get weather
curl -X POST http://127.0.0.1:10776/api/weather/forecast \
  -H "Content-Type: application/json" \
  -d '{"latitude": 48.2, "longitude": 16.37, "forecast_days": 3}'

# Generate UUID
curl "http://127.0.0.1:10776/api/uuid?version=4"

# Probe endpoints
curl -X POST http://127.0.0.1:10776/api/probe \
  -H "Content-Type: application/json" \
  -d '{"urls": ["http://127.0.0.1:10776/health"], "timeout_seconds": 3}'
```

## CI/CD Integration Examples

### GitHub Actions — RSS Monitor

```yaml
name: Monitor RSS
on:
  schedule:
    - cron: '0 6 * * *'
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install uv
      - run: uv sync
      - run: |
          uv run python -c "
          import asyncio
          from glance_mcp.services.rss import fetch_feed
          result = asyncio.run(fetch_feed('https://news.ycombinator.com/rss'))
          print(f'Feed: {result[\"feed_title\"]} — {len(result[\"entries\"])} entries')
          "
```

### GitLab CI — Weather Check

```yaml
weather-check:
  script:
    - uv sync
    - uv run python -c "
      import asyncio
      from glance_mcp.services.weather import forecast
      r = asyncio.run(forecast(48.2, 16.37, forecast_days=3))
      print(r['current']['temperature_2m'])
      "
```

## Fleet Monitoring Dashboard Example

Run a comprehensive health check of all MCP fleet servers:

```
fleet_http_probe(
  urls=[
    "http://127.0.0.1:10746/health",  # autohotkey-mcp
    "http://127.0.0.1:10776/health",  # glance-mcp itself
    "http://127.0.0.1:10780/health",  # browser-mcp
    "http://127.0.0.1:10968/health",  # kick-mcp
    "http://127.0.0.1:10740/health",  # plex-mcp
    "http://127.0.0.1:10812/health",  # email-mcp backend
    "http://127.0.0.1:10813/health",  # calibre-mcp
    "http://127.0.0.1:10818/health",  # obs-mcp
  ],
  timeout_seconds=2.0,
  max_concurrency=8
)
```

## MCP Tool Chaining

glance-mcp integrates naturally with other MCP servers:

- **browser-mcp**: Use `rss_fetch_feed` to find article links, then `browser-mcp.browse_items` to deep-read each
- **aiwatcher-mcp**: Use `rss_fetch_feed` results as feed sources, then `aiwatcher-mcp.poll_feeds` for ongoing monitoring
- **gitops-mcp**: Use `fleet_http_probe` to check if webapp endpoints are live before running git operations
- **notifications-mcp**: Use `open_meteo_forecast` to get weather data, then notify via email/speech

## Performance Tuning

### RSS Fetch Performance

- Reduce `max_items` for faster responses (fewer entries to process)
- Set `GLANCE_RSS_MAX_BYTES` lower for feeds known to be small
- Use LAN-feeds with `GLANCE_RSS_ALLOW_PRIVATE_HOSTS=1` for intranet RSS sources
- The default User-Agent identifies as glance-mcp — feeds may rate-limit unknown agents

### Fleet Probe Performance

- Use lower `timeout_seconds` (1-2s) for localhost probes that should respond quickly
- Use higher `timeout_seconds` (10-30s) for probes to remote or slow services
- `max_concurrency` controls how many URLs are checked in parallel — default 12 is good for most setups
- Probe results include `elapsed_ms` — use this to identify slow services

## Security and Privacy

- **No data is collected**: glance-mcp makes no telemetry or analytics calls
- **No API keys stored**: The server has no API keys to leak
- **RSS privacy**: RSS feed URLs are sent directly to the feed server — use public HTTPS feeds
- **Weather privacy**: Your coordinates are sent to Open-Meteo for the forecast
- **Probe privacy**: Probing URLs from your local network may expose internal services
- **OPML privacy**: OPML files may contain subscription lists revealing personal interests — they are processed locally and discarded

## Integration with Open-Meteo

Open-Meteo is a free, open-source weather API that provides high-resolution forecasts for any location on Earth. Key features:
- No API key required
- No rate limits on non-commercial use
- Covers the entire globe with ~11km grid resolution
- Hourly and daily forecasts up to 16 days
- Includes WMO weather codes, temperature, precipitation, wind, humidity

The API is called at `https://api.open-meteo.com/v1/forecast` with standard HTTP GET. Response data is returned as-is from Open-Meteo without additional processing.

## FAQ — Extended Answers

**Q: What is the WMO weather code?**
A: The `weather_code` field in the forecast response uses World Meteorological Organization codes:
- 0: Clear sky
- 1-3: Mainly clear, partly cloudy, overcast
- 45-48: Foggy
- 51-57: Drizzle
- 61-67: Rain
- 71-77: Snow
- 80-82: Rain showers
- 85-86: Snow showers
- 95: Thunderstorm
- 96-99: Thunderstorm with hail

**Q: Can I use glance-mcp to monitor my own APIs?**
A: Yes. Use `fleet_http_probe` with URLs pointing to your API endpoints. The tool supports any HTTP(S) URL including localhost and LAN. Results include status codes, response times, and body previews.

**Q: How does the RSS size cap work?**
A: The feed XML is downloaded with streaming — content is accumulated in memory until the cap (default 3MB) is reached. If the cap is exceeded, an error is returned and any partially downloaded data is discarded. This prevents out-of-memory situations with huge feeds.

**Q: What is the URL safety check for RSS?**
A: By default, RSS feeds must resolve to public IP addresses (not private, loopback, or link-local). This prevents accidental SSRF. Set `GLANCE_RSS_ALLOW_PRIVATE_HOSTS=1` to allow LAN feeds. Cloud metadata endpoints (169.254.169.254) are always blocked regardless of this setting.

**Q: Can I use generic hash algorithms?**
A: Supported algorithms: `md5`, `sha1`, `sha256`, `sha512`. MD5 and SHA1 are provided for legacy compatibility — they are cryptographically broken and should not be used for security-sensitive hashing. SHA256 is the recommended default.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GLANCE_MCP_HOST` | `127.0.0.1` | HTTP bind address |
| `GLANCE_MCP_PORT` | `10776` | HTTP port |
| `GLANCE_MCP_HTTP_PATH` | `/mcp` | MCP mount path |
| `GLANCE_RSS_MAX_BYTES` | `3145728` (3MB) | Max RSS feed size |
| `GLANCE_RSS_ALLOW_PRIVATE_HOSTS` | `false` | Allow LAN RSS feeds |
| `MCP_TRANSPORT` | `stdio` | Transport mode |
| `MCP_BRIDGE_URLS` | (empty) | MCP proxy URLs |

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| RSS feed returns "blocked hostname" | Private IP blocked | Set `GLANCE_RSS_ALLOW_PRIVATE_HOSTS=1` |
| RSS feed exceeds size cap | Feed too large (default 3MB) | Increase `GLANCE_RSS_MAX_BYTES` |
| Weather "invalid coordinates" | Lat/lon out of range | Latitude must be [-90, 90], longitude [-180, 180] |
| Fleet probe "empty" | No URLs provided | Pass at least one URL |
| Fleet probe "Max 64 URLs" | Too many URLs in one call | Split into batches |
| Redirect trace "invalid method" | Wrong method string | Must be "head" or "get" |
| OPML "Invalid XML" | Malformed OPML input | Validate OPML before calling |
| Base64 decode error | Corrupted base64 string | Input must be valid base64 |
| JWT "invalid format" | Not a valid JWT | Must have exactly 3 dot-separated sections |
| JSON tool parse error | Malformed JSON | Validate on jsonlint.com first |
| Random "unknown kind" | Invalid kind string | Use: uuid, hex, password, int, float |

## FAQ

**Q: Do I need any API keys for glance-mcp?**
A: No. Open-Meteo weather forecasts are free with no API key. RSS/Atom feeds are public by nature. All utility functions use the Python standard library. There are zero paid dependencies.

**Q: Why can't I fetch an RSS feed from my internal server?**
A: By default, glance-mcp blocks RSS requests to private/localhost IPs for security. Set `GLANCE_RSS_ALLOW_PRIVATE_HOSTS=1` to enable LAN RSS fetching.

**Q: What IPs are always blocked?**
A: Cloud metadata endpoints (169.254.169.254) and blocked hostnames (metadata.google.internal) are always blocked in all network tools to prevent SSRF.

**Q: Can I run glance-mcp in CI/CD pipelines?**
A: Yes. Use HTTP mode (`--serve`) in your CI environment. All tools work without any network access except the explicitly called RSS/weather/probe URLs.

**Q: What is the maximum number of URLs I can probe at once?**
A: 64 URLs per call. For larger fleets, split into multiple calls.

**Q: Does JWT decode verify the signature?**
A: No. glance-mcp only decodes the header and payload (base64 sections). The signature is truncated and returned for inspection only. Use a dedicated JWT library for verification.

**Q: What encoding does the base64 tool use?**
A: Standard base64 (RFC 4648), not modified for URLs. Use url_encode for URL-safe encoding.

**Q: Can I use glance-mcp to monitor websites?**
A: Not directly — glance-mcp has no scheduled polling. But you can use `rss_fetch_feed` for sites with feeds and `fleet_http_probe` for health checks on demand.
