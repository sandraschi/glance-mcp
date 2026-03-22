"""Weather response shape (offline)."""

import asyncio

from glance_mcp.services.weather import forecast


def test_forecast_rejects_bad_lat() -> None:
    r = asyncio.run(forecast(100.0, 0.0))
    assert r["success"] is False
