# ⬡ QuantDesk — Advanced Market Analysis Tool

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)

**A professional-grade quantitative market analysis suite built in Python.**  
Modular, extensible, and designed to work like a real hedge-fund quant tool.

[Features](#-features) · [Quickstart](#-quickstart) · [Usage](#-usage) · [Modules](#-modules) · [Customisation](#-customisation) · [Output](#-output)

</div>

---

## 📌 Overview

QuantDesk is a modular Python toolkit that combines **technical analysis**, **statistical risk metrics**, **machine learning price prediction**, **backtesting**, and **interactive visualisation** into a single pipeline — runnable with one command.

It supports any asset tradeable on Yahoo Finance: equities, ETFs, crypto, commodities, and indices.

```bash
python main.py TSLA 3y 1d
```

That single command will:

1. Download 3 years of Tesla daily OHLCV data from Yahoo Finance
2. Compute 12+ professional technical indicators (RSI, MACD, Bollinger, ADX…)
3. Run full statistical risk analysis (Sharpe, Sortino, Calmar, VaR, CVaR, drawdown…)
4. Generate BUY / HOLD / SELL signals using a weighted multi-indicator scoring engine
5. Backtest the strategy vs buy-and-hold with commission + slippage
6. Train a Random Forest and Linear Regression price prediction model
7. Run a 500-path Monte Carlo simulation over a 252-day horizon
8. Export an interactive self-contained HTML dashboard with 7 professional charts

---

## ✨ Features

| Module | What it does |
|---|---|
| `data_loader.py` | Fetches OHLCV from Yahoo Finance; handles missing values; computes returns and rolling stats |
| `indicators.py` | SMA, EMA, MACD, RSI, Stochastic, Bollinger Bands, ATR, ADX — pure pandas/numpy, no ta-lib |
| `stats.py` | Sharpe, Sortino, Calmar, VaR 95%, CVaR, max drawdown, skewness, kurtosis |
| `strategy.py` | Weighted multi-indicator signal engine → BUY / HOLD / SELL |
| `backtest.py` | Vectorised backtester with commission + slippage, benchmarked vs buy-and-hold |
| `ml_model.py` | Random Forest + Linear Regression with time-series CV; Monte Carlo (GBM) |
| `visualization.py` | 7 Plotly charts saved to a single self-contained HTML dashboard |
| `main.py` | Master orchestrator — chains everything with one CLI call |

---

## 🚀 Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/your-username/quantdesk.git
cd quantdesk
```

### 2. Create a virtual environment (recommended)

```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run your first analysis

```bash
python main.py AAPL 2y 1d
```

When it finishes, open `dashboard.html` in your browser to explore the full interactive dashboard.

---

## 📦 Requirements

```
Python        3.9+
yfinance      >= 0.2.36
pandas        >= 2.0.0
numpy         >= 1.24.0
scikit-learn  >= 1.3.0
plotly        >= 5.18.0
matplotlib    >= 3.7.0
seaborn       >= 0.13.0
```

Install everything at once:

```bash
pip install yfinance pandas numpy scikit-learn plotly matplotlib seaborn
```

---

## 🖥️ Usage

### Basic syntax

```bash
python main.py [TICKER] [PERIOD] [INTERVAL]
```

| Argument | Description | Available options | Default |
|---|---|---|---|
| `TICKER` | Asset symbol | `AAPL`, `TSLA`, `NVDA`, `BTC-USD`, `SPY`, `GLD`, any Yahoo Finance symbol | `AAPL` |
| `PERIOD` | Lookback window | `1y` `2y` `3y` `5y` `10y` `max` | `2y` |
| `INTERVAL` | Bar frequency | `1d` (daily) · `1wk` (weekly) · `1mo` (monthly) | `1d` |

### Examples

```bash
# Apple — 2 years daily (uses all defaults)
python main.py

# Tesla — 3 years daily
python main.py TSLA 3y 1d

# Bitcoin — 5 years weekly
python main.py BTC-USD 5y 1wk

# S&P 500 ETF — 10 years daily
python main.py SPY 10y 1d

# Gold ETF — 1 year daily
python main.py GLD 1y 1d

# Ethereum — max available history, weekly bars
python main.py ETH-USD max 1wk

# NVIDIA — 3 years daily
python main.py NVDA 3y 1d
```

### Use as a Python library

You can import and use individual modules directly in your own scripts:

```python
from data_loader import load
from indicators import add_all_indicators
from strategy import generate_signals, latest_signal, print_signal
from stats import market_statistics, print_statistics

# 1. Load and preprocess data
df = load("NVDA", period="2y", interval="1d")

# 2. Add all technical indicators
df = add_all_indicators(df)

# 3. Generate signals
df = generate_signals(df)

# 4. Read the latest signal
signal = latest_signal(df)
print_signal(signal)

# 5. Print full statistical report
stats = market_statistics(df, "NVDA")
print_statistics(stats)
```

Or run the complete pipeline programmatically and access all results:

```python
from main import run_analysis

results = run_analysis(
    ticker="NVDA",
    period="2y",
    interval="1d",
    output_html="nvda_report.html"
)

# All results are returned in a dict
print(results["market_stats"])     # risk metrics dict
print(results["latest_signal"])    # current BUY/SELL/HOLD
print(results["bt_metrics"])       # backtest performance
print(results["future_preds"])     # 10-day ML forecast (pd.Series)
print(results["mc_summary"])       # Monte Carlo summary
```

---

## 📁 Modules

### `data_loader.py`

Downloads OHLCV data from Yahoo Finance, cleans it, and computes foundational return features.

```python
from data_loader import load, fetch_market_data, preprocess

# All-in-one convenience wrapper
df = load("AAPL", period="2y", interval="1d", rolling_window=20)

# Step-by-step
raw = fetch_market_data("AAPL", period="2y", interval="1d")
df  = preprocess(raw, rolling_window=20)
```

**Columns added by preprocessing:**

| Column | Description |
|---|---|
| `daily_return` | Simple percentage return: `(close_t / close_{t-1}) − 1` |
| `log_return` | Natural log return: `ln(close_t / close_{t-1})` |
| `rolling_mean_N` | Rolling mean of close over N days |
| `rolling_std_N` | Rolling standard deviation of close over N days |
| `close_norm` | Min-max normalised close price (0 to 1 range) |

---

### `indicators.py`

Computes all indicators using pure pandas and numpy — no ta-lib installation required.

```python
from indicators import add_all_indicators, sma, ema, rsi, macd, bollinger_bands, atr, adx

# Append all indicators to a DataFrame in one call
df = add_all_indicators(df)

# Or call individual functions
df["rsi14"]  = rsi(df["close"], period=14)
df["ema50"]  = ema(df["close"], span=50)
macd_df      = macd(df["close"], fast=12, slow=26, signal=9)
bb_df        = bollinger_bands(df["close"], window=20, num_std=2.0)
atr_series   = atr(df["high"], df["low"], df["close"], period=14)
adx_df       = adx(df["high"], df["low"], df["close"], period=14)
```

**Full indicator reference:**

| Indicator | Output column(s) | Notes |
|---|---|---|
| SMA 20 | `ma20` | Simple Moving Average, 20-period |
| SMA 50 | `ma50` | Simple Moving Average, 50-period |
| SMA 200 | `ma200` | Simple Moving Average, 200-period |
| EMA 12 | `ema12` | Exponential Moving Average |
| EMA 26 | `ema26` | Exponential Moving Average |
| MACD | `macd_line`, `signal_line`, `histogram` | 12/26/9 default |
| RSI | `rsi14` | Wilder's smoothing, 14-period |
| Stochastic | `stoch_k`, `stoch_d` | %K 14-period, %D 3-period smooth |
| Bollinger Bands | `bb_upper`, `bb_middle`, `bb_lower`, `bb_width`, `bb_pct` | 20-period, ±2σ |
| ATR | `atr14` | Average True Range, 14-period |
| ADX | `adx`, `plus_di`, `minus_di` | Trend strength + directional indicators |

---

### `stats.py`

Computes a comprehensive suite of professional risk and return metrics.

```python
from stats import market_statistics, print_statistics, correlation_matrix

# Single asset report
stats = market_statistics(df, ticker="AAPL")
print_statistics(stats)

# Multi-asset return correlation
dfs  = {"AAPL": df_aapl, "TSLA": df_tsla, "BTC-USD": df_btc}
corr = correlation_matrix(dfs)
print(corr.round(3))
```

**Metrics computed:**

| Metric | Formula / Description |
|---|---|
| Annualised Return | Compound annual growth rate over the full period |
| Annualised Volatility | `daily_std × √252` |
| Sharpe Ratio | `(Ann. return − 5% Rf) / Ann. vol` |
| Sortino Ratio | `(Ann. return − Rf) / Downside vol` (penalises only losses) |
| Calmar Ratio | `Ann. return / |Max Drawdown|` |
| Max Drawdown | Largest peak-to-trough price decline |
| VaR 95% | 5th percentile of the daily return distribution |
| CVaR 95% | Mean return of all days beyond the VaR threshold |
| Skewness | Asymmetry of return distribution |
| Excess Kurtosis | Fat-tail measure relative to a normal distribution |

---

### `strategy.py`

Generates BUY / HOLD / SELL signals using a configurable weighted voting system.

```python
from strategy import generate_signals, latest_signal, print_signal

# With default weights and threshold
df = generate_signals(df)

# With custom weights (must sum to 1.0) and custom threshold
df = generate_signals(df, weights={
    "rsi":      0.30,
    "bb":       0.20,
    "ma_cross": 0.25,
    "macd":     0.15,
    "stoch":    0.10,
}, threshold=0.40)

# Print latest signal to console
signal = latest_signal(df)
print_signal(signal)
```

**Signal logic — how each component votes:**

| Component | BUY trigger | SELL trigger |
|---|---|---|
| RSI | RSI-14 < 30 (oversold) | RSI-14 > 70 (overbought) |
| Bollinger Bands | Price touches or breaks below lower band | Price touches or breaks above upper band |
| MA Crossover | MA50 crosses above MA200 — Golden Cross | MA50 crosses below MA200 — Death Cross |
| MACD | Histogram crosses from negative to positive | Histogram crosses from positive to negative |
| Stochastic | %K crosses above %D while both are in oversold zone (<20) | %K crosses below %D while both are in overbought zone (>80) |

Each component contributes its weight to a composite `signal_score` in the range `[−1, +1]`:
- Score ≥ `threshold` → **BUY**
- Score ≤ `−threshold` → **SELL**
- Otherwise → **HOLD**

---

### `backtest.py`

Simulates trading based on generated signals with realistic cost modelling.

```python
from backtest import run_backtest, backtest_metrics, print_backtest

df_bt, trade_log = run_backtest(
    df,
    initial_capital=100_000,   # USD
    commission_pct=0.001,      # 0.1% per trade side
    slippage_pct=0.0005,       # 0.05% price impact
)

metrics = backtest_metrics(df_bt, trade_log)
print_backtest(metrics)
```

**Rules applied during simulation:**
- Fully invested (100% of capital) on each BUY signal
- Full liquidation on each SELL signal
- No short selling
- Commission + slippage applied on every entry and exit

**Metrics output:**

| Metric | Description |
|---|---|
| Strategy Total Return | Cumulative return of the signal-driven strategy |
| Buy-and-Hold Return | Passive benchmark — buy at start, hold to end |
| Strategy Ann. Return | Compounded annual growth rate of strategy |
| Sharpe Ratio | Risk-adjusted return of the strategy |
| Max Drawdown | Largest equity peak-to-trough decline |
| Number of Trades | Total completed round-trips |
| Win Rate | Percentage of trades closed at a profit |
| Profit Factor | Gross profit divided by gross loss |

---

### `ml_model.py`

Trains price prediction models using technical indicators as features, with Monte Carlo simulation.

```python
from ml_model import train_and_evaluate, predict_future, monte_carlo, monte_carlo_summary

# Train both models and evaluate on held-out test set
results = train_and_evaluate(df, target_horizon=5, test_size=0.2)

# Generate a multi-day forward forecast
future = predict_future(df, results, n_days=10)
print(future)
# Output:
# 2025-01-06    189.42
# 2025-01-07    190.11
# ...

# Monte Carlo price path simulation
mc_df   = monte_carlo(df, n_simulations=500, n_days=252)
summary = monte_carlo_summary(mc_df, confidence=0.95)
# Returns: mean_price, median_price, lower_bound (5%), upper_bound (95%), prob_up
```

**Key design decisions:**
- Test set is always the most recent 20% — no data leakage
- Features include 1-day and 5-day lags to avoid look-ahead bias
- The better-performing model (lower MAE) is automatically selected for forecasting
- Monte Carlo uses Geometric Brownian Motion calibrated on historical log-return mean and std

---

### `visualization.py`

Generates 7 professional interactive charts and saves them to a single self-contained HTML file.

```python
from visualization import (
    candlestick_chart, momentum_chart, equity_curve_chart,
    prediction_chart, monte_carlo_chart, return_distribution_chart,
    feature_importance_chart, save_all_charts,
)

charts = []
charts.append(("Price",       candlestick_chart(df, "AAPL")))
charts.append(("Momentum",    momentum_chart(df, "AAPL")))
charts.append(("Equity",      equity_curve_chart(df_bt, "AAPL")))
charts.append(("Returns",     return_distribution_chart(df, "AAPL")))
charts.append(("ML Forecast", prediction_chart(df, ml_results, future_preds, "AAPL")))
charts.append(("Monte Carlo", monte_carlo_chart(df, mc_df, mc_summary, "AAPL")))
charts.append(("Features",    feature_importance_chart(ml_results, "AAPL")))

save_all_charts(charts, "dashboard.html")
```

| Chart | Contents |
|---|---|
| Candlestick | OHLC candles + MA20/50/200 + Bollinger Bands + volume bars + MACD + BUY/SELL signal markers |
| Momentum | RSI-14 with overbought/oversold bands + Stochastic %K/%D + ADX/±DI with trend threshold |
| Equity Curve | Strategy vs Buy-and-Hold normalised to 100 + drawdown area chart |
| Return Distribution | Daily return histogram + mean line + VaR 95% marker |
| ML Prediction | Actual price + test-set predictions + 10-day forward forecast |
| Monte Carlo | 500 GBM price paths + 5th / 50th / 95th percentile bands |
| Feature Importance | Top 15 Random Forest feature importance scores (horizontal bar chart) |

---

## 🎛️ Customisation

### Change the default ticker, period, or interval

Edit the bottom of `main.py`:

```python
if __name__ == "__main__":
    run_analysis(
        ticker="BTC-USD",   # ← change to any Yahoo Finance symbol
        period="5y",        # ← 1y, 2y, 3y, 5y, 10y, max
        interval="1wk",     # ← 1d, 1wk, 1mo
        output_html="dashboard.html",
    )
```

---

### Add a new technical indicator

**Step 1.** Define the function in `indicators.py`:

```python
def vwap(df: pd.DataFrame) -> pd.Series:
    """Volume Weighted Average Price — resets daily."""
    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    return (typical_price * df["volume"]).cumsum() / df["volume"].cumsum()
```

**Step 2.** Register it inside `add_all_indicators()`:

```python
def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # ... existing lines ...
    df["vwap"] = vwap(df)   # ← add this line
    return df
```

The new column will automatically be available to the signal engine, backtester, and ML model.

---

### Add a new trading signal rule

**Step 1.** Add a signal function in `strategy.py`:

```python
def _vwap_signal(df: pd.DataFrame) -> pd.Series:
    """Price below VWAP → bullish; above VWAP → bearish."""
    sig = pd.Series(HOLD, index=df.index)
    sig[df["close"] < df["vwap"]] = BUY
    sig[df["close"] > df["vwap"]] = SELL
    return sig
```

**Step 2.** Add it to `generate_signals()` with a weight. Make sure all weights still sum to 1.0:

```python
def generate_signals(df, weights=None, threshold=0.4):
    if weights is None:
        weights = {
            "rsi":      0.22,
            "bb":       0.18,
            "ma_cross": 0.22,
            "macd":     0.13,
            "stoch":    0.13,
            "vwap":     0.12,   # ← new component
        }

    df["vwap_sig"] = _vwap_signal(df)   # ← compute

    score = (
        df["rsi_sig"]   * weights["rsi"]      +
        df["bb_sig"]    * weights["bb"]        +
        df["ma_sig"]    * weights["ma_cross"]  +
        df["macd_sig"]  * weights["macd"]      +
        df["stoch_sig"] * weights["stoch"]     +
        df["vwap_sig"]  * weights["vwap"]      # ← include
    )
    # ... rest of function unchanged ...
```

---

### Tune signal sensitivity

```python
# More signals — lower threshold (looser filter)
df = generate_signals(df, threshold=0.25)

# Fewer, higher-conviction signals — higher threshold
df = generate_signals(df, threshold=0.55)
```

A good practice is to plot the signal count at different thresholds against backtest win rate to find the optimal value for your asset.

---

### Change the ML model

Open `ml_model.py` and replace the model inside `train_and_evaluate()`:

```python
# Option A: Gradient Boosting
from sklearn.ensemble import GradientBoostingRegressor
rf = GradientBoostingRegressor(n_estimators=300, max_depth=5,
                                learning_rate=0.05, random_state=42)

# Option B: XGBoost (requires: pip install xgboost)
from xgboost import XGBRegressor
rf = XGBRegressor(n_estimators=300, max_depth=5,
                   learning_rate=0.05, random_state=42)

# Option C: Support Vector Regression
from sklearn.svm import SVR
rf = SVR(kernel="rbf", C=100, gamma=0.01, epsilon=0.1)
```

Change the prediction horizon:

```python
# Predict 10 trading days ahead instead of 5
results = train_and_evaluate(df, target_horizon=10)
```

---

### Change backtest capital or transaction costs

```python
df_bt, log = run_backtest(
    df,
    initial_capital=50_000,    # starting portfolio value in USD
    commission_pct=0.0025,     # 0.25% — typical crypto exchange fee
    slippage_pct=0.001,        # 0.1% price impact
)
```

---

### Run a multi-asset portfolio correlation

```python
from data_loader import load
from stats import correlation_matrix

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "BTC-USD"]
dfs     = {t: load(t, period="2y") for t in tickers}
corr    = correlation_matrix(dfs)
print(corr.round(3))
```

---

### Adjust Monte Carlo parameters

```python
from ml_model import monte_carlo, monte_carlo_summary

mc_df = monte_carlo(
    df,
    n_simulations=1000,   # more paths = smoother distribution
    n_days=504,           # 2-year forecast horizon (504 trading days ≈ 2y)
)

summary = monte_carlo_summary(mc_df, confidence=0.90)  # 90% confidence interval
```

---

## 📊 Output

### Console output example

```
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ADVANCED MARKET ANALYSIS TOOL
  Ticker: TSLA  |  Period: 3y  |  Interval: 1d
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

══════════════════════════════════════════════════════
  MARKET STATISTICS — TSLA
══════════════════════════════════════════════════════
  Period                   2022-01-03  →  2025-01-02
  Trading Days             756
  Current Price            $248.5100
  Annualised Return        +18.40 %
  Annualised Volatility    55.20 %
  Sharpe Ratio             0.241
  Sortino Ratio            0.318
  Max Drawdown             -73.60 %
  VaR 95 %                 -3.41 %
  CVaR 95 %                -5.20 %
══════════════════════════════════════════════════════

  LATEST SIGNAL  (2025-01-02)
  ─────────────────────────────────────────────
  🟢 BUY  (score: +0.5500)
  Close:       $248.5100
  RSI-14:      28.4
  ADX:         34.2
  BB %B:       0.062
  Above MA50:  ❌
  Above MA200: ✅

══════════════════════════════════════════════════════
  BACKTEST RESULTS
══════════════════════════════════════════════════════
  Strategy Total Return    +42.80 %
  Buy-and-Hold Return      +28.10 %
  Sharpe Ratio             0.840
  Max Drawdown (Strategy)  -24.30 %
  Number of Trades         18
  Win Rate                 58.3 %
  Profit Factor            1.840
  Final Portfolio Value    $142,800.00
══════════════════════════════════════════════════════

  [ML Model]  MAE=4.2140  RMSE=6.8830  (Random Forest selected)

  Future price predictions (next 10 trading days):
    2025-01-06  →  $251.3200
    2025-01-07  →  $253.8800
    ...
```

### `dashboard.html`

A fully self-contained interactive HTML file — no server, no internet connection required after generation. Open it in any modern browser.

---

## 🗂️ Project Structure

```
quantdesk/
│
├── data_loader.py       # Data collection & preprocessing
├── indicators.py        # Technical analysis indicators
├── stats.py             # Statistical risk & return metrics
├── strategy.py          # Multi-indicator signal engine
├── backtest.py          # Strategy simulation & evaluation
├── ml_model.py          # ML price prediction + Monte Carlo
├── visualization.py     # Interactive Plotly chart dashboard
├── main.py              # CLI entry point & pipeline orchestrator
├── requirements.txt     # Python dependencies
└── README.md
```

---

## ⚠️ Disclaimer

This project is intended for **educational and research purposes only**.

Nothing in this repository constitutes financial advice, investment advice, or a recommendation to buy or sell any security. Past performance of any backtested strategy does not guarantee future results. Always conduct your own due diligence before making any investment decision.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — free to use, modify, and distribute, including for commercial purposes, with attribution.

---

## 🤝 Contributing

Contributions are welcome. To propose a new feature or fix:

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-feature`
3. Make your changes with clear docstrings and inline comments
4. Test with at least two different tickers
5. Open a pull request with a concise description of what you changed and why

---

<div align="center">

Built with Python · Data from Yahoo Finance · Charts by Plotly

</div>
