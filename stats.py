"""
stats.py — Statistical Market Analysis Module
Risk metrics, performance analytics, and correlation analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


TRADING_DAYS = 252   # annual trading days (equities)


# ─────────────────────────────────────────────
#  Core Risk & Performance Metrics
# ─────────────────────────────────────────────

def annualized_return(returns: pd.Series) -> float:
    """Compound annualised return from daily return series."""
    n_days = len(returns)
    total  = (1 + returns).prod()
    return float(total ** (TRADING_DAYS / n_days) - 1)


def annualized_volatility(returns: pd.Series) -> float:
    """Annualised volatility (standard deviation of daily returns × √252)."""
    return float(returns.std() * np.sqrt(TRADING_DAYS))


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.05) -> float:
    """
    Sharpe Ratio = (annualised return − Rf) / annualised volatility.
    Default risk-free rate: 5 % (approximate current US T-bill yield).
    """
    ann_ret = annualized_return(returns)
    ann_vol = annualized_volatility(returns)
    if ann_vol == 0:
        return 0.0
    return (ann_ret - risk_free_rate) / ann_vol


def sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.05) -> float:
    """Sortino Ratio — penalises only downside volatility."""
    ann_ret     = annualized_return(returns)
    downside    = returns[returns < 0]
    down_vol    = float(downside.std() * np.sqrt(TRADING_DAYS))
    if down_vol == 0:
        return 0.0
    return (ann_ret - risk_free_rate) / down_vol


def max_drawdown(close: pd.Series) -> float:
    """
    Maximum Drawdown — largest peak-to-trough decline in price history.
    Returns a negative float (e.g. -0.35 means −35 %).
    """
    roll_max = close.cummax()
    dd       = (close - roll_max) / roll_max
    return float(dd.min())


def drawdown_series(close: pd.Series) -> pd.Series:
    """Full time-series of drawdown values (for plotting equity curve)."""
    roll_max = close.cummax()
    return (close - roll_max) / roll_max


def calmar_ratio(close: pd.Series, returns: pd.Series) -> float:
    """Calmar Ratio = annualised return / |max drawdown|."""
    mdd = abs(max_drawdown(close))
    if mdd == 0:
        return 0.0
    return annualized_return(returns) / mdd


def value_at_risk(returns: pd.Series, confidence: float = 0.95) -> float:
    """Historical VaR at given confidence level (e.g. 0.95 → 5th percentile)."""
    return float(np.percentile(returns.dropna(), (1 - confidence) * 100))


def conditional_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """CVaR / Expected Shortfall — mean of losses beyond VaR threshold."""
    var    = value_at_risk(returns, confidence)
    losses = returns[returns <= var]
    return float(losses.mean()) if len(losses) > 0 else var


# ─────────────────────────────────────────────
#  Summary Report
# ─────────────────────────────────────────────

def market_statistics(df: pd.DataFrame, ticker: str = "Asset") -> Dict[str, Any]:
    """
    Compute comprehensive market statistics from preprocessed DataFrame.

    Returns a dictionary of labelled metrics.
    """
    returns = df["daily_return"].dropna()
    close   = df["close"]

    stats = {
        "ticker":                ticker,
        "start_date":            str(df.index[0].date()),
        "end_date":              str(df.index[-1].date()),
        "trading_days":          len(df),
        "current_price":         round(float(close.iloc[-1]), 4),
        "price_high":            round(float(close.max()), 4),
        "price_low":             round(float(close.min()), 4),

        # Returns
        "total_return_pct":      round((close.iloc[-1] / close.iloc[0] - 1) * 100, 2),
        "annualized_return_pct": round(annualized_return(returns) * 100, 2),
        "annualized_vol_pct":    round(annualized_volatility(returns) * 100, 2),

        # Risk-adjusted
        "sharpe_ratio":          round(sharpe_ratio(returns), 3),
        "sortino_ratio":         round(sortino_ratio(returns), 3),
        "calmar_ratio":          round(calmar_ratio(close, returns), 3),

        # Drawdown
        "max_drawdown_pct":      round(max_drawdown(close) * 100, 2),

        # Tail risk
        "var_95_pct":            round(value_at_risk(returns, 0.95) * 100, 2),
        "cvar_95_pct":           round(conditional_var(returns, 0.95) * 100, 2),

        # Distribution
        "daily_return_mean_pct": round(returns.mean() * 100, 4),
        "daily_return_skew":     round(float(returns.skew()), 4),
        "daily_return_kurtosis": round(float(returns.kurtosis()), 4),
    }
    return stats


def print_statistics(stats: Dict[str, Any]) -> None:
    """Pretty-print the statistics dictionary to console."""
    print("\n" + "═" * 55)
    print(f"  MARKET STATISTICS — {stats['ticker']}")
    print("═" * 55)
    rows = [
        ("Period",                f"{stats['start_date']}  →  {stats['end_date']}"),
        ("Trading Days",          stats["trading_days"]),
        ("Current Price",         f"${stats['current_price']:,.4f}"),
        ("52-wk High / Low",      f"${stats['price_high']:,.4f} / ${stats['price_low']:,.4f}"),
        ("",                      ""),
        ("Total Return",          f"{stats['total_return_pct']:+.2f} %"),
        ("Annualised Return",     f"{stats['annualized_return_pct']:+.2f} %"),
        ("Annualised Volatility", f"{stats['annualized_vol_pct']:.2f} %"),
        ("",                      ""),
        ("Sharpe Ratio",          stats["sharpe_ratio"]),
        ("Sortino Ratio",         stats["sortino_ratio"]),
        ("Calmar Ratio",          stats["calmar_ratio"]),
        ("Max Drawdown",          f"{stats['max_drawdown_pct']:.2f} %"),
        ("",                      ""),
        ("VaR 95 %",              f"{stats['var_95_pct']:.2f} %"),
        ("CVaR 95 %",             f"{stats['cvar_95_pct']:.2f} %"),
        ("",                      ""),
        ("Daily Return Mean",     f"{stats['daily_return_mean_pct']:.4f} %"),
        ("Skewness",              stats["daily_return_skew"]),
        ("Excess Kurtosis",       stats["daily_return_kurtosis"]),
    ]
    for label, value in rows:
        if label == "":
            print()
        else:
            print(f"  {label:<26} {value}")
    print("═" * 55 + "\n")


# ─────────────────────────────────────────────
#  Correlation Matrix
# ─────────────────────────────────────────────

def correlation_matrix(dataframes: dict) -> pd.DataFrame:
    """
    Build a return-correlation matrix across multiple assets.

    Args:
        dataframes : { 'AAPL': df_aapl, 'TSLA': df_tsla, ... }

    Returns:
        Correlation matrix DataFrame.
    """
    returns = {ticker: df["daily_return"] for ticker, df in dataframes.items()}
    combined = pd.DataFrame(returns)
    return combined.corr()
