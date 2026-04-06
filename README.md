<div align="center">

```
╔═══════════════════════════════════════════════════════════╗
║         A D V A N C E D   M A R K E T   A N A L Y S I S ║
║                    T O O L  ·  v1.0.0                    ║
╚═══════════════════════════════════════════════════════════╝
```

**Professional-grade quantitative analysis suite for stocks & crypto**  
Built with the methodology of a hedge-fund quant desk

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=flat-square&logo=pandas)](https://pandas.pydata.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-f7931e?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3f4f75?style=flat-square&logo=plotly)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 📋 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Fitur Utama](#-fitur-utama)
- [Struktur Project](#-struktur-project)
- [Instalasi](#-instalasi)
- [Quick Start](#-quick-start)
- [Cara Penggunaan Lengkap](#-cara-penggunaan-lengkap)
- [Kustomisasi](#-kustomisasi)
- [Output Program](#-output-program)
- [Penjelasan Setiap Modul](#-penjelasan-setiap-modul)
- [Contoh Hasil](#-contoh-hasil)
- [FAQ & Troubleshooting](#-faq--troubleshooting)
- [Kontribusi](#-kontribusi)

---

## 🎯 Tentang Proyek

**Advanced Market Analysis Tool** adalah framework analisis pasar saham dan cryptocurrency berbasis Python yang dirancang menggunakan metodologi kuantitatif profesional. Tool ini mengintegrasikan teknikal analisis, statistik keuangan, machine learning, dan backtesting dalam satu pipeline yang modular dan mudah dikembangkan.

> ⚠️ **Disclaimer:** Tool ini dibuat untuk tujuan edukasi dan riset. Bukan merupakan saran investasi. Selalu lakukan due diligence sebelum mengambil keputusan finansial.

---

## ✨ Fitur Utama

| Modul | Fitur |
|-------|-------|
| 📥 **Data Collection** | Yahoo Finance API, OHLCV + Adjusted Close, saham & crypto |
| 🔧 **Preprocessing** | Handle missing values, daily/log returns, rolling statistics |
| 📐 **Technical Analysis** | 12+ indikator: MA, EMA, MACD, RSI, Stochastic, BB, ATR, ADX |
| 📊 **Statistical Analysis** | Sharpe, Sortino, Calmar, VaR 95%, CVaR, Max Drawdown |
| 🤖 **Machine Learning** | Linear Regression + Random Forest, feature engineering dari indikator |
| 🎲 **Monte Carlo** | 500 simulasi path GBM, confidence interval 5%-95% |
| 🚦 **Signal Engine** | Weighted-voting BUY/SELL/HOLD dari kombinasi 5 indikator |
| 🔬 **Backtesting** | Simulasi lengkap dengan komisi, slippage, equity curve |
| 📈 **Visualization** | 7 grafik Plotly interaktif dalam satu HTML dashboard |

---

## 📁 Struktur Project

```
market_analysis_tool/
│
├── 📄 main.py              # Entry point utama — jalankan ini
├── 📄 data_loader.py       # Fetch & preprocess data pasar
├── 📄 indicators.py        # Semua indikator teknikal
├── 📄 stats.py             # Statistik & risk metrics
├── 📄 strategy.py          # Signal engine BUY/SELL/HOLD
├── 📄 backtest.py          # Backtesting engine
├── 📄 ml_model.py          # ML prediction + Monte Carlo
├── 📄 visualization.py     # Chart dashboard (Plotly)
│
├── 📄 requirements.txt     # Python dependencies
└── 📄 README.md            # Dokumentasi ini
```

---

## 🛠 Instalasi

### Prasyarat

- Python **3.9** atau lebih baru
- pip (sudah termasuk di Python)
- Koneksi internet (untuk fetch data)

### Langkah Instalasi

**1. Clone repository**
```bash
git clone https://github.com/username/market-analysis-tool.git
cd market-analysis-tool
```

**2. (Opsional tapi dianjurkan) Buat virtual environment**
```bash
# Buat venv
python -m venv venv

# Aktifkan — Windows
venv\Scripts\activate

# Aktifkan — macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install yfinance pandas numpy scikit-learn plotly matplotlib seaborn
```

**4. Verifikasi instalasi**
```bash
python -c "import yfinance, pandas, numpy, sklearn, plotly; print('✅ Semua library berhasil diinstall')"
```

---

## ⚡ Quick Start

```bash
# Analisis AAPL (Apple) — 2 tahun data harian
python main.py

# Analisis Tesla — 3 tahun
python main.py TSLA 3y 1d

# Analisis Bitcoin — 5 tahun, data mingguan
python main.py BTC-USD 5y 1wk

# Analisis S&P 500 ETF — 10 tahun
python main.py SPY 10y 1d
```

Setelah selesai, buka file `dashboard.html` di browser untuk melihat grafik interaktif.

---

## 📖 Cara Penggunaan Lengkap

### Argumen Command Line

```bash
python main.py [TICKER] [PERIOD] [INTERVAL]
```

| Argumen | Deskripsi | Contoh Nilai | Default |
|---------|-----------|--------------|---------|
| `TICKER` | Simbol aset | `AAPL`, `TSLA`, `BTC-USD`, `ETH-USD`, `SPY`, `GLD` | `AAPL` |
| `PERIOD` | Rentang waktu lookback | `1y`, `2y`, `3y`, `5y`, `10y`, `max` | `2y` |
| `INTERVAL` | Ukuran bar data | `1d` (harian), `1wk` (mingguan) | `1d` |

### Contoh Penggunaan Lengkap

```bash
# ── Saham US
python main.py AAPL 2y 1d        # Apple — 2 tahun harian
python main.py MSFT 5y 1d        # Microsoft — 5 tahun harian
python main.py NVDA 3y 1d        # NVIDIA — 3 tahun harian
python main.py GOOGL 5y 1wk      # Google — 5 tahun mingguan

# ── Cryptocurrency
python main.py BTC-USD 3y 1d     # Bitcoin — 3 tahun harian
python main.py ETH-USD 2y 1d     # Ethereum — 2 tahun harian
python main.py SOL-USD 1y 1d     # Solana — 1 tahun harian

# ── ETF & Indeks
python main.py SPY 10y 1d        # S&P 500 ETF — 10 tahun
python main.py QQQ 5y 1d         # Nasdaq 100 ETF
python main.py GLD 5y 1wk        # Gold ETF — mingguan

# ── Saham Indonesia (via Yahoo Finance)
python main.py BBCA.JK 2y 1d     # Bank BCA
python main.py TLKM.JK 3y 1d     # Telkom Indonesia
python main.py ASII.JK 2y 1d     # Astra International
```

### Penggunaan sebagai Library (Import)

```python
from main import run_analysis

# Jalankan analisis dan simpan semua hasil
results = run_analysis(
    ticker      = "AAPL",
    period      = "2y",
    interval    = "1d",
    output_html = "my_dashboard.html"
)

# Akses hasil
df_signals   = results["df_signals"]       # DataFrame dengan semua indikator & sinyal
market_stats = results["market_stats"]     # Dict statistik pasar
bt_metrics   = results["bt_metrics"]       # Dict hasil backtesting
ml_results   = results["ml_results"]       # Dict model ML
future_preds = results["future_preds"]     # Series prediksi harga
mc_summary   = results["mc_summary"]       # Dict ringkasan Monte Carlo

# Contoh: cek sinyal terbaru
from strategy import latest_signal, print_signal
signal = latest_signal(df_signals)
print_signal(signal)
```

### Penggunaan Modul Secara Individual

```python
import data_loader
import indicators
import stats
import strategy

# 1. Load data
df = data_loader.load("TSLA", period="1y", interval="1d")

# 2. Tambah indikator
df = indicators.add_all_indicators(df)

# 3. Hitung statistik
market_stats = stats.market_statistics(df, ticker="TSLA")
stats.print_statistics(market_stats)

# 4. Generate sinyal
df = strategy.generate_signals(df)
info = strategy.latest_signal(df)
strategy.print_signal(info)
```

---

## 🔧 Kustomisasi

### 1. Mengganti Ticker

**Via CLI (paling mudah):**
```bash
python main.py NVDA 3y 1d
```

**Via kode — ubah default di `main.py`:**
```python
# Baris terakhir main.py
if __name__ == "__main__":
    args     = sys.argv[1:]
    ticker   = args[0] if len(args) > 0 else "NVDA"   # ← ubah di sini
    period   = args[1] if len(args) > 1 else "3y"     # ← ubah di sini
    interval = args[2] if len(args) > 2 else "1d"
```

---

### 2. Menambah Indikator Teknikal Baru

Buka `indicators.py` dan tambahkan fungsi baru:

```python
# Contoh: tambah Williams %R
def williams_r(high: pd.Series, low: pd.Series, close: pd.Series,
               period: int = 14) -> pd.Series:
    """
    Williams %R — momentum oscillator.
    Range: -100 (oversold) to 0 (overbought).
    """
    highest_high = high.rolling(period).max()
    lowest_low   = low.rolling(period).min()
    return -100 * (highest_high - close) / (highest_high - lowest_low + 1e-10)


# Lalu daftarkan di fungsi add_all_indicators():
def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # ... kode yang sudah ada ...

    # Tambahkan ini:
    df["williams_r"] = williams_r(df["high"], df["low"], df["close"])

    return df
```

---

### 3. Membuat Strategi Trading Baru

Buka `strategy.py` dan ikuti pola ini:

```python
# Step 1: Buat fungsi sinyal komponen baru
def _my_volume_signal(df: pd.DataFrame) -> pd.Series:
    """
    Volume spike signal — BUY ketika volume 2x rata-rata 20 hari
    dan harga naik; SELL ketika volume spike tapi harga turun.
    """
    sig = pd.Series(HOLD, index=df.index)
    avg_vol    = df["volume"].rolling(20).mean()
    vol_spike  = df["volume"] > (avg_vol * 2)
    price_up   = df["close"] > df["close"].shift(1)

    sig[vol_spike &  price_up] = BUY
    sig[vol_spike & ~price_up] = SELL
    return sig


# Step 2: Daftarkan ke generate_signals()
def generate_signals(df, weights=None, threshold=0.4):
    if weights is None:
        weights = {
            "rsi":       0.20,   # turunkan weight lama
            "bb":        0.15,
            "ma_cross":  0.20,
            "macd":      0.15,
            "stoch":     0.15,
            "volume":    0.15,   # ← tambahkan weight baru
        }

    df["rsi_sig"]    = _rsi_signal(df)
    df["bb_sig"]     = _bb_signal(df)
    df["ma_sig"]     = _ma_crossover_signal(df)
    df["macd_sig"]   = _macd_signal(df)
    df["stoch_sig"]  = _stoch_signal(df)
    df["volume_sig"] = _my_volume_signal(df)   # ← panggil sinyal baru

    score = (
        df["rsi_sig"]    * weights["rsi"]      +
        df["bb_sig"]     * weights["bb"]        +
        df["ma_sig"]     * weights["ma_cross"]  +
        df["macd_sig"]   * weights["macd"]      +
        df["stoch_sig"]  * weights["stoch"]     +
        df["volume_sig"] * weights["volume"]    # ← masukkan ke score
    )
    # ... sisa kode sama ...
```

---

### 4. Mengubah Parameter Backtesting

Di `main.py`, ubah parameter saat memanggil `run_backtest()`:

```python
# Temukan baris ini di main.py (Step 5)
df_bt, trade_log = backtest.run_backtest(
    df,
    initial_capital = 100_000.0,   # ← modal awal (USD)
    commission_pct  = 0.001,       # ← komisi 0.1% per trade
    slippage_pct    = 0.0005,      # ← slippage 0.05%
)
```

---

### 5. Mengubah Model Machine Learning

Di `ml_model.py`, ganti model di fungsi `train_and_evaluate()`:

```python
# Opsi A: Gradient Boosting (biasanya lebih akurat dari RF)
from sklearn.ensemble import GradientBoostingRegressor

gb = GradientBoostingRegressor(
    n_estimators   = 300,
    max_depth      = 5,
    learning_rate  = 0.05,
    random_state   = 42,
)
gb.fit(X_train_s, y_train)
gb_pred = gb.predict(X_test_s)

results["gradient_boost"] = {
    "model": gb, "scaler": scaler,
    "mae": round(mean_absolute_error(y_test, gb_pred), 4),
    "rmse": round(np.sqrt(mean_squared_error(y_test, gb_pred)), 4),
    "pred": pd.Series(gb_pred, index=y_test.index),
    "actual": y_test,
}
```

```python
# Opsi B: XGBoost (install: pip install xgboost)
from xgboost import XGBRegressor

xgb = XGBRegressor(
    n_estimators = 500,
    max_depth    = 6,
    learning_rate = 0.03,
    subsample    = 0.8,
    random_state = 42,
    verbosity    = 0,
)
```

---

### 6. Mengubah Target Prediksi ML

```python
# Di main.py, ubah target_horizon (default = 5 hari ke depan)
ml_results = ml_model.train_and_evaluate(
    df,
    target_horizon = 10,   # ← prediksi 10 hari ke depan
    test_size      = 0.2,
)

# Ubah juga jumlah hari prediksi masa depan
future_preds = ml_model.predict_future(df, ml_results, n_days=20)
```

---

### 7. Mengubah Threshold Sinyal

```python
# Di main.py (atau panggil langsung)
df = strategy.generate_signals(
    df,
    weights = {
        "rsi":      0.25,
        "bb":       0.20,
        "ma_cross": 0.25,
        "macd":     0.15,
        "stoch":    0.15,
    },
    threshold = 0.35,   # ← lebih rendah = sinyal lebih sering
                        #    lebih tinggi = sinyal lebih selektif
)
```

---

### 8. Mengubah Jumlah Simulasi Monte Carlo

```python
# Di main.py
mc_df = ml_model.monte_carlo(
    df,
    n_simulations = 1000,   # ← lebih banyak = lebih akurat tapi lebih lambat
    n_days        = 504,    # ← 2 tahun ke depan (252 hari × 2)
)
```

---

### 9. Menyimpan Dashboard dengan Nama Custom

```python
# Di main.py atau saat memanggil run_analysis()
results = run_analysis(
    ticker      = "TSLA",
    period      = "3y",
    interval    = "1d",
    output_html = "dashboard_TSLA_3y.html"   # ← nama file output
)
```

---

## 📊 Output Program

Setelah menjalankan program, Anda akan mendapatkan:

### 1. Console Output

```
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ADVANCED MARKET ANALYSIS TOOL
  Ticker: AAPL  |  Period: 2y  |  Interval: 1d
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

[DataLoader] Fetching AAPL | period=2y | interval=1d
[DataLoader] Retrieved 504 rows  (2022-01-03 → 2023-12-29)

═══════════════════════════════════════════════════════
  MARKET STATISTICS — AAPL
═══════════════════════════════════════════════════════
  Period                     2022-01-03  →  2023-12-29
  Trading Days               504
  Current Price              $192.5300
  Annualised Return          +24.80 %
  Annualised Volatility      28.60 %
  Sharpe Ratio               1.420
  Max Drawdown               -31.20 %
  VaR 95 %                   -2.43 %
═══════════════════════════════════════════════════════

  LATEST SIGNAL  (2023-12-29)
─────────────────────────────────────────────
  🟢 BUY  (score: +0.6200)
  Close:       $192.5300
  RSI-14:      48.3
  ADX:         32.1
  Above MA50:  ✅
  Above MA200: ✅
─────────────────────────────────────────────

[ML Model] Target horizon: 5 days ahead
  linear_regression      MAE=3.2100  RMSE=4.8500
  random_forest          MAE=2.4300  RMSE=3.7200
```

### 2. Dashboard HTML (`dashboard.html`)

File HTML interaktif yang berisi 7 grafik:

| # | Grafik | Konten |
|---|--------|--------|
| 1 | 📈 Price Chart | Candlestick + MA20/50/200 + Bollinger Bands + Sinyal BUY/SELL |
| 2 | ⚡ Momentum | RSI-14 + Stochastic %K/%D + ADX/±DI |
| 3 | 💰 Equity Curve | Strategy vs Buy & Hold + Drawdown |
| 4 | 🤖 ML Prediction | Prediksi RF + Forecast 10 hari ke depan |
| 5 | 🎲 Monte Carlo | 500 simulasi path harga + confidence band |
| 6 | 📊 Distribution | Histogram return harian + VaR |
| 7 | 🔍 Feature Importance | Kontribusi setiap fitur ke model RF |

---

## 🧩 Penjelasan Setiap Modul

### `data_loader.py`

Mengambil data OHLCV dari Yahoo Finance menggunakan `yfinance`. Fungsi utama:

- `fetch_market_data(ticker, period, interval)` — download raw data
- `preprocess(df, rolling_window)` — bersihkan data, hitung returns, rolling stats
- `load(ticker, period, interval)` — wrapper: fetch + preprocess dalam satu panggilan

### `indicators.py`

Implementasi murni dengan `pandas` dan `numpy` (tanpa `ta-lib`):

| Fungsi | Indikator | Keterangan |
|--------|-----------|------------|
| `sma(series, window)` | Simple MA | Rata-rata bergerak sederhana |
| `ema(series, span)` | Exponential MA | Lebih responsif terhadap perubahan terbaru |
| `macd(series)` | MACD | Fast EMA − Slow EMA + Signal + Histogram |
| `rsi(series, period)` | RSI | Wilder's smoothing; oversold<30, overbought>70 |
| `stochastic(high, low, close)` | Stoch %K/%D | Momentum oscillator zona ekstrem |
| `bollinger_bands(series)` | BB | Middle ± 2σ, %B oscillator, bandwidth |
| `atr(high, low, close)` | ATR | Volatility proxy (true range) |
| `adx(high, low, close)` | ADX/±DI | Kekuatan trend; >25 = trending market |
| `add_all_indicators(df)` | Semua | Append semua kolom indikator sekaligus |

### `stats.py`

Metrik risiko dan performa standar industri:

- **Annualised Return** — return tahunan majemuk
- **Sharpe Ratio** — return berlebih per unit risiko total
- **Sortino Ratio** — return berlebih per unit risiko downside
- **Calmar Ratio** — return tahunan / max drawdown
- **VaR 95%** — kerugian maksimal hari terburuk 5% kasus
- **CVaR 95%** — rata-rata kerugian di luar threshold VaR
- `correlation_matrix(dataframes)` — korelasi return multi-aset

### `strategy.py`

Sistem sinyal berbasis **weighted voting** dari 5 komponen:

```
SCORE = RSI×0.25 + BB×0.20 + MA_Cross×0.25 + MACD×0.15 + Stoch×0.15

SCORE ≥ +0.40  →  BUY
SCORE ≤ −0.40  →  SELL
Otherwise      →  HOLD
```

### `backtest.py`

Vectorised backtester dengan simulasi realistis:
- Fully invested (100%) saat BUY signal
- Likuidasi penuh saat SELL signal
- Komisi 0.1% + slippage 0.05% per trade
- Benchmark otomatis vs Buy-and-Hold
- Metrik: total return, Sharpe, max drawdown, win rate, profit factor

### `ml_model.py`

Pipeline ML dengan data leakage prevention:
- **Feature Engineering** — 20+ fitur dari indikator + lag 1 & 5 hari
- **Time-Series Split** — 80% train / 20% test (urutan temporal dijaga)
- **Linear Regression** — baseline model
- **Random Forest** — 200 trees, max depth 8, feature importance
- **Monte Carlo GBM** — Geometric Brownian Motion, 500 paths

### `visualization.py`

7 chart Plotly dengan dark-mode professional theme:
- Semua chart disimpan ke satu file HTML self-contained
- Tema dark `#0d1117` (GitHub dark style)
- Font `JetBrains Mono` untuk nilai numerik

---

## 🖼 Contoh Hasil

```
Contoh output untuk TSLA 3y 1d:

  Ticker:              TSLA
  Period:              2021-01-04 → 2023-12-29
  Total Return:        +48.20 %
  Annualised Return:   +14.10 %
  Annualised Vol:      65.30 %
  Sharpe Ratio:        0.320
  Max Drawdown:        -73.60 %
  
  Strategy (Backtest):
  ├── Total Return:    +31.50 %
  ├── Win Rate:        54.3 %
  ├── Max Drawdown:    -48.20 %
  └── Profit Factor:   1.42
  
  ML Prediction (Random Forest):
  ├── MAE:             $8.34
  ├── RMSE:            $12.71
  └── Best Model:      random_forest
  
  Monte Carlo (252d):
  ├── Mean:            $285.40
  ├── 5th pct:         $142.10
  ├── 95th pct:        $521.80
  └── P(price up):     58.4%
```

---

## ❓ FAQ & Troubleshooting

**Q: Error `No data returned for ticker`**

```bash
# Pastikan simbol benar. Cek di finance.yahoo.com
# Saham Indonesia pakai suffix .JK
python main.py BBCA.JK 2y 1d

# Crypto pakai suffix -USD atau -USDT
python main.py BTC-USD 2y 1d
```

**Q: Error `ModuleNotFoundError: No module named 'yfinance'`**

```bash
pip install yfinance
# atau
pip install -r requirements.txt
```

**Q: Data hanya sedikit / hasil indikator banyak NaN**

Indikator seperti MA200 butuh minimal 200 hari data. Gunakan period yang lebih panjang:
```bash
python main.py AAPL 3y 1d   # minimal 2y untuk MA200
```

**Q: ML prediction tidak akurat**

Ini normal — prediksi harga saham sangat sulit. Model ML di sini lebih berguna sebagai salah satu input sinyal, bukan oracle. Gunakan `target_horizon` yang lebih pendek (1-3 hari) untuk akurasi lebih baik.

**Q: Program berjalan lambat**

Monte Carlo dengan 500 simulasi membutuhkan waktu. Kurangi:
```python
mc_df = ml_model.monte_carlo(df, n_simulations=100, n_days=252)
```

**Q: Bagaimana cara analisis beberapa saham sekaligus?**

```python
from main import run_analysis

tickers = ["AAPL", "MSFT", "NVDA", "TSLA"]
all_results = {}

for ticker in tickers:
    print(f"\n{'='*50}\nAnalyzing {ticker}...\n{'='*50}")
    all_results[ticker] = run_analysis(
        ticker,
        period      = "2y",
        output_html = f"dashboard_{ticker}.html"
    )
```

---

## 🤝 Kontribusi

Pull request dan issue sangat disambut! Beberapa area yang bisa dikembangkan:

- [ ] LSTM / Transformer model untuk prediksi
- [ ] Portfolio optimization (Modern Portfolio Theory)
- [ ] Analisis sentimen berita (NLP)
- [ ] Risk management module (position sizing, Kelly Criterion)
- [ ] Real-time data streaming
- [ ] Web UI dengan Streamlit atau Dash
- [ ] Alert system (email / Telegram notification)
- [ ] Support untuk lebih banyak data source (Alpha Vantage, Binance API)

### Cara Berkontribusi

```bash
# 1. Fork repo ini
# 2. Buat branch baru
git checkout -b feature/nama-fitur-baru

# 3. Commit perubahan
git commit -m "feat: tambah indikator Williams %R"

# 4. Push ke branch
git push origin feature/nama-fitur-baru

# 5. Buat Pull Request
```

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** — bebas digunakan, dimodifikasi, dan didistribusikan untuk keperluan apapun.

---

<div align="center">

Dibuat dengan ☕ dan Python

*"In God we trust. All others must bring data."* — W. Edwards Deming

</div>
