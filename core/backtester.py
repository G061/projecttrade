"""
Multi-symbol, multi-strategy backtesting engine with walk-forward support
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

class Backtester:
    def __init__(self, strategies, data_loader, initial_capital=100000):
        self.strategies = strategies  # dict: name -> strategy instance
        self.data_loader = data_loader
        self.initial_capital = initial_capital
        self.results = {}

    def run(self, symbols, start_date, end_date):
        for symbol in symbols:
            df = self.data_loader(symbol, start_date, end_date)
            for strat_name, strat in self.strategies.items():
                signals = strat.generate_signals(df)
                pnl, trades = self.simulate(df, signals)
                self.results[(symbol, strat_name)] = {'pnl': pnl, 'trades': trades}

    def simulate(self, df, signals):
        capital = self.initial_capital
        position = 0
        trades = []
        pnl_list = []
        for i, signal in enumerate(signals):
            price = df['close'].iloc[i]
            if signal == 'BUY' and position == 0:
                position = 1
                entry_price = price
                trades.append({'action': 'BUY', 'price': price, 'index': i})
            elif signal == 'SELL' and position == 1:
                capital += price - entry_price
                position = 0
                trades.append({'action': 'SELL', 'price': price, 'index': i})
            pnl_list.append(capital)
        return pnl_list, trades

    def plot_pnl(self, symbol, strat_name):
        result = self.results.get((symbol, strat_name))
        if not result:
            print(f"No results for {symbol}, {strat_name}")
            return
        plt.figure(figsize=(10, 4))
        plt.plot(result['pnl'])
        plt.title(f"PnL: {symbol} - {strat_name}")
        plt.xlabel("Time")
        plt.ylabel("Capital")
        plt.show()

    def export_logs(self, out_dir="logs"):
        os.makedirs(out_dir, exist_ok=True)
        for (symbol, strat_name), result in self.results.items():
            fname = f"{out_dir}/backtest_{symbol}_{strat_name}.csv"
            pd.DataFrame(result['trades']).to_csv(fname, index=False)
