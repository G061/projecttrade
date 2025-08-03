"""
Main entry point for Modular AI-Powered Automated Trading System
Includes fail-safe, auto-resume, and logging.
"""
import os
import sys
import traceback
from utils.logger import log_trade_json

import argparse
from core.strategy_engine import StrategyEngine
from core.live_engine import LiveEngine
from utils.alert import send_telegram_alert, send_pushbullet_alert


def main():
    parser = argparse.ArgumentParser(description="ProjectTrade CLI")
    parser.add_argument('--paper', action='store_true', help='Run in paper trading mode')
    parser.add_argument('--live', action='store_true', help='Run in live trading mode')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--strategies', action='store_true', help='List available strategies')
    parser.add_argument('--start', action='store_true', help='Start trading loop')
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
            return

        # Start trading loop
        if args.start:
            print("[ENGINE] Starting trading loop (stub)...")
            # Example: run all discovered strategies in a stub loop
            for strat_name in strat_engine.list_strategies():
                strat = strat_engine.get_strategy(strat_name)
                print(f"[STRATEGY] Running {strat_name} (stub)")
                # Here you would fetch market data and call strat.generate_signals()
                # For now, just log and send alert
                send_telegram_alert(f"Strategy {strat_name} executed (stub)")
            print("[ENGINE] Trading loop complete (stub).")
            return

        print("[INFO] Use --help for CLI options.")
    except Exception as e:
        print(f"Fatal error: {e}")
        log_trade_json({"error": str(e), "traceback": traceback.format_exc()})
        send_pushbullet_alert(f"ProjectTrade Fatal Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
