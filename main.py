import time

from config import (
    BOT_NAME,
    MARKET_SYMBOL,
    MARKET_INTERVAL,
    CANDLE_LIMIT,
    SCAN_INTERVAL_SECONDS,
    MAX_CONSECUTIVE_LOSSES,
    MAX_DAILY_TRADES,
)
from core.control_server import start_server, RUN_EVENT, STOP_EVENT
from core.market_data import get_candles
from core.engine import analyze
from core.risk import RiskManager


def main():
    risk = RiskManager(
        max_losses=MAX_CONSECUTIVE_LOSSES,
        max_daily_trades=MAX_DAILY_TRADES,
    )

    print(f"\n===== {BOT_NAME} =====")
    print(f"Market: {MARKET_SYMBOL}")
    print(f"Interval: {MARKET_INTERVAL}")
    print("Mode: ANALYSIS ONLY - NO AUTOMATIC TRADES")

    start_server()
    print("Waiting for START command...\n")

    try:
        while True:
            RUN_EVENT.wait()

            if not RUN_EVENT.is_set():
                continue

            print("\nAASHIS BOT: ANALYSIS STARTED")

            while RUN_EVENT.is_set():
                if not risk.can_trade():
                    print("RISK LIMIT REACHED - ANALYSIS STOPPED")
                    RUN_EVENT.clear()
                    STOP_EVENT.set()
                    break

                try:
                    candles = get_candles(
                        MARKET_SYMBOL,
                        MARKET_INTERVAL,
                        CANDLE_LIMIT,
                    )

                    if not RUN_EVENT.is_set():
                        break

                    result = analyze(candles)

                    print("\n---------- ANALYSIS ----------")
                    print(f"Candles: {len(candles)}")
                    print(f"Signal: {result['signal']}")
                    print(f"Bullish score: {result['bullish_score']}")
                    print(f"Bearish score: {result['bearish_score']}")
                    print(f"Score difference: {result['score_difference']}")
                    print(f"Signal confidence: {result['confidence']} (not win probability)")
                    print(f"Trend: {result['trend']}")
                    print(f"Momentum: {result.get('momentum', 'UNKNOWN')}")
                    print(f"Support: {result.get('support', 'N/A')}")
                    print(f"Resistance: {result.get('resistance', 'N/A')}")
                    print(f"Patterns: {', '.join(result['patterns']) or 'None'}")
                    print(f"Reason: {result['reason']}")
                    print("------------------------------")

                except Exception as error:
                    print("Market/Analysis error:", error)

                if STOP_EVENT.wait(SCAN_INTERVAL_SECONDS):
                    break

            print("AASHIS BOT: STOPPED")

    except KeyboardInterrupt:
        print("\nClosing AASHIS BOT...")

    finally:
        RUN_EVENT.clear()
        STOP_EVENT.set()
        print("AASHIS BOT closed.")


if __name__ == "__main__":
    main()
