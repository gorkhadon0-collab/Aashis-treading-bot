from core.candles import analyze_candle


def detect_patterns(candles):
    if len(candles) < 3:
        return []

    a, b, c = candles[-3:]
    A, B, C = map(analyze_candle, (a, b, c))
    patterns = []

    # Single candle patterns
    if C["body_ratio"] <= 0.10:
        patterns.append(("Doji", "neutral"))

    if (C["lower_wick_ratio"] >= 0.60
            and C["body_ratio"] <= 0.35
            and C["upper_wick_ratio"] <= 0.15):
        patterns.append(("Hammer", "bullish"))

    if (C["upper_wick_ratio"] >= 0.60
            and C["body_ratio"] <= 0.35
            and C["lower_wick_ratio"] <= 0.15):
        patterns.append(("Shooting Star", "bearish"))

    if C["body_ratio"] >= 0.85:
        direction = C["direction"]
        if direction != "DOJI":
            patterns.append((
                "Marubozu " + direction.title(),
                direction.lower()
            ))

    # Two candle patterns
    if (B["direction"] == "BEARISH"
            and C["direction"] == "BULLISH"
            and float(c["open"]) <= float(b["close"])
            and float(c["close"]) >= float(b["open"])):
        patterns.append(("Bullish Engulfing", "bullish"))

    if (B["direction"] == "BULLISH"
            and C["direction"] == "BEARISH"
            and float(c["open"]) >= float(b["close"])
            and float(c["close"]) <= float(b["open"])):
        patterns.append(("Bearish Engulfing", "bearish"))

    # Three candle patterns
    midpoint_a = (
        float(a["open"]) + float(a["close"])
    ) / 2

    if (A["direction"] == "BEARISH"
            and B["body_ratio"] < 0.35
            and C["direction"] == "BULLISH"
            and float(c["close"]) > midpoint_a):
        patterns.append(("Morning Star", "bullish"))

    if (A["direction"] == "BULLISH"
            and B["body_ratio"] < 0.35
            and C["direction"] == "BEARISH"
            and float(c["close"]) < midpoint_a):
        patterns.append(("Evening Star", "bearish"))

    return patterns
