"""
backtest.py — Strategy Backtesting Module
Simulates trading based on generated signals and computes performance metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


TRADING_DAYS = 252


# ─────────────────────────────────────────────
#  Core Backtester
# ─────────────────────────────────────────────

def run_backtest(df: pd.DataFrame,
                 initial_capital: float = 100_000.0,
                 commission_pct: float = 0.001,
                 slippage_pct: float = 0.0005) -> pd.DataFrame:
    """
    Vectorised backtest engine.

    Rules:
        • Fully invested (100 % of capital) on each BUY signal.
        • Liquidate entire position on SELL signal.
        • No short selling.
        • Commission + slippage applied on each trade.

    Args:
        df              : DataFrame with 'signal' and 'close' columns.
        initial_capital : Starting portfolio value (USD).
        commission_pct  : Round-trip cost per trade (default 0.1 %).
        slippage_pct    : Price impact per side (default 0.05 %).

    Returns:
        DataFrame with portfolio tracking columns appended.
    """
    df = df.copy()
    df = df.dropna(subset=["signal", "close"])

    capital    = initial_capital
    position   = 0.0    # number of shares held
    in_market  = False

    portfolio_values = []
    trade_log        = []

    cost_factor = 1 + commission_pct + slippage_pct  # entry cost multiplier
    sell_factor = 1 - commission_pct - slippage_pct  # exit receipt multiplier

    for i, (date, row) in enumerate(df.iterrows()):
        sig   = row["signal"]
        price = row["close"]

        # ── Entry
        if sig == 1 and not in_market:
            effective_price = price * cost_factor
            position        = capital / effective_price
            capital         = 0.0
            in_market       = True
            trade_log.append({
                "date": date, "type": "BUY",
                "price": price, "shares": position,
            })

        # ── Exit
        elif sig == -1 and in_market:
            effective_price = price * sell_factor
            capital         = position * effective_price
            trade_log.append({
                "date": date, "type": "SELL",
                "price": price, "shares": position,
                "value": capital,
            })
            position  = 0.0
            in_market = False

        # ── Mark-to-market portfolio value
        portfolio_values.append(capital + position * price)

    df["portfolio_value"] = portfolio_values
    df["portfolio_return"] = df["portfolio_value"].pct_change()

    # Buy-and-hold benchmark
    bah_shares              = initial_capital / df["close"].iloc[0]
    df["bah_value"]         = bah_shares * df["close"]
    df["bah_return"]        = df["bah_value"].pct_change()

    # Drawdown series
    df["strategy_drawdown"] = _drawdown(df["portfolio_value"])
    df["bah_drawdown"]      = _drawdown(df["bah_value"])

    return df, trade_log


def _drawdown(series: pd.Series) -> pd.Series:
    roll_max = series.cummax()
    return (series - roll_max) / roll_max


# ─────────────────────────────────────────────
#  Performance Metrics
# ─────────────────────────────────────────────

def backtest_metrics(df: pd.DataFrame, trade_log: list,
                     initial_capital: float = 100_000.0) -> Dict[str, Any]:
    """
    Compute comprehensive backtest performance metrics.
    """
    port  = df["portfolio_value"].dropna()
    bah   = df["bah_value"].dropna()
    rets  = df["portfolio_return"].dropna()
    n     = len(df)

    # Win rate
    trades     = pd.DataFrame(trade_log)
    sell_trades = trades[trades["type"] == "SELL"] if len(trades) > 0 else pd.DataFrame()
    win_rate    = 0.0
    if len(sell_trades) > 0:
        buy_prices  = trades[trades["type"] == "BUY"]["price"].values
        sell_prices = sell_trades["price"].values
        pairs       = min(len(buy_prices), len(sell_prices))
        if pairs > 0:
            wins     = sum(sell_prices[:pairs] > buy_prices[:pairs])
            win_rate = wins / pairs

    # Returns
    strat_total = (port.iloc[-1] / initial_capital - 1) * 100
    bah_total   = (bah.iloc[-1] / initial_capital - 1) * 100

    n_years     = n / TRADING_DAYS
    strat_ann   = ((port.iloc[-1] / initial_capital) ** (1 / n_years) - 1) * 100 if n_years > 0 else 0
    bah_ann     = ((bah.iloc[-1] / initial_capital) ** (1 / n_years) - 1) * 100 if n_years > 0 else 0

    # Sharpe
    sharpe = 0.0
    if rets.std() > 0:
        sharpe = (rets.mean() / rets.std()) * np.sqrt(TRADING_DAYS)

    # Profit factor
    pnl_per_trade = []
    buy_prices    = trades[trades["type"] == "BUY"]["price"].values if len(trades) > 0 else []
    sell_prices   = sell_trades["price"].values if len(sell_trades) > 0 else []
    for bp, sp in zip(buy_prices, sell_prices):
        pnl_per_trade.append(sp - bp)

    gross_profit = sum(p for p in pnl_per_trade if p > 0)
    gross_loss   = abs(sum(p for p in pnl_per_trade if p < 0))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float("inf")

    return {
        "strategy_total_return_pct":  round(strat_total, 2),
        "bah_total_return_pct":       round(bah_total, 2),
        "strategy_ann_return_pct":    round(strat_ann, 2),
        "bah_ann_return_pct":         round(bah_ann, 2),
        "sharpe_ratio":               round(sharpe, 3),
        "max_drawdown_pct":           round(df["strategy_drawdown"].min() * 100, 2),
        "bah_max_drawdown_pct":       round(df["bah_drawdown"].min() * 100, 2),
        "num_trades":                 len(trades) // 2,
        "win_rate_pct":               round(win_rate * 100, 1),
        "profit_factor":              round(profit_factor, 3),
        "final_portfolio_value":      round(float(port.iloc[-1]), 2),
        "final_bah_value":            round(float(bah.iloc[-1]), 2),
    }


def print_backtest(metrics: Dict[str, Any]) -> None:
    print("\n" + "═" * 55)
    print("  BACKTEST RESULTS")
    print("═" * 55)
    rows = [
        ("Strategy Total Return",   f"{metrics['strategy_total_return_pct']:+.2f} %"),
        ("Buy-and-Hold Return",     f"{metrics['bah_total_return_pct']:+.2f} %"),
        ("Strategy Ann. Return",    f"{metrics['strategy_ann_return_pct']:+.2f} %"),
        ("B&H Ann. Return",         f"{metrics['bah_ann_return_pct']:+.2f} %"),
        ("",                        ""),
        ("Sharpe Ratio",            metrics["sharpe_ratio"]),
        ("Max Drawdown (Strategy)", f"{metrics['max_drawdown_pct']:.2f} %"),
        ("Max Drawdown (B&H)",      f"{metrics['bah_max_drawdown_pct']:.2f} %"),
        ("",                        ""),
        ("Number of Trades",        metrics["num_trades"]),
        ("Win Rate",                f"{metrics['win_rate_pct']:.1f} %"),
        ("Profit Factor",           metrics["profit_factor"]),
        ("",                        ""),
        ("Final Portfolio Value",   f"${metrics['final_portfolio_value']:,.2f}"),
        ("Final B&H Value",         f"${metrics['final_bah_value']:,.2f}"),
    ]
    for label, value in rows:
        if label == "":
            print()
        else:
            print(f"  {label:<28} {value}")
    print("═" * 55 + "\n")
