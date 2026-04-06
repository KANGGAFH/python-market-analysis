"""
data_loader.py — Market Data Collection Module
Fetches OHLCV data from yfinance and preprocesses it for analysis.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────
#  Core Data Fetcher
# ─────────────────────────────────────────────

def fetch_market_data(ticker: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    """
    Download OHLCV data from Yahoo Finance.

    Args:
        ticker   : Asset symbol, e.g. 'AAPL', 'BTC-USD', 'TSLA'
        period   : Lookback window — '1y', '2y', '5y', '10y', 'max'
        interval : Bar size — '1d' (daily), '1wk' (weekly), '1mo' (monthly)

    Returns:
        Cleaned pandas DataFrame with DatetimeIndex.
    """
    print(f"[DataLoader] Fetching {ticker} | period={period} | interval={interval}")
    raw = yf.download(ticker, period=period, interval=interval, auto_adjust=True, progress=False)

    if raw.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'. Check symbol and network.")

    # Flatten MultiIndex columns if present (yfinance ≥ 0.2)
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    # Standardise column names
    raw.columns = [c.lower().replace(" ", "_") for c in raw.columns]

    # Keep only the columns we care about
    cols_wanted = [c for c in ["open", "high", "low", "close", "volume"] if c in raw.columns]
    df = raw[cols_wanted].copy()
    df.index.name = "date"
    df.index = pd.to_datetime(df.index)

    print(f"[DataLoader] Retrieved {len(df)} rows  ({df.index[0].date()} → {df.index[-1].date()})")
    return df


# ─────────────────────────────────────────────
#  Preprocessing
# ─────────────────────────────────────────────

def preprocess(df: pd.DataFrame, rolling_window: int = 20) -> pd.DataFrame:
    """
    Clean and enrich raw OHLCV data.

    Steps:
      1. Forward-fill missing values (weekends / holidays)
      2. Daily simple returns and log-returns
      3. Rolling mean & rolling std (volatility proxy)
      4. Normalised close price (min-max, 0-1 range)

    Args:
        df             : Raw OHLCV DataFrame
        rolling_window : Window size for rolling statistics (default 20 trading days)

    Returns:
        Enriched DataFrame.
    """
    df = df.copy()

    # 1. Handle missing values — forward fill then back fill any leading NaNs
    df.ffill(inplace=True)
    df.bfill(inplace=True)

    # 2. Return series
    df["daily_return"]  = df["close"].pct_change()
    df["log_return"]    = np.log(df["close"] / df["close"].shift(1))

    # 3. Rolling statistics on close price
    df[f"rolling_mean_{rolling_window}"] = df["close"].rolling(rolling_window).mean()
    df[f"rolling_std_{rolling_window}"]  = df["close"].rolling(rolling_window).std()

    # 4. Min-max normalisation (useful for ML feature scaling)
    price_min = df["close"].min()
    price_max = df["close"].max()
    df["close_norm"] = (df["close"] - price_min) / (price_max - price_min)

    df.dropna(subset=["daily_return"], inplace=True)
    print(f"[DataLoader] Preprocessing done — {len(df)} usable rows.")
    return df


# ─────────────────────────────────────────────
#  Convenience wrapper
# ─────────────────────────────────────────────

def load(ticker: str, period: str = "2y", interval: str = "1d",
         rolling_window: int = 20) -> pd.DataFrame:
    """Single call: fetch + preprocess."""
    raw = fetch_market_data(ticker, period, interval)
    return preprocess(raw, rolling_window)
