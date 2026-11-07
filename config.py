import os

BOT_NAME = "AASHIS BOT"

# Market settings
MARKET_SYMBOL = os.getenv("AASHIS_SYMBOL", "EUR/USD")
MARKET_INTERVAL = os.getenv("AASHIS_INTERVAL", "1min")
CANDLE_LIMIT = 100

# Analysis settings
MIN_CANDLES = 30
MIN_SIGNAL_STRENGTH = 4

# Risk settings
MAX_CONSECUTIVE_LOSSES = 3
MAX_DAILY_TRADES = 20

# Engine settings
SCAN_INTERVAL_SECONDS = 60
API_TIMEOUT_SECONDS = 20

# Safety settings
AUTO_TRADING_ENABLED = False
DEMO_MODE = True
REQUIRE_MANUAL_CONFIRMATION = True

# API key must be set in Termux environment.
AASHIS_API_KEY = os.getenv("AASHIS_API_KEY", "")
