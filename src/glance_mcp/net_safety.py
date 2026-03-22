"""Host / IP checks before outbound HTTP (SSRF hardening for local single-user servers)."""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, urlunparse

_BLOCKED_HOSTNAMES = frozenset(
    {
        "metadata.google.internal",
        "metadata.google.internal.",
    }
)

_METADATA_IPV4 = ipaddress.ip_address("169.254.169.254")


def _is_metadata_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    if ip.version == 4:
        return ip == _METADATA_IPV4
    return False


def resolve_first_ip(host: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
    """Resolve hostname to first address."""
    infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    for _fam, _type, _proto, _canon, sockaddr in infos:
        if len(sockaddr) >= 1:
            raw = sockaddr[0]
            return ipaddress.ip_address(raw)
    raise ValueError(f"Could not resolve host: {host!r}")


def assert_http_https(url: str) -> None:
    p = urlparse(url)
    if p.scheme not in {"http", "https"}:
        raise ValueError("Only http and https URLs are allowed.")


def assert_safe_for_rss(url: str, *, allow_private_hosts: bool) -> None:
    """RSS feed fetch: block cloud metadata; optionally block RFC1918/loopback."""
    assert_http_https(url)
    p = urlparse(url)
    host = (p.hostname or "").lower().strip()
    if not host or host in _BLOCKED_HOSTNAMES:
        raise ValueError("Blocked hostname.")
    ip = resolve_first_ip(host)
    if _is_metadata_ip(ip):
        raise ValueError("Blocked metadata IP.")
    if allow_private_hosts:
        return
    if ip.is_private or ip.is_loopback or ip.is_link_local:
        raise ValueError(
            "RSS URL resolves to private, loopback, or link-local; "
            "set GLANCE_RSS_ALLOW_PRIVATE_HOSTS=1 for LAN/dev feeds."
        )


def assert_safe_for_probe(url: str) -> None:
    """Health probe: allow loopback + LAN + public; block metadata endpoints only."""
    assert_http_https(url)
    p = urlparse(url)
    host = (p.hostname or "").lower().strip()
    if not host or host in _BLOCKED_HOSTNAMES:
        raise ValueError("Blocked hostname.")
    ip = resolve_first_ip(host)
    if _is_metadata_ip(ip):
        raise ValueError("Blocked metadata IP (169.254.169.254).")


def normalize_url(url: str) -> str:
    """Strip fragments; ensure parseable."""
    p = urlparse(url.strip())
    if not p.scheme or not p.netloc:
        raise ValueError("Invalid URL.")
    return urlunparse(
        (
            p.scheme,
            p.netloc,
            p.path or "/",
            p.params,
            p.query,
            "",
        )
    )
