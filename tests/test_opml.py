"""OPML parsing."""

from glance_mcp.services.opml import list_feeds_from_opml


def test_opml_extracts_xmlurl() -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <head><title>Test</title></head>
  <body>
    <outline text="Ex" title="Example" type="rss"
      xmlUrl="https://example.com/feed.xml" htmlUrl="https://example.com/"/>
  </body>
</opml>"""
    r = list_feeds_from_opml(xml)
    assert r["success"] is True
    assert len(r["feeds"]) == 1
    assert r["feeds"][0]["xmlUrl"] == "https://example.com/feed.xml"
    assert r["feeds"][0]["title"] == "Example"


def test_opml_rejects_huge() -> None:
    r = list_feeds_from_opml("x" * (3 * 1024 * 1024))
    assert r["success"] is False
