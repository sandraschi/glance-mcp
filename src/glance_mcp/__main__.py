"""CLI: stdio (Cursor) or HTTP (FastAPI + MCP at /mcp)."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys

import uvicorn

from glance_mcp.config import load_settings
from glance_mcp.server import mcp


def _configure_logging(*, debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(message)s", stream=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="glance-mcp (FastMCP 3.1)")
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Run FastAPI on GLANCE_MCP_HOST:GLANCE_MCP_PORT with MCP mounted",
    )
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="MCP over stdio (default when --serve is not passed)",
    )
    parser.add_argument("--debug", action="store_true", help="Verbose logs (stderr)")
    args = parser.parse_args()
    _configure_logging(debug=args.debug)

    transport = os.getenv("MCP_TRANSPORT", "").lower()
    use_http = args.serve or transport in {"http", "streamable"}

    if use_http and args.stdio:
        parser.error("Choose either --serve or --stdio, not both.")

    settings = load_settings()

    if use_http:
        uvicorn.run(
            "glance_mcp.app:app",
            host=settings.host,
            port=settings.port,
            log_level="debug" if args.debug else "info",
        )
        return

    asyncio.run(mcp.run_stdio_async())


if __name__ == "__main__":
    main()
