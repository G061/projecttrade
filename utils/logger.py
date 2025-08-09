"""
Trade logger for JSON/CSV logs and daily PnL reports
"""
import os
import json
import csv
import datetime

def log_trade_json(trade, out_dir="logs"):
    os.makedirs(out_dir, exist_ok=True)
    fname = os.path.join(out_dir, "trades.json")
    # Auto-augment with timestamp/date if missing
    if 'timestamp' not in trade:
        trade['timestamp'] = datetime.datetime.utcnow().isoformat()
    if 'date' not in trade:
        trade['date'] = datetime.date.today().isoformat()
    with open(fname, "a") as f:
        f.write(json.dumps(trade) + "\n")

def log_trade_csv(trade, out_dir="logs"):
    os.makedirs(out_dir, exist_ok=True)
    fname = os.path.join(out_dir, "trades.csv")
    write_header = not os.path.exists(fname)
    with open(fname, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=trade.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(trade)

def log_daily_pnl(pnl, out_dir="logs"):
    os.makedirs(out_dir, exist_ok=True)
    date = datetime.date.today().isoformat()
    fname = os.path.join(out_dir, f"pnl_{date}.txt")
    with open(fname, "w") as f:
        f.write(str(pnl))

def log_signal_json(signal_entry, out_dir="logs"):
    """Append a signal entry to logs/signals.json as JSONL."""
    os.makedirs(out_dir, exist_ok=True)
    fname = os.path.join(out_dir, "signals.json")
    with open(fname, "a") as f:
        f.write(json.dumps(signal_entry) + "\n")

def log_position_json(position_entry, out_dir="logs"):
    """Append a position entry to logs/positions.json as JSONL."""
    os.makedirs(out_dir, exist_ok=True)
    fname = os.path.join(out_dir, "positions.json")
    with open(fname, "a") as f:
        f.write(json.dumps(position_entry) + "\n")

def log_positions_state(positions, out_dir="logs"):
    """Overwrite logs/positions_state.json with the list of currently open positions.
    Expected `positions` is a list of dicts representing open positions.
    """
    os.makedirs(out_dir, exist_ok=True)
    fname = os.path.join(out_dir, "positions_state.json")
    try:
        with open(fname, "w") as f:
            json.dump(positions or [], f)
    except Exception as e:
        # Non-fatal: continue even if state file write fails
        print(f"[LOGGER] Failed to write positions_state.json: {e}")
