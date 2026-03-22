"""Environment-driven settings."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _b(name: str, default: bool = False) -> bool:
    v = os.getenv(name, "").strip().lower()
    if v in {"1", "true", "yes", "on"}:
        return True
    if v in {"0", "false", "no", "off"}:
        return False
    return default


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    mcp_http_path: str
    rss_max_bytes: int
    rss_allow_private_hosts: bool

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            host=os.getenv("GLANCE_MCP_HOST", "127.0.0.1"),
            port=int(os.getenv("GLANCE_MCP_PORT", "10776")),
            mcp_http_path=os.getenv("GLANCE_MCP_HTTP_PATH", "/mcp"),
            rss_max_bytes=int(os.getenv("GLANCE_RSS_MAX_BYTES", str(3 * 1024 * 1024))),
            rss_allow_private_hosts=_b("GLANCE_RSS_ALLOW_PRIVATE_HOSTS", False),
        )


def load_settings() -> Settings:
    return Settings.from_env()
