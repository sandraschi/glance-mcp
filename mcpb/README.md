# glance-mcp (MCPB Bundle)

FastMCP 3.1: RSS/Atom feeds, Open-Meteo weather (no API key), and HTTP health probes for local fleet — minimal keys, httpx + feedparser.

## Usage

Add to \claude_desktop_config.json\:
\\\json
{
  "mcpServers": {
    "glance-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "\D:\Dev\repos", "python", "-m", "glance_mcp"],
      "env": { "PYTHONPATH": "\D:\Dev\repos/src" }
    }
  }
}
\\\

## Tools

- **health**: health
- **root**: root
- **api_rss**: api_rss
- **api_weather**: api_weather
- **api_probe**: api_probe
- **api_resolve**: api_resolve
- **api_opml**: api_opml
- **api_uuid**: api_uuid
- **api_hash**: api_hash
- **api_b64encode**: api_b64encode
- **api_b64decode**: api_b64decode
- **api_json**: api_json
- **api_jwt_decode**: api_jwt_decode
- **api_time**: api_time
- **build_app_head**: build_app(head)
- **build_app_get**: build_app(get)
- **rss_fetch_feed**: rss_fetch_feed
- **open_meteo_forecast**: open_meteo_forecast
- **fleet_http_probe**: fleet_http_probe
- **http_redirect_trace**: http_redirect_trace
- **opml_list_feeds**: opml_list_feeds
- **generate_uuid**: generate_uuid
- **hash_text**: hash_text
- **base64_encode**: base64_encode
- **base64_decode**: base64_decode
- **json_tool**: json_tool
- **jwt_decode**: jwt_decode
- **url_encode**: url_encode
- **url_decode**: url_decode
- **text_stats**: text_stats
- **timestamp_info**: timestamp_info
- **random_value**: random_value

## Requirements

- Python 3.12+
- uv
