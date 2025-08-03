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
