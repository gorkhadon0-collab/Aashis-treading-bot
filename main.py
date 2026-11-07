import time
from core.market_data import get_candles
from core.engine import analyze

SYMBOL = "EUR/USD"
INTERVAL = "1min"

def main():
    print("\n===== AASHIS BOT =====")
    print("Market:", SYMBOL)
    print("Status: SCANNING")
    print("Ctrl + C to stop\n")

    while True:
        try:
            candles = get_candles(SYMBOL, INTERVAL, 100)
            result = analyze(candles)

            print(
                f"Candles: {len(candles)} | "
                f"Signal: {result['signal']} | "
                f"Confidence score: {result['confidence']} | "
                f"Reason: {result['reason']}"
            )

        except KeyboardInterrupt:
            print("\nAASHIS BOT stopped.")
            break
        except Exception as error:
            print("Market error:", error)

        time.sleep(60)

if __name__ == "__main__":
    main()
