from core.patterns import detect_patterns, candle_info


def analyze(candles):
    if len(candles) < 20:
        return {"signal": "WAIT", "confidence": 0, "reason": "Not enough candles"}

    recent = candles[-20:]
    patterns = detect_patterns(recent)

    bullish = 0
    bearish = 0
    reasons = []

    for name, direction in patterns:
        if direction == "bullish":
            bullish += 2
            reasons.append(name)
        elif direction == "bearish":
            bearish += 2
            reasons.append(name)

    # Recent candle momentum
    last_three = recent[-3:]
    for candle in last_three:
        info = candle_info(candle)
        if info["bull"] and info["body"] > 0.55:
            bullish += 1
        elif info["bear"] and info["body"] > 0.55:
            bearish += 1

    # Recent price direction
    closes = [float(c["close"]) for c in recent]
    if closes[-1] > closes[-5]:
        bullish += 1
    elif closes[-1] < closes[-5]:
        bearish += 1

    difference = bullish - bearish

    if difference >= 3:
        signal = "BUY"
    elif difference <= -3:
        signal = "SELL"
    else:
        signal = "WAIT"

    confidence = min(95, 50 + abs(difference) * 7) if signal != "WAIT" else 0

    return {
        "signal": signal,
        "confidence": confidence,
        "reason": ", ".join(reasons) if reasons else "No strong candle pattern",
    }
