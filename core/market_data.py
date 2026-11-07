import os
import requests
from datetime import datetime, timezone


def get_candles(symbol="EUR/USD", interval="1min", limit=100):
    api_key = os.getenv("AASHIS_API_KEY")

    if not api_key:
        raise RuntimeError("Twelve Data API key not set")

    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": limit,
        "order": "ASC",
        "apikey": api_key
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    if data.get("status") == "error" or "values" not in data:
        raise RuntimeError(data.get("message", "Market data unavailable"))

    candles = []
    for item in data["values"]:
        candles.append({
            "time": item["datetime"],
            "open": float(item["open"]),
            "high": float(item["high"]),
            "low": float(item["low"]),
            "close": float(item["close"])
        })

    # अन्तिम candle पूरा बन्द भएको नहुन सक्छ।
    if candles:
        last_time = datetime.strptime(
            candles[-1]["time"], "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        if (now - last_time).total_seconds() < 60:
            candles.pop()

    return candles
