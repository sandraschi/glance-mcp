"""Open-Meteo forecast (no API key)."""

from __future__ import annotations

from typing import Any

import httpx

_OPEN_METEO = "https://api.open-meteo.com/v1/forecast"


async def forecast(
    latitude: float,
    longitude: float,
    *,
    timezone: str = "auto",
    current: str = "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
    hourly: str | None = "temperature_2m,precipitation_probability",
    forecast_days: int = 3,
) -> dict[str, Any]:
    """Fetch grid forecast from Open-Meteo public API."""
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return {
            "success": False,
            "error": "latitude must be [-90,90], longitude [-180,180].",
        }
    forecast_days = max(1, min(forecast_days, 16))
    params: dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "forecast_days": forecast_days,
    }
    if current:
        params["current"] = current
    if hourly:
        params["hourly"] = hourly

    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        r = await client.get(_OPEN_METEO, params=params)
    if r.status_code >= 400:
        return {
            "success": False,
            "error": f"Open-Meteo HTTP {r.status_code}",
            "detail": r.text[:2000],
        }
    try:
        data = r.json()
    except Exception as e:
        return {"success": False, "error": f"Invalid JSON: {e}"}
    return {
        "success": True,
        "message": "Open-Meteo forecast retrieved.",
        "latitude": latitude,
        "longitude": longitude,
        "timezone": data.get("timezone"),
        "current": data.get("current"),
        "hourly": data.get("hourly"),
        "daily": data.get("daily"),
        "source": _OPEN_METEO,
    }
