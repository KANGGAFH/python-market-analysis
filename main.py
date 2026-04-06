"""
main.py — Advanced Market Analysis Tool
Quantitative Analysis Suite | Hedge-Fund Grade

Usage:
    python main.py                          # uses defaults (AAPL, 2y, daily)
    python main.py TSLA 3y 1d              # custom ticker / period / interval
    python main.py BTC-USD 5y 1wk          # crypto weekly bars

Positional args:
    1. ticker   — e.g. AAPL, TSLA, BTC-USD, ETH-USD, SPY, GLD
    2. period   — 1y | 2y | 3y | 5y | 10y | max
    3. interval — 1d (daily) | 1wk (weekly)
"""

import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

# ── Local modules ──────────────────────────────────────────────────────────────
import data_loader
import indicators
import stats
import strategy
import backtest
import ml_model
import visualization


# ══════════════════════════════════════════════════════════════════════════════
def run_analysis(ticker: str  = "AAPL",
                 period: str  = "2y",
                 interval: str = "1d",
                 output_html: str = "dashboard.html") -> dict:
    """
    Master pipeline — runs all modules in sequence.

    Returns a results dict containing all computed DataFrames and metrics.
    """
    print("\n" + "▓" * 60)
    print(f"  ADVANCED MARKET ANALYSIS TOOL")
    print(f"  Ticker: {ticker}  |  Period: {period}  |  Interval: {interval}")
    print("▓" * 60 + "\n")

    results = {}

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 1 — DATA COLLECTION & PREPROCESSING
    # ──────────────────────────────────────────────────────────────────────────
    print("━" * 50)
    print("  [1/7] Data Collection & Preprocessing")
    print("━" * 50)
    df = data_loader.load(ticker, period, interval)
    results["df_raw"] = df.copy()

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 2 — TECHNICAL INDICATORS
    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "━" * 50)
    print("  [2/7] Technical Analysis")
    print("━" * 50)
    df = indicators.add_all_indicators(df)
    results["df_indicators"] = df.copy()

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 3 — MARKET STATISTICS
    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "━" * 50)
    print("  [3/7] Statistical Analysis")
    print("━" * 50)
    market_stats = stats.market_statistics(df, ticker)
    stats.print_statistics(market_stats)
    results["market_stats"] = market_stats

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 4 — TRADING SIGNALS
    # ──────────────────────────────────────────────────────────────────────────
    print("━" * 50)
    print("  [4/7] Signal Generation")
    print("━" * 50)
    df = strategy.generate_signals(df)
    latest = strategy.latest_signal(df)
    strategy.print_signal(latest)
    results["df_signals"] = df.copy()
    results["latest_signal"] = latest

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 5 — BACKTESTING
    # ──────────────────────────────────────────────────────────────────────────
    print("━" * 50)
    print("  [5/7] Backtesting")
    print("━" * 50)
    df_bt, trade_log = backtest.run_backtest(df)
    bt_metrics        = backtest.backtest_metrics(df_bt, trade_log)
    backtest.print_backtest(bt_metrics)
    results["df_backtest"]  = df_bt
    results["trade_log"]    = trade_log
    results["bt_metrics"]   = bt_metrics

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 6 — MACHINE LEARNING
    # ──────────────────────────────────────────────────────────────────────────
    print("━" * 50)
    print("  [6/7] Machine Learning Prediction")
    print("━" * 50)
    try:
        ml_results   = ml_model.train_and_evaluate(df, target_horizon=5)
        future_preds = ml_model.predict_future(df, ml_results, n_days=10)

        print(f"\n  Future price predictions (next 10 trading days):")
        for date, price in future_preds.items():
            print(f"    {date.date()}  →  ${price:,.4f}")

        mc_df     = ml_model.monte_carlo(df, n_simulations=500, n_days=252)
        mc_summary = ml_model.monte_carlo_summary(mc_df)

        print(f"\n  Monte Carlo (252-day horizon, 500 simulations):")
        for k, v in mc_summary.items():
            print(f"    {k:<18} {v}")

        results["ml_results"]   = ml_results
        results["future_preds"] = future_preds
        results["mc_df"]        = mc_df
        results["mc_summary"]   = mc_summary

    except Exception as e:
        print(f"  [ML] Skipped: {e}")
        results["ml_results"]   = None
        results["future_preds"] = pd.Series(dtype=float)
        results["mc_df"]        = None

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 7 — VISUALIZATION
    # ──────────────────────────────────────────────────────────────────────────
    print("\n" + "━" * 50)
    print("  [7/7] Building Dashboard")
    print("━" * 50)

    charts = []
    charts.append(("Price Chart",
                   visualization.candlestick_chart(df_bt, ticker)))
    charts.append(("Momentum",
                   visualization.momentum_chart(df, ticker)))
    charts.append(("Equity Curve",
                   visualization.equity_curve_chart(df_bt, ticker)))
    charts.append(("Return Distribution",
                   visualization.return_distribution_chart(df, ticker)))

    if results["ml_results"]:
        charts.append(("ML Prediction",
                       visualization.prediction_chart(
                           df, results["ml_results"],
                           results["future_preds"], ticker)))
        charts.append(("Feature Importance",
                       visualization.feature_importance_chart(
                           results["ml_results"], ticker)))
        if results["mc_df"] is not None:
            charts.append(("Monte Carlo",
                           visualization.monte_carlo_chart(
                               df, results["mc_df"],
                               results["mc_summary"], ticker)))

    visualization.save_all_charts(charts, output_html)
    results["charts"] = charts

    print("\n" + "▓" * 60)
    print(f"  ✅  Analysis complete!  →  {output_html}")
    print("▓" * 60 + "\n")
    return results


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    args     = sys.argv[1:]
    ticker   = args[0] if len(args) > 0 else "AAPL"
    period   = args[1] if len(args) > 1 else "2y"
    interval = args[2] if len(args) > 2 else "1d"

    run_analysis(ticker, period, interval, output_html="dashboard.html")
