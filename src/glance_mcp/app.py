"""FastAPI: health + optional REST mirrors + FastMCP streamable HTTP."""

from __future__ import annotations

from typing import Any, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from glance_mcp.config import load_settings
from glance_mcp.server import mcp
from glance_mcp.services import opml, probe, resolve, rss, weather

mcp_http = mcp.http_app(path="/mcp")


class RssBody(BaseModel):
    feed_url: str = Field(..., min_length=8)
    max_items: int = Field(25, ge=1, le=100)


class ProbeBody(BaseModel):
    urls: list[str] = Field(..., min_length=1, max_length=64)
    timeout_seconds: float = Field(5.0, ge=0.5, le=60.0)
    max_concurrency: int = Field(12, ge=1, le=32)


class WeatherBody(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timezone: str = "auto"
    forecast_days: int = Field(3, ge=1, le=16)


class ResolveBody(BaseModel):
    url: str = Field(..., min_length=8)
    max_hops: int = Field(15, ge=1, le=30)
    timeout_seconds: float = Field(20.0, ge=1.0, le=60.0)
    method: Literal["head", "get"] = "head"


class OpmlBody(BaseModel):
    opml_xml: str = Field(..., min_length=10)


def build_app() -> FastAPI:
    settings = load_settings()
    app = FastAPI(
        title="glance-mcp",
        version="0.2.0",
        lifespan=mcp_http.lifespan,
    )

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "ok": True,
            "service": "glance-mcp",
            "port": settings.port,
            "mcp_http": f"http://{settings.host}:{settings.port}{settings.mcp_http_path}",
        }

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {
            "service": "glance-mcp",
            "version": "0.2.0",
            "docs": f"http://{settings.host}:{settings.port}/docs",
            "mcp_http": f"http://{settings.host}:{settings.port}{settings.mcp_http_path}",
            "webapp": "http://127.0.0.1:10777",
        }

    @app.post("/api/rss/fetch")
    async def api_rss(body: RssBody) -> dict[str, Any]:
        return await rss.fetch_feed(body.feed_url, max_items=body.max_items)

    @app.post("/api/weather/forecast")
    async def api_weather(body: WeatherBody) -> dict[str, Any]:
        return await weather.forecast(
            body.latitude,
            body.longitude,
            timezone=body.timezone,
            forecast_days=body.forecast_days,
        )

    @app.post("/api/probe")
    async def api_probe(body: ProbeBody) -> dict[str, Any]:
        return await probe.probe_many(
            body.urls,
            timeout_s=body.timeout_seconds,
            max_concurrency=body.max_concurrency,
        )

    @app.post("/api/resolve/trace")
    async def api_resolve(body: ResolveBody) -> dict[str, Any]:
        return await resolve.trace_redirects(
            body.url,
            max_hops=body.max_hops,
            timeout_s=body.timeout_seconds,
            method=body.method.lower(),
        )

    @app.post("/api/opml/feeds")
    async def api_opml(body: OpmlBody) -> dict[str, Any]:
        return opml.list_feeds_from_opml(body.opml_xml)

    path = settings.mcp_http_path.strip() or "/mcp"
    app.mount(path, mcp_http)

    return app


app = build_app()
