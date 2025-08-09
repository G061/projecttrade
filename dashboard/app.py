"""
Streamlit Dashboard for ProjectTrade
"""
import streamlit as st
import pandas as pd
import os
import glob
import json
from datetime import date

st.set_page_config(page_title="ProjectTrade Dashboard", layout="wide")
st.title("📈 ProjectTrade Live Dashboard")

# --- Current Positions ---
st.header("Current Positions")
positions_state_file = os.path.join("logs", "positions_state.json")
positions_history_file = os.path.join("logs", "positions.json")
positions = []
# Prefer current state JSON (array of open positions)
if os.path.exists(positions_state_file):
    try:
        with open(positions_state_file) as f:
            positions = json.load(f)
    except Exception:
        positions = []
# Fallback to history JSONL if state is missing or empty
if not positions and os.path.exists(positions_history_file):
    with open(positions_history_file) as f:
        positions = [json.loads(line) for line in f if line.strip()]
if positions:
    st.dataframe(pd.DataFrame(positions))
else:
    st.info("No current positions.")

# --- Strategy Performance Leaderboard ---
st.header("Strategy Performance Leaderboard")
leaderboard = []
for file in glob.glob(os.path.join("logs", "backtest_*.csv")):
    df = pd.read_csv(file)
    if not df.empty:
        strat = file.split("backtest_")[1].replace(".csv", "")
        # Prefer PnL column if present, else simple price diff fallback
        if 'pnl' in df.columns:
            pnl_val = df['pnl'].sum()
        elif 'price' in df.columns:
            pnl_val = df['price'].diff().sum()
        else:
            pnl_val = 0
        leaderboard.append({"Strategy": strat, "PnL": pnl_val, "Trades": len(df)})
if leaderboard:
    st.dataframe(pd.DataFrame(leaderboard).sort_values("PnL", ascending=False))
else:
    st.info("No backtest results yet.")

# --- Live Signal Feed ---
st.header("Live Signal Feed")
signals_file = os.path.join("logs", "signals.json")
if os.path.exists(signals_file):
    with open(signals_file) as f:
        signals = [json.loads(line) for line in f if line.strip()]
    if signals:
        st.dataframe(pd.DataFrame(signals))
    else:
        st.info("No signals yet.")
else:
    st.info("No signals yet.")

# --- Daily PnL (from trades.json) ---
st.header("Daily PnL")
trades_file = os.path.join("logs", "trades.json")
if os.path.exists(trades_file):
    with open(trades_file) as f:
        trades = [json.loads(line) for line in f if line.strip()]
    if trades:
        trades_df = pd.DataFrame(trades)
        if 'date' in trades_df.columns and 'pnl' in trades_df.columns:
            daily = trades_df.groupby('date', dropna=False)['pnl'].sum().reset_index().sort_values('date')
            daily['CumPnL'] = daily['pnl'].cumsum()
            st.subheader("By Day")
            st.dataframe(daily)
            st.metric("Total PnL", f"{daily['pnl'].sum():.2f}")
        else:
            st.info("Trades found but missing 'date' or 'pnl' fields.")
    else:
        st.info("No trades yet.")
else:
    st.info("No trades yet.")

# --- Control Panel ---
st.header("Control Panel")
col1, col2 = st.columns(2)
with col1:
    if st.button("Activate All Strategies"):
        st.success("All strategies activated (stub).")
with col2:
    if st.button("Deactivate All Strategies"):
        st.warning("All strategies deactivated (stub).")

# --- Natural Language Command/Query ---
st.header("Ask Anything (Natural Language Query)")
user_query = st.text_input("Ask about trades, PnL, win rate, etc.")
if user_query:
    from core.nlp_query import query_trades_nlp
    trades_file = os.path.join("logs", "trades.json")
    trade_logs = []
    if os.path.exists(trades_file):
        with open(trades_file) as f:
            trade_logs = [json.loads(line) for line in f if line.strip()]
    response = query_trades_nlp(user_query, trade_logs)
    st.write(response)
