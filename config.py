# config.py
# Holds core configuration parameters for the arbitrage detection system.

import os

# Exchange and asset settings
TARGET_EXCHANGES = [
    "binance",
    # "coinbasepro",
    "kraken",
    # add more as needed (bitfinex, okx, bybit, etc.)
]

TARGET_PAIRS = [
    "BTC/USDT",
    "ETH/USDT",
    # add more pairs here
]

# Z-score and Spread thresholds
Z_SCORE_THRESHOLD = 0.9      # |Z| >= 2 triggers a potential signal
MIN_SPREAD_PCT = 0.002        # 0.2% minimum spread required (e.g., 0.002 = 0.2%)

# Rolling window for spread, mean, and std calculations
ROLLING_WINDOW_SIZE = 100

# Cooldown period (seconds) to avoid spamming signals for the same condition
SIGNAL_COOLDOWN = 600  # 10 minutes in seconds

# Alert system settings
ALERT_EMAIL_ENABLED = False
ALERT_TELEGRAM_ENABLED = False
ALERT_DISCORD_ENABLED = False

# Example credentials / tokens (replace with real ones if you enable each alert type)
EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 587
EMAIL_SENDER = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

# Database or local storage
USE_DATABASE = False
DATABASE_URI = "postgresql://user:password@localhost:5432/arbitrage_db"

# Optional environment variable usage
API_KEY_BINANCE = os.getenv("BINANCE_API_KEY", "")
API_SECRET_BINANCE = os.getenv("BINANCE_API_SECRET", "")
# etc. for other exchanges

