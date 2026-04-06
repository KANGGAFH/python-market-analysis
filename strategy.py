"""
strategy.py — Trading Signal Engine
Generates BUY / SELL / HOLD signals from combined indicator rules.
"""

import pandas as pd
import numpy as np


# ─────────────────────────────────────────────
#  Signal constants
# ─────────────────────────────────────────────

BUY  =  1
HOLD =  0
SELL = -1


# ─────────────────────────────────────────────
#  Individual signal components
# ─────────────────────────────────────────────

def _rsi_signal(df: pd.DataFrame,
                oversold: float = 30, overbought: float = 70) -> pd.Series:
    """RSI-based signal."""
    sig = pd.Series(HOLD, index=df.index)
    sig[df["rsi14"] < oversold]   = BUY
    sig[df["rsi14"] > overbought] = SELL
    return sig


def _bb_signal(df: pd.DataFrame) -> pd.Series:
    """Bollinger Band touch signal."""
    sig = pd.Series(HOLD, index=df.index)
    sig[df["close"] <= df["bb_lower"]] = BUY
    sig[df["close"] >= df["bb_upper"]] = SELL
    return sig


def _ma_crossover_signal(df: pd.DataFrame,
                          fast_col: str = "ma50",
                          slow_col: str = "ma200") -> pd.Series:
    """
    Golden / Death Cross.
    BUY  when fast MA crosses above slow MA.
    SELL when fast MA crosses below slow MA.
    """
    sig = pd.Series(HOLD, index=df.index)
    prev_fast = df[fast_col].shift(1)
    prev_slow = df[slow_col].shift(1)

    golden = (df[fast_col] > df[slow_col]) & (prev_fast <= prev_slow)
    death  = (df[fast_col] < df[slow_col]) & (prev_fast >= prev_slow)

    sig[golden] = BUY
    sig[death]  = SELL
    return sig


def _macd_signal(df: pd.DataFrame) -> pd.Series:
    """MACD histogram sign-change signal."""
    sig = pd.Series(HOLD, index=df.index)
    prev_hist = df["histogram"].shift(1)

    bullish = (df["histogram"] > 0) & (prev_hist <= 0)
    bearish = (df["histogram"] < 0) & (prev_hist >= 0)

    sig[bullish] = BUY
    sig[bearish] = SELL
    return sig


def _stoch_signal(df: pd.DataFrame,
                  oversold: float = 20, overbought: float = 80) -> pd.Series:
    """Stochastic %K/%D crossover in extreme zones."""
    sig = pd.Series(HOLD, index=df.index)
    k, d = df["stoch_k"], df["stoch_d"]
    prev_k, prev_d = k.shift(1), d.shift(1)

    buy_zone  = (k < oversold)  & (k > d) & (prev_k <= prev_d)
    sell_zone = (k > overbought) & (k < d) & (prev_k >= prev_d)

    sig[buy_zone]  = BUY
    sig[sell_zone] = SELL
    return sig


# ─────────────────────────────────────────────
#  Composite Signal Generator
# ─────────────────────────────────────────────

def generate_signals(df: pd.DataFrame,
                     weights: dict = None,
                     threshold: float = 0.4) -> pd.DataFrame:
    """
    Combine multiple indicator signals via weighted voting.

    Default weights assign equal importance to each component.
    A row is flagged BUY if weighted_score >= +threshold,
    SELL if <= -threshold, else HOLD.

    Args:
        df        : DataFrame with all indicators added.
        weights   : Dict of component weights. Keys:
                    'rsi', 'bb', 'ma_cross', 'macd', 'stoch'
        threshold : Minimum absolute score to generate a signal.

    Returns:
        df with extra columns: signal, signal_score,
        rsi_sig, bb_sig, ma_sig, macd_sig, stoch_sig
    """
    df = df.copy()

    if weights is None:
        weights = {"rsi": 0.25, "bb": 0.20, "ma_cross": 0.25,
                   "macd": 0.15, "stoch": 0.15}

    # Component signals
    df["rsi_sig"]   = _rsi_signal(df)
    df["bb_sig"]    = _bb_signal(df)
    df["ma_sig"]    = _ma_crossover_signal(df)
    df["macd_sig"]  = _macd_signal(df)
    df["stoch_sig"] = _stoch_signal(df)

    # Weighted score (−1 to +1 range)
    score = (
        df["rsi_sig"]   * weights["rsi"]      +
        df["bb_sig"]    * weights["bb"]        +
        df["ma_sig"]    * weights["ma_cross"]  +
        df["macd_sig"]  * weights["macd"]      +
        df["stoch_sig"] * weights["stoch"]
    )
    df["signal_score"] = score.round(4)

    # Final signal
    df["signal"] = HOLD
    df.loc[score >=  threshold, "signal"] = BUY
    df.loc[score <= -threshold, "signal"] = SELL

    n_buy  = (df["signal"] == BUY).sum()
    n_sell = (df["signal"] == SELL).sum()
    print(f"[Strategy] Signals generated — BUY: {n_buy} | SELL: {n_sell}")
    return df


# ─────────────────────────────────────────────
#  Latest Signal Summary
# ─────────────────────────────────────────────

def latest_signal(df: pd.DataFrame) -> dict:
    """Return the most recent trading signal and its context."""
    row  = df.iloc[-1]
    sig  = int(row["signal"])
    label = {BUY: "🟢 BUY", SELL: "🔴 SELL", HOLD: "⚪ HOLD"}[sig]

    return {
        "date":         str(df.index[-1].date()),
        "signal":       label,
        "score":        round(float(row["signal_score"]), 4),
        "close":        round(float(row["close"]), 4),
        "rsi14":        round(float(row["rsi14"]), 2),
        "adx":          round(float(row["adx"]), 2),
        "bb_pct":       round(float(row["bb_pct"]), 3),
        "macd_hist":    round(float(row["histogram"]), 4),
        "above_ma50":   bool(row["close"] > row["ma50"]),
        "above_ma200":  bool(row["close"] > row["ma200"]),
    }


def print_signal(info: dict) -> None:
    """Pretty-print the latest signal."""
    print("\n" + "─" * 45)
    print(f"  LATEST SIGNAL  ({info['date']})")
    print("─" * 45)
    print(f"  {info['signal']}  (score: {info['score']:+.4f})")
    print(f"  Close:       ${info['close']:,.4f}")
    print(f"  RSI-14:      {info['rsi14']:.1f}")
    print(f"  ADX:         {info['adx']:.1f}")
    print(f"  BB %B:       {info['bb_pct']:.3f}")
    print(f"  MACD Hist:   {info['macd_hist']:+.4f}")
    print(f"  Above MA50:  {'✅' if info['above_ma50']  else '❌'}")
    print(f"  Above MA200: {'✅' if info['above_ma200'] else '❌'}")
    print("─" * 45 + "\n")
