# Example Atom/RSS feeds (curated)

Use these with **`rss_fetch_feed`** or the **web_sota** Feeds tab. Third-party URLs can change; if a fetch fails, open the site and look for “Atom”, “RSS”, or “Subscribe”.

| Feed | URL | Notes |
|------|-----|--------|
| **Simon Willison** (default demo) | `https://simonwillison.net/atom/everything/` | Full blog; not Hacker News — HN is a separate site. Open in a reader (not raw XML): [Feedly](https://feedly.com/i/subscription/feed/https%3A%2F%2Fsimonwillison.net%2Fatom%2Feverything%2F) · [Inoreader](https://www.inoreader.com/feed/https%3A%2F%2Fsimonwillison.net%2Fatom%2Feverything%2F). |
| **Bruce Schneier** | `https://www.schneier.com/feed/` | Security and policy. |
| Julia Evans | `https://jvns.ca/atom.xml` | Systems, zines. |
| Dan Luu | `https://danluu.com/atom.xml` | Performance, eng. |
| rachel by the bay | `https://rachelbythebay.com/w/feed` | Systems essays. |
| The Pragmatic Engineer | `https://blog.pragmaticengineer.com/rss/` | Industry / Big Tech. |
| Krebs on Security | `https://krebsonsecurity.com/feed/` | Cybercrime reporting. |
| Martin Fowler | `https://martinfowler.com/feed.atom` | Architecture. |
| **Hacker News** (aggregator) | `https://hnrss.org/frontpage` | Links from the front page — **not** a personal blog. |

Simon’s writing often **appears on** HN when someone submits it; the **canonical blog feed** is still `simonwillison.net`, not `news.ycombinator.com`.

## Browsers vs readers

Pasting a feed URL into the address bar usually shows **XML**, not a readable article list. Use **Feedly**, **Inoreader**, **NetNewsWire**, etc., or the glance-mcp **Feeds** tab, which fetches and lists entries.

For any feed URL, Feedly subscribe: `https://feedly.com/i/subscription/feed/` + URL-encoded feed URL. Example (Simon): `https://feedly.com/i/subscription/feed/https%3A%2F%2Fsimonwillison.net%2Fatom%2Feverything%2F`.

The **web_sota** Feeds panel also includes **Feedly** and **Inoreader** links derived from the feed URL you have in the field.
