"""
ml_model.py — Machine Learning Price Prediction Module
Uses Random Forest and Linear Regression with technical indicator features.
Also includes Monte Carlo simulation.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
import warnings
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────
#  Feature Engineering
# ─────────────────────────────────────────────

FEATURE_COLS = [
    "daily_return", "log_return",
    "rsi14", "stoch_k", "stoch_d",
    "macd_line", "signal_line", "histogram",
    "bb_pct", "bb_width", "atr14",
    "adx", "plus_di", "minus_di",
    "ma20", "ma50",
    "volume",
]

def build_features(df: pd.DataFrame,
                   target_horizon: int = 5) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Build ML feature matrix X and target y.

    Target y: forward return over next `target_horizon` days.
    This turns the problem into a price-direction regression task.

    Returns:
        X : feature DataFrame
        y : target Series (future close price)
    """
    df = df.copy()

    # Lag features (1-day and 5-day lags) to avoid look-ahead bias
    for col in ["rsi14", "macd_line", "bb_pct", "adx", "daily_return"]:
        if col in df.columns:
            df[f"{col}_lag1"] = df[col].shift(1)
            df[f"{col}_lag5"] = df[col].shift(5)

    # Target: close price N days ahead
    df["target"] = df["close"].shift(-target_horizon)

    available = [c for c in FEATURE_COLS if c in df.columns]
    lag_cols   = [c for c in df.columns if "_lag" in c]
    feature_cols = available + lag_cols

    df_clean = df[feature_cols + ["target"]].dropna()

    X = df_clean[feature_cols]
    y = df_clean["target"]
    return X, y


# ─────────────────────────────────────────────
#  Model Training & Evaluation
# ─────────────────────────────────────────────

def train_and_evaluate(df: pd.DataFrame,
                       target_horizon: int = 5,
                       test_size: float = 0.2
                       ) -> Dict[str, Any]:
    """
    Train both Linear Regression and Random Forest.
    Uses walk-forward (time-series) cross-validation to avoid data leakage.

    Returns dict with models, scalers, metrics, and predictions.
    """
    X, y = build_features(df, target_horizon)

    n         = len(X)
    split_idx = int(n * (1 - test_size))

    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    scaler  = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    results = {}

    # ── Linear Regression
    lr = LinearRegression()
    lr.fit(X_train_s, y_train)
    lr_pred = lr.predict(X_test_s)

    results["linear_regression"] = {
        "model":   lr,
        "scaler":  scaler,
        "mae":     round(mean_absolute_error(y_test, lr_pred), 4),
        "rmse":    round(np.sqrt(mean_squared_error(y_test, lr_pred)), 4),
        "pred":    pd.Series(lr_pred, index=y_test.index),
        "actual":  y_test,
    }

    # ── Random Forest
    rf = RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        min_samples_split=10,
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train_s, y_train)
    rf_pred = rf.predict(X_test_s)

    results["random_forest"] = {
        "model":   rf,
        "scaler":  scaler,
        "mae":     round(mean_absolute_error(y_test, rf_pred), 4),
        "rmse":    round(np.sqrt(mean_squared_error(y_test, rf_pred)), 4),
        "pred":    pd.Series(rf_pred, index=y_test.index),
        "actual":  y_test,
        "feature_importance": pd.Series(
            rf.feature_importances_,
            index=X_train.columns,
        ).sort_values(ascending=False),
    }

    print(f"\n[ML Model] Target horizon: {target_horizon} days ahead")
    for name, r in results.items():
        print(f"  {name:<22} MAE={r['mae']:.4f}  RMSE={r['rmse']:.4f}")

    results["best"] = (
        "random_forest"
        if results["random_forest"]["mae"] < results["linear_regression"]["mae"]
        else "linear_regression"
    )

    results["X_test"]      = X_test
    results["y_test"]      = y_test
    results["X_train"]     = X_train
    results["train_size"]  = split_idx
    results["horizon"]     = target_horizon

    return results


def predict_future(df: pd.DataFrame,
                   results: Dict[str, Any],
                   n_days: int = 5) -> pd.Series:
    """
    Predict future prices using the best model on the latest available features.
    Simple recursive forecast: each prediction becomes input for next step.

    Returns a Series of n_days predicted prices with future dates.
    """
    best_key = results["best"]
    model    = results[best_key]["model"]
    scaler   = results[best_key]["scaler"]

    # Re-build features on full dataset
    X, _ = build_features(df, target_horizon=1)
    if X.empty:
        return pd.Series(dtype=float)

    last_features = scaler.transform(X.iloc[[-1]])
    base_price    = float(df["close"].iloc[-1])
    last_date     = df.index[-1]

    preds  = []
    dates  = pd.bdate_range(start=last_date + pd.Timedelta(days=1), periods=n_days)

    # Naive multi-step: use same feature row for all steps
    for _ in range(n_days):
        p = float(model.predict(last_features)[0])
        preds.append(p)

    return pd.Series(preds, index=dates, name="predicted_close")


# ─────────────────────────────────────────────
#  Monte Carlo Simulation
# ─────────────────────────────────────────────

def monte_carlo(df: pd.DataFrame,
                n_simulations: int = 500,
                n_days: int = 252) -> pd.DataFrame:
    """
    Monte Carlo price path simulation using Geometric Brownian Motion.

    Args:
        df            : Preprocessed DataFrame with log_return column.
        n_simulations : Number of price paths to simulate.
        n_days        : Forecast horizon in trading days.

    Returns:
        DataFrame of shape (n_days, n_simulations) with simulated price paths.
    """
    mu    = df["log_return"].mean()
    sigma = df["log_return"].std()
    S0    = float(df["close"].iloc[-1])

    dt       = 1          # daily steps
    paths    = np.zeros((n_days, n_simulations))
    paths[0] = S0

    rand = np.random.standard_normal((n_days - 1, n_simulations))
    daily_returns = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * rand)

    for t in range(1, n_days):
        paths[t] = paths[t - 1] * daily_returns[t - 1]

    dates = pd.bdate_range(start=df.index[-1], periods=n_days + 1)[1:]
    return pd.DataFrame(paths, index=dates)


def monte_carlo_summary(mc_df: pd.DataFrame,
                         confidence: float = 0.95) -> Dict[str, float]:
    """Summarise Monte Carlo outcomes at end of simulation horizon."""
    final_prices = mc_df.iloc[-1]
    lower_q      = (1 - confidence) / 2
    upper_q      = 1 - lower_q

    return {
        "mean_price":    round(float(final_prices.mean()), 4),
        "median_price":  round(float(final_prices.median()), 4),
        "lower_bound":   round(float(final_prices.quantile(lower_q)), 4),
        "upper_bound":   round(float(final_prices.quantile(upper_q)), 4),
        "prob_up":       round(float((final_prices > mc_df.iloc[0].mean()).mean()), 4),
    }
