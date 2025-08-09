"""
Main entry point for Modular AI-Powered Automated Trading System
Includes fail-safe, auto-resume, and logging.
"""
import os
import sys
import traceback
import pandas as pd
from utils.logger import log_trade_json, log_signal_json, log_position_json, log_positions_state
from dotenv import load_dotenv

import argparse
from core.strategy_engine import StrategyEngine
from core.live_engine import LiveEngine
from utils.alert import send_telegram_alert, send_pushbullet_alert
from core.risk import RiskEngine
load_dotenv()

def load_mock_ohlcv(n=200):
    """Create a simple mock OHLCV DataFrame for demonstration/paper loop."""
    # Simple synthetic series
    idx = list(range(n))
    close = [100 + i*0.1 + (1 if i % 10 == 0 else 0) for i in idx]
    open_ = [c - 0.05 for c in close]
    high = [max(o, c) + 0.1 for o, c in zip(open_, close)]
    low = [min(o, c) - 0.1 for o, c in zip(open_, close)]
    vol = [1000 + (i % 5) * 10 for i in idx]
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": vol})

def load_csv_ohlcv(path):
    """Load OHLCV data from a CSV file. Expects columns: open,high,low,close[,volume][,date]."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {path}")
    df = pd.read_csv(path)
    required = {'open', 'high', 'low', 'close'}
    if not required.issubset(set(df.columns.str.lower())):
        # try lowercasing column names
        df.columns = [c.lower() for c in df.columns]
    if not required.issubset(set(df.columns)):
        raise ValueError(f"CSV must contain columns: {sorted(list(required))}")
    # Parse date if present
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'])
        except Exception:
            pass
    return df[['open','high','low','close'] + ([ 'volume' ] if 'volume' in df.columns else [])]


def main():
    parser = argparse.ArgumentParser(description="ProjectTrade CLI")
    parser.add_argument('--paper', action='store_true', help='Run in paper trading mode')
    parser.add_argument('--live', action='store_true', help='Run in live trading mode')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--strategies', action='store_true', help='List available strategies')
    parser.add_argument('--start', action='store_true', help='Start trading loop')
    parser.add_argument('--data-csv', type=str, help='Path to OHLCV CSV file to drive paper trading')
    parser.add_argument('--risk-reset', action='store_true', help='Reset daily risk state and clear circuit breaker')
    args = parser.parse_args()

    try:
        print("[INIT] ProjectTrade system booting...")
        # Discover and list strategies
        strat_engine = StrategyEngine()
        strat_engine.discover_strategies()
        print(f"[INFO] Strategies found: {strat_engine.list_strategies()}")

        # Show strategies and exit
        if args.strategies:
            print("Available strategies:", strat_engine.list_strategies())
            return

        # Init live engine and authenticate broker
        paper_mode = args.paper or not args.live
        live_engine = LiveEngine(paper_mode=paper_mode)
        risk_engine = RiskEngine()
        # Load persisted risk state unless reset
        if args.risk_reset:
            risk_engine.reset_daily()
            risk_engine.save_state()
            print("[RISK] Daily risk state reset.")
        else:
            if risk_engine.load_state():
                print(f"[RISK] Loaded risk state. Daily loss: {risk_engine.daily_loss}, CB: {risk_engine.circuit_breaker}")

        if not live_engine.authenticate():
            print("[ERROR] Broker authentication failed!")
            send_telegram_alert("ProjectTrade: Broker authentication failed!")
            sys.exit(1)
        print(f"[INFO] Broker authenticated. Paper mode: {paper_mode}")

        # Show system status and exit
        if args.status:
            print(f"Capital: {live_engine.capital}")
            print(f"Positions: {live_engine.positions}")
            print(f"Trades: {live_engine.trades}")
            print(f"Risk Daily Loss: {risk_engine.daily_loss}")
            print(f"Circuit Breaker: {risk_engine.circuit_breaker}")
            return

        # Start trading loop
        if args.start:
            print("[ENGINE] Starting paper trading loop...")
            symbol = os.getenv('SYMBOL', 'DEMO')
            try:
                if args.data_csv:
                    print(f"[DATA] Loading OHLCV from CSV: {args.data_csv}")
                    df = load_csv_ohlcv(args.data_csv)
                else:
                    df = load_mock_ohlcv(n=200)
            except Exception as e:
                print(f"[DATA] Failed to load CSV, falling back to mock data: {e}")
                df = load_mock_ohlcv(n=200)
            for strat_name in strat_engine.list_strategies():
                strat = strat_engine.get_strategy(strat_name)
                print(f"[STRATEGY] Running {strat_name} on {symbol}")
                signals = strat.generate_signals(df)
                position_open = False
                entry_price = None
                qty = 1
                for i, sig in enumerate(signals):
                    if live_engine.circuit_breaker or risk_engine.circuit_breaker:
                        print("[RISK] Circuit breaker active. Halting strategy loop.")
                        break
                    price = float(df['close'].iloc[i])
                    # Log signal for dashboard
                    log_signal_json({
                        'i': int(i),
                        'symbol': symbol,
                        'strategy': strat_name,
                        'signal': str(sig),
                        'price': price
                    })
                    if sig == 'BUY' and not position_open:
                        # Risk check before entering
                        ok, msg = risk_engine.check_trade(live_engine.capital, qty * price, 0)
                        if not ok:
                            print(f"[RISK] Trade blocked: {msg}")
                            continue
                        trade = live_engine.place_order(symbol, qty, 'BUY', 'MARKET', price=price)
                        entry_price = price
                        position_open = True
                        live_engine.positions.append({'symbol': symbol, 'qty': qty, 'side': 'LONG', 'entry': entry_price, 'strategy': strat_name, 'i': int(i)})
                        log_position_json(live_engine.positions[-1])
                        # Persist current open positions state for dashboard
                        log_positions_state(live_engine.positions)
                    elif sig == 'SELL' and position_open:
                        trade = live_engine.place_order(symbol, qty, 'SELL', 'MARKET', price=price)
                        pnl = (price - entry_price) * qty
                        position_open = False
                        # Record position close
                        log_trade_json({'symbol': symbol, 'qty': qty, 'entry': entry_price, 'exit': price, 'pnl': pnl, 'strategy': strat_name, 'i': int(i), 'paper': True})
                        # Update risk with losses; trigger circuit breaker if needed
                        if pnl < 0:
                            ok, msg = risk_engine.update_daily_loss(abs(pnl), live_engine.capital)
                            if not ok:
                                live_engine.circuit_breaker = True
                                print(f"[RISK] {msg}")
                        # Remove last open position record (simple single-position demo) and update positions state
                        if live_engine.positions:
                            live_engine.positions.pop()
                        log_positions_state(live_engine.positions)
                # Close any open position at last price
                if position_open:
                    price = float(df['close'].iloc[-1])
                    trade = live_engine.place_order(symbol, qty, 'SELL', 'MARKET', price=price)
                    pnl = (price - entry_price) * qty
                    log_trade_json({'symbol': symbol, 'qty': qty, 'entry': entry_price, 'exit': price, 'pnl': pnl, 'strategy': strat_name, 'i': int(len(df)-1), 'paper': True})
                    # Update positions state on forced close
                    if live_engine.positions:
                        live_engine.positions.pop()
                    log_positions_state(live_engine.positions)
            print("[ENGINE] Paper trading loop complete.")
            # Persist risk state at end of run
            risk_engine.save_state()
            # Final positions state write
            log_positions_state(live_engine.positions)
            return

        print("[INFO] Use --help for CLI options.")
    except Exception as e:
        print(f"Fatal error: {e}")
        log_trade_json({"error": str(e), "traceback": traceback.format_exc()})
        send_pushbullet_alert(f"ProjectTrade Fatal Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
