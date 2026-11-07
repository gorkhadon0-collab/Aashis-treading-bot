def validate_candle(candle):
    required = ("open", "high", "low", "close")

    if not all(key in candle for key in required):
        return False

    try:
        o, h, l, c = [float(candle[key]) for key in required]
    except (TypeError, ValueError):
        return False

    if not all(map(lambda x: x == x and abs(x) != float("inf"), (o, h, l, c))):
        return False

    return l <= min(o, c) and h >= max(o, c) and h > l


def analyze_candle(candle):
    if not validate_candle(candle):
        raise ValueError("Invalid candle data")

    o = float(candle["open"])
    h = float(candle["high"])
    l = float(candle["low"])
    c = float(candle["close"])

    total_range = h - l
    body = abs(c - o)
    upper_wick = h - max(o, c)
    lower_wick = min(o, c) - l

    return {
        "direction": "BULLISH" if c > o else "BEARISH" if c < o else "DOJI",
        "body": body,
        "body_ratio": body / total_range,
        "upper_wick": upper_wick,
        "lower_wick": lower_wick,
        "upper_wick_ratio": upper_wick / total_range,
        "lower_wick_ratio": lower_wick / total_range,
        "range": total_range,
        "close_position": (c - l) / total_range
    }


def analyze_candles(candles):
    return [analyze_candle(candle) for candle in candles if validate_candle(candle)]
