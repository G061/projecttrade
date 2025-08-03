# Modular AI-Powered Automated Trading System (ProjectTrade)

## Overview
A production-ready, modular, AI-powered auto-trading system for Indian stock markets (Angel One, 5paisa, Upstox-ready). Features multi-strategy, AI/ML, news/sentiment, risk, logging, and dashboarding.

## Folder Structure
```
core/         # Core engine: execution, backtesting, broker, risk, config
strategies/   # Plug-and-play strategies: momentum, mean-rev, breakout, etc.
models/       # ML/DL models: LSTM, transformer, sentiment, etc.
utils/        # Utilities: indicators, news scraping, NLP, helpers
logs/         # All logs, trade history, daily PnL, error logs
dashboard/    # Streamlit or React+Flask dashboard
tests/        # Unit and integration tests
main.py       # Entry point
requirements.txt
.env          # Secrets (not committed)
README.md
```

## Features
- Modular multi-layer strategy engine (AI, technical, sentiment, candlestick)
- Angel One SmartAPI integration (extensible to others)
- Backtesting engine, walk-forward, multi-symbol, daily PnL
- LSTM/Transformer models, sentiment analysis, news scraping
- Risk engine: stop loss, max loss, circuit breaker
- Alerts: Telegram, Pushbullet, daily PnL
- Web dashboard (optional)
- Self-learning pipeline (auto-training, model update)
- Security: .env secrets, auto-resume, full logging

## Setup
1. `pip install -r requirements.txt`
2. Add your API keys and secrets to `.env` (see template below).
3. Run `python main.py` or launch dashboard.

## .env Template
```
ANGEL_API_KEY=your_angel_api_key
ANGEL_CLIENT_CODE=your_client_code
ANGEL_ACCESS_TOKEN=your_access_token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
PUSHBULLET_API_KEY=your_pushbullet_key
# ... more as needed
```

## Extending
- Add new strategies in `strategies/`
- Add new models in `models/`
- Add new utilities in `utils/`

## Disclaimer
For educational use only. Use at your own risk.
