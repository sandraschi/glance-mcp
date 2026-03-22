"""URL safety rules."""

import pytest

from glance_mcp.net_safety import assert_http_https, assert_safe_for_probe, assert_safe_for_rss


def test_assert_http_https_rejects_ftp() -> None:
    with pytest.raises(ValueError, match="Only http"):
        assert_http_https("ftp://example.com/feed")


def test_rss_blocks_loopback_by_default() -> None:
    with pytest.raises(ValueError, match="private|loopback"):
        assert_safe_for_rss("https://127.0.0.1/feed.xml", allow_private_hosts=False)


def test_probe_allows_localhost() -> None:
    assert_safe_for_probe("http://127.0.0.1:10776/health")


def test_probe_blocks_metadata_ip() -> None:
    with pytest.raises(ValueError, match="metadata|Blocked"):
        assert_safe_for_probe("http://169.254.169.254/latest/meta-data/")
