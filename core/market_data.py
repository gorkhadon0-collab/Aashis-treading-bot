import os
import requests
from datetime import datetime, timezone, timedelta

from core.candles import validate_candle

API_URL = "https://api.twelvedata.com/time_series"

INTERVAL_SECONDS = {
    "1min": 60,
    "5min": 300,
    "15min": 900,
    "30min": 1800,
    "1h": 3600,
    "4h": 14400,
    "1day": 86400,
}


def get_candles(symbol="EUR/USD", interval="1min", limit=100):
    api_key = os.getenv("AASHIS_API_KEY")

    if not api_key:
        raise RuntimeError("AASHIS_API_KEY is not set")

    if interval not in INTERVAL_SECONDS:
        raise ValueError(f"Unsupported interval: {interval}")

    if not isinstance(limit, int) or not 30 <= limit <= 5000:
        raise ValueError("limit must be between 30 and 5000")

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": limit,
        "order": "ASC",
        "timezone": "UTC",
        "apikey": api_key,
    }

    response = requests.get(API_URL, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    if data.get("status") == "error" or "values" not in data:
        message = data.get("message", "Market data unavailable")
        raise RuntimeError(message)

    now = datetime.now(timezone.utc)
    duration = timedelta(seconds=INTERVAL_SECONDS[interval])
    candles_by_time = {}

    for item in data["values"]:
        try:
            timestamp = datetime.fromisoformat(
                item["datetime"].replace("Z", "+00:00")
            )

            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            else:
                timestamp = timestamp.astimezone(timezone.utc)

            candle = {
                "time": timestamp.isoformat(),
                "open": float(item["open"]),
                "high": float(item["high"]),
                "low": float(item["low"]),
                "close": float(item["close"]),
            }

            if not validate_candle(candle):
                continue

            # Do not use a candle until its full interval has closed.
            if timestamp + duration > now:
                continue

            candles_by_time[candle["time"]] = candle

        except (KeyError, TypeError, ValueError):
            continue

    candles = sorted(
        candles_by_time.values(),
        key=lambda candle: candle["time"]
    )

    if len(candles) < 30:
        raise RuntimeError(
            f"Only {len(candles)} valid closed candles received"
        )

    return candles[-limit:]
