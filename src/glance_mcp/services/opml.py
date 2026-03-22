"""OPML outline parsing → feed URLs (defused XML)."""

from __future__ import annotations

from typing import Any

from defusedxml import ElementTree as ET

_MAX_OPML_BYTES = 2 * 1024 * 1024


def list_feeds_from_opml(opml_xml: str) -> dict[str, Any]:
    """Parse OPML 1/2 XML; return outline entries with xmlUrl."""
    raw = opml_xml.encode("utf-8", errors="replace")
    if len(raw) > _MAX_OPML_BYTES:
        return {
            "success": False,
            "error": f"OPML text exceeds {_MAX_OPML_BYTES} bytes.",
            "feeds": [],
        }
    try:
        root = ET.fromstring(raw)
    except Exception as e:
        return {
            "success": False,
            "error": f"Invalid XML: {e}",
            "feeds": [],
        }

    feeds: list[dict[str, str]] = []
    for el in root.iter():
        tag = el.tag.split("}")[-1] if el.tag else ""
        if tag != "outline":
            continue
        xml_url = el.attrib.get("xmlUrl") or el.attrib.get("xmlurl")
        if not xml_url or not xml_url.strip():
            continue
        feeds.append(
            {
                "title": (el.attrib.get("title") or el.attrib.get("text") or "").strip(),
                "xmlUrl": xml_url.strip(),
                "htmlUrl": (el.attrib.get("htmlUrl") or el.attrib.get("htmlurl") or "").strip(),
                "type": (el.attrib.get("type") or "").strip(),
            }
        )

    return {
        "success": True,
        "message": f"Found {len(feeds)} feed outline(s) with xmlUrl.",
        "feeds": feeds,
    }
