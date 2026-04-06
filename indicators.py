"""
indicators.py — Technical Analysis Module
Computes professional-grade indicators using pandas/numpy only (no ta-lib dependency).
"""

import pandas as pd
import numpy as np


# ══════════════════════════════════════════════
#  TREND INDICATORS
# ══════════════════════════════════════════════

def sma(series: pd.Series, window: int) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window).mean()


def ema(series: pd.Series, span: int) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=span, adjust=False).mean()


def macd(series: pd.Series,
         fast: int = 12, slow: int = 26, signal: int = 9
         ) -> pd.DataFrame:
    """
    MACD — Moving Average Convergence Divergence.

    Returns DataFrame with columns:
        macd_line, signal_line, histogram
    """
    ema_fast   = ema(series, fast)
    ema_slow   = ema(series, slow)
    macd_line  = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram   = macd_line - signal_line
    return pd.DataFrame({
        "macd_line":   macd_line,
        "signal_line": signal_line,
        "histogram":   histogram,
    })


# ══════════════════════════════════════════════
#  MOMENTUM INDICATORS
# ══════════════════════════════════════════════

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Relative Strength Index (Wilder's smoothing).
    Values: 0-100. Overbought > 70, Oversold < 30.
    """
    delta = series.diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def stochastic(high: pd.Series, low: pd.Series, close: pd.Series,
               k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
    """
    Stochastic Oscillator (%K and %D).

    Returns DataFrame with columns: stoch_k, stoch_d
    """
    lowest_low   = low.rolling(k_period).min()
    highest_high = high.rolling(k_period).max()

    stoch_k = 100 * (close - lowest_low) / (highest_high - lowest_low + 1e-10)
    stoch_d = stoch_k.rolling(d_period).mean()

    return pd.DataFrame({"stoch_k": stoch_k, "stoch_d": stoch_d})


# ══════════════════════════════════════════════
#  VOLATILITY INDICATORS
# ══════════════════════════════════════════════

def bollinger_bands(series: pd.Series,
                    window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    """
    Bollinger Bands.

    Returns DataFrame with: bb_middle, bb_upper, bb_lower, bb_width, bb_pct
    """
    middle = series.rolling(window).mean()
    std    = series.rolling(window).std()

    upper  = middle + num_std * std
    lower  = middle - num_std * std
    width  = (upper - lower) / middle          # normalised band width
    pct    = (series - lower) / (upper - lower + 1e-10)  # %B oscillator

    return pd.DataFrame({
        "bb_middle": middle,
        "bb_upper":  upper,
        "bb_lower":  lower,
        "bb_width":  width,
        "bb_pct":    pct,
    })


def atr(high: pd.Series, low: pd.Series, close: pd.Series,
        period: int = 14) -> pd.Series:
    """
    Average True Range — measures market volatility.
    """
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low  - prev_close).abs(),
    ], axis=1).max(axis=1)

    return tr.ewm(alpha=1 / period, adjust=False).mean()


# ══════════════════════════════════════════════
#  TREND STRENGTH
# ══════════════════════════════════════════════

def adx(high: pd.Series, low: pd.Series, close: pd.Series,
        period: int = 14) -> pd.DataFrame:
    """
    Average Directional Index — measures trend strength (not direction).
    ADX > 25 = strong trend; ADX < 20 = weak / ranging market.

    Returns DataFrame with: adx, plus_di, minus_di
    """
    prev_high  = high.shift(1)
    prev_low   = low.shift(1)
    prev_close = close.shift(1)

    plus_dm  = np.where((high - prev_high) > (prev_low - low),
                        np.maximum(high - prev_high, 0), 0)
    minus_dm = np.where((prev_low - low) > (high - prev_high),
                        np.maximum(prev_low - low, 0), 0)

    plus_dm  = pd.Series(plus_dm, index=high.index)
    minus_dm = pd.Series(minus_dm, index=high.index)

    atr_val   = atr(high, low, close, period)
    plus_di   = 100 * plus_dm.ewm(alpha=1/period, adjust=False).mean() / (atr_val + 1e-10)
    minus_di  = 100 * minus_dm.ewm(alpha=1/period, adjust=False).mean() / (atr_val + 1e-10)

    dx        = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di + 1e-10)
    adx_val   = dx.ewm(alpha=1/period, adjust=False).mean()

    return pd.DataFrame({
        "adx":      adx_val,
        "plus_di":  plus_di,
        "minus_di": minus_di,
    })


# ══════════════════════════════════════════════
#  Composite: add ALL indicators to DataFrame
# ══════════════════════════════════════════════

def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mutates (copies) df by appending all technical indicator columns.
    Expects df to have: open, high, low, close, volume
    """
    df = df.copy()
    c, h, l = df["close"], df["high"], df["low"]

    # Trend
    df["ma20"]  = sma(c, 20)
    df["ma50"]  = sma(c, 50)
    df["ma200"] = sma(c, 200)
    df["ema12"] = ema(c, 12)
    df["ema26"] = ema(c, 26)

    macd_df = macd(c)
    df = pd.concat([df, macd_df], axis=1)

    # Momentum
    df["rsi14"] = rsi(c, 14)
    stoch_df = stochastic(h, l, c)
    df = pd.concat([df, stoch_df], axis=1)

    # Volatility
    bb_df = bollinger_bands(c)
    df = pd.concat([df, bb_df], axis=1)
    df["atr14"] = atr(h, l, c, 14)

    # Trend strength
    adx_df = adx(h, l, c)
    df = pd.concat([df, adx_df], axis=1)

    print(f"[Indicators] Added {len(df.columns)} columns total.")
    return df
