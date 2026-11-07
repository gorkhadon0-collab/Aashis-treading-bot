from core.candles import analyze_candle, validate_candle
from core.patterns import detect_patterns


def analyze(candles):
    candles = [c for c in candles if validate_candle(c)]

    if len(candles) < 30:
        return {
            "signal": "WAIT",
            "confidence": 0,
            "bullish_score": 0,
            "bearish_score": 0,
            "score_difference": 0,
            "reason": "Not enough valid candles",
            "patterns": [],
            "trend": "UNKNOWN"
        }

    closes = [float(c["close"]) for c in candles]
    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]

    recent = candles[-30:]
    last = recent[-1]
    info = analyze_candle(last)

    bullish = 0
    bearish = 0
    reasons = []

    # Candle patterns
    patterns = detect_patterns(recent)

    for name, direction in patterns:
        if direction == "bullish":
            bullish += 2
            reasons.append(name)
        elif direction == "bearish":
            bearish += 2
            reasons.append(name)

    # Trend analysis
    short_ma = sum(closes[-5:]) / 5
    long_ma = sum(closes[-20:]) / 20

    if short_ma > long_ma:
        bullish += 2
        trend = "BULLISH"
        reasons.append("Bullish trend")
    elif short_ma < long_ma:
        bearish += 2
        trend = "BEARISH"
        reasons.append("Bearish trend")
    else:
        trend = "SIDEWAYS"

    # Momentum
    if closes[-1] > closes[-4]:
        bullish += 1
        reasons.append("Positive momentum")
    elif closes[-1] < closes[-4]:
        bearish += 1
        reasons.append("Negative momentum")

    # Candle strength
    if info["body_ratio"] >= 0.60:
        if info["direction"] == "BULLISH":
            bullish += 1
        elif info["direction"] == "BEARISH":
            bearish += 1

    # Recent support and resistance
    support = min(lows[-21:-1])
    resistance = max(highs[-21:-1])
    current = closes[-1]

    # Breakout checks
    if current > resistance:
        bullish += 2
        reasons.append("Resistance breakout")
    elif current < support:
        bearish += 2
        reasons.append("Support breakdown")

    difference = bullish - bearish

    # Conservative signal filter
    if difference >= 4 and trend == "BULLISH":
        signal = "BUY"
    elif difference <= -4 and trend == "BEARISH":
        signal = "SELL"
    else:
        signal = "WAIT"

    confidence = (
        min(90, 50 + abs(difference) * 5)
        if signal != "WAIT" else 0
    )

    return {
        "signal": signal,
        "confidence": confidence,
        "bullish_score": bullish,
        "bearish_score": bearish,
        "score_difference": difference,
        "reason": ", ".join(reasons) if reasons else "No strong setup",
        "patterns": [name for name, direction in patterns],
        "trend": trend,
        "support": support,
        "resistance": resistance,
        "momentum": "BULLISH" if closes[-1] > closes[-4]
                    else "BEARISH" if closes[-1] < closes[-4]
                    else "NEUTRAL"
    }
