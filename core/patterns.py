def candle_info(c):
    o, h, l, close = map(float, (c["open"], c["high"], c["low"], c["close"]))
    size = max(h - l, 1e-12)
    body = abs(close - o)
    upper = h - max(o, close)
    lower = min(o, close) - l
    return {
        "bull": close > o,
        "bear": close < o,
        "body": body / size,
        "upper": upper / size,
        "lower": lower / size,
        "range": size,
    }


def detect_patterns(candles):
    if len(candles) < 3:
        return []

    a, b, c = candles[-3:]
    A, B, C = map(candle_info, (a, b, c))
    patterns = []

    # Single-candle patterns
    if C["body"] <= 0.10:
        patterns.append(("Doji", "neutral"))
    if C["lower"] >= 0.60 and C["body"] <= 0.35 and C["upper"] <= 0.15:
        patterns.append(("Hammer", "bullish"))
    if C["upper"] >= 0.60 and C["body"] <= 0.35 and C["lower"] <= 0.15:
        patterns.append(("Shooting Star", "bearish"))
    if C["body"] >= 0.85:
        patterns.append(("Marubozu Bullish" if C["bull"] else "Marubozu Bearish", "bullish" if C["bull"] else "bearish"))

    # Two-candle patterns
    if B["bear"] and C["bull"] and c["open"] <= b["close"] and c["close"] >= b["open"]:
        patterns.append(("Bullish Engulfing", "bullish"))
    if B["bull"] and C["bear"] and c["open"] >= b["close"] and c["close"] <= b["open"]:
        patterns.append(("Bearish Engulfing", "bearish"))

    # Three-candle patterns
    if A["bear"] and B["body"] < 0.35 and C["bull"] and c["close"] > (a["open"] + a["close"]) / 2:
        patterns.append(("Morning Star", "bullish"))
    if A["bull"] and B["body"] < 0.35 and C["bear"] and c["close"] < (a["open"] + a["close"]) / 2:
        patterns.append(("Evening Star", "bearish"))

    return patterns
