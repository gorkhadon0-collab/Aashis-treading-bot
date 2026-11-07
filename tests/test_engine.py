import os
import tempfile
import unittest

from core.candles import validate_candle, analyze_candle
from core.patterns import detect_patterns
from core.engine import analyze
from core.risk import RiskManager


def make_candles(count=40):
    candles = []
    price = 100.0

    for i in range(count):
        open_price = price
        close_price = price + 0.2
        candles.append({
            "time": str(i),
            "open": open_price,
            "high": close_price + 0.1,
            "low": open_price - 0.1,
            "close": close_price
        })
        price = close_price

    return candles


class CandleTests(unittest.TestCase):
    def test_valid_candle(self):
        candle = make_candles(1)[0]
        self.assertTrue(validate_candle(candle))

    def test_invalid_candle(self):
        candle = {
            "open": 100,
            "high": 99,
            "low": 98,
            "close": 101
        }
        self.assertFalse(validate_candle(candle))

    def test_candle_direction(self):
        candle = make_candles(1)[0]
        self.assertEqual(
            analyze_candle(candle)["direction"],
            "BULLISH"
        )


class PatternTests(unittest.TestCase):
    def test_engulfing_pattern(self):
        candles = [
            {"open": 105, "high": 106, "low": 99, "close": 100},
            {"open": 100, "high": 101, "low": 98, "close": 99},
            {"open": 98, "high": 107, "low": 97, "close": 106}
        ]
        patterns = detect_patterns(candles)
        self.assertIn(
            ("Bullish Engulfing", "bullish"),
            patterns
        )


class EngineTests(unittest.TestCase):
    def test_insufficient_candles_wait(self):
        result = analyze(make_candles(10))
        self.assertEqual(result["signal"], "WAIT")

    def test_analysis_structure(self):
        result = analyze(make_candles(40))
        self.assertIn(result["signal"], ("BUY", "SELL", "WAIT"))
        self.assertIn("confidence", result)
        self.assertIn("reason", result)


class RiskTests(unittest.TestCase):
    def test_three_losses_stop_trading(self):
        original = os.getcwd()

        with tempfile.TemporaryDirectory() as folder:
            try:
                os.chdir(folder)
                risk = RiskManager()

                risk.record_result("LOSS")
                risk.record_result("LOSS")
                risk.record_result("LOSS")

                self.assertFalse(risk.can_trade())
                self.assertEqual(
                    risk.status()["consecutive_losses"], 3
                )
            finally:
                os.chdir(original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
