"""
visualization.py — Professional Chart Dashboard
Generates Plotly interactive charts for all analysis modules.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")


COLORS = {
    "bg":       "#0d1117",
    "panel":    "#161b22",
    "accent":   "#58a6ff",
    "green":    "#3fb950",
    "red":      "#f85149",
    "yellow":   "#d29922",
    "purple":   "#bc8cff",
    "text":     "#e6edf3",
    "muted":    "#8b949e",
    "grid":     "#21262d",
}

LAYOUT_DEFAULTS = dict(
    paper_bgcolor=COLORS["bg"],
    plot_bgcolor =COLORS["panel"],
    font         =dict(family="JetBrains Mono, monospace", color=COLORS["text"], size=11),
    legend       =dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
    margin       =dict(l=60, r=30, t=60, b=40),
    xaxis        =dict(gridcolor=COLORS["grid"], zeroline=False, showgrid=True),
    yaxis        =dict(gridcolor=COLORS["grid"], zeroline=False, showgrid=True),
)


def _apply_layout(fig: go.Figure, title: str, **kwargs) -> go.Figure:
    layout = {**LAYOUT_DEFAULTS, "title": dict(text=title, font=dict(size=14)), **kwargs}
    fig.update_layout(**layout)
    return fig


# ─────────────────────────────────────────────
#  1. Candlestick + MA + Bollinger Bands + Signals
# ─────────────────────────────────────────────

def candlestick_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Multi-panel chart:
      Row 1 (70%): Candlestick + MA20/50/200 + Bollinger Bands + Buy/Sell signals
      Row 2 (15%): Volume bars
      Row 3 (15%): MACD histogram + signal
    """
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.65, 0.15, 0.20],
        vertical_spacing=0.03,
    )

    # ── Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["open"], high=df["high"],
        low=df["low"], close=df["close"],
        name="OHLC",
        increasing_line_color=COLORS["green"],
        decreasing_line_color=COLORS["red"],
        increasing_fillcolor=COLORS["green"],
        decreasing_fillcolor=COLORS["red"],
    ), row=1, col=1)

    # ── Moving Averages
    for col, color, name in [("ma20", COLORS["yellow"], "MA20"),
                               ("ma50", COLORS["accent"], "MA50"),
                               ("ma200", COLORS["purple"], "MA200")]:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df[col], name=name,
                line=dict(color=color, width=1.2, dash="dot"),
                opacity=0.85,
            ), row=1, col=1)

    # ── Bollinger Bands
    if "bb_upper" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["bb_upper"], name="BB Upper",
            line=dict(color=COLORS["muted"], width=0.8), showlegend=False,
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["bb_lower"], name="BB Lower",
            fill="tonexty", fillcolor="rgba(139,148,158,0.1)",
            line=dict(color=COLORS["muted"], width=0.8), showlegend=False,
        ), row=1, col=1)

    # ── Trading Signals
    if "signal" in df.columns:
        buy  = df[df["signal"] == 1]
        sell = df[df["signal"] == -1]
        fig.add_trace(go.Scatter(
            x=buy.index, y=buy["close"] * 0.985,
            mode="markers", name="BUY",
            marker=dict(symbol="triangle-up", size=8,
                        color=COLORS["green"], line=dict(width=1, color="#fff")),
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=sell.index, y=sell["close"] * 1.015,
            mode="markers", name="SELL",
            marker=dict(symbol="triangle-down", size=8,
                        color=COLORS["red"], line=dict(width=1, color="#fff")),
        ), row=1, col=1)

    # ── Volume
    colors_vol = [COLORS["green"] if c >= o else COLORS["red"]
                  for c, o in zip(df["close"], df["open"])]
    fig.add_trace(go.Bar(
        x=df.index, y=df["volume"], name="Volume",
        marker_color=colors_vol, opacity=0.6, showlegend=False,
    ), row=2, col=1)

    # ── MACD
    if "histogram" in df.columns:
        colors_hist = [COLORS["green"] if v >= 0 else COLORS["red"]
                       for v in df["histogram"]]
        fig.add_trace(go.Bar(
            x=df.index, y=df["histogram"], name="MACD Hist",
            marker_color=colors_hist, opacity=0.7, showlegend=False,
        ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["macd_line"], name="MACD",
            line=dict(color=COLORS["accent"], width=1.2),
        ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["signal_line"], name="Signal",
            line=dict(color=COLORS["yellow"], width=1.2),
        ), row=3, col=1)

    fig.update_xaxes(rangeslider_visible=False)
    _apply_layout(fig, f"📈 {ticker} — Price Chart + Indicators + Signals")
    for row in [1, 2, 3]:
        fig.update_xaxes(gridcolor=COLORS["grid"], row=row, col=1)
        fig.update_yaxes(gridcolor=COLORS["grid"], row=row, col=1)
    return fig


# ─────────────────────────────────────────────
#  2. Momentum Dashboard (RSI + Stochastic + ADX)
# ─────────────────────────────────────────────

def momentum_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        subplot_titles=["RSI-14", "Stochastic %K/%D", "ADX / ±DI"],
        vertical_spacing=0.08,
    )

    # RSI
    fig.add_trace(go.Scatter(
        x=df.index, y=df["rsi14"], name="RSI-14",
        line=dict(color=COLORS["accent"], width=1.5),
    ), row=1, col=1)
    for level, color in [(70, COLORS["red"]), (30, COLORS["green"]), (50, COLORS["muted"])]:
        fig.add_hline(y=level, line_dash="dot",
                      line_color=color, opacity=0.5, row=1, col=1)

    # Stochastic
    fig.add_trace(go.Scatter(
        x=df.index, y=df["stoch_k"], name="%K",
        line=dict(color=COLORS["yellow"], width=1.5),
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["stoch_d"], name="%D",
        line=dict(color=COLORS["purple"], width=1.2, dash="dash"),
    ), row=2, col=1)

    # ADX
    fig.add_trace(go.Scatter(
        x=df.index, y=df["adx"], name="ADX",
        line=dict(color=COLORS["accent"], width=1.8),
    ), row=3, col=1)
    if "plus_di" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["plus_di"], name="+DI",
            line=dict(color=COLORS["green"], width=1.2),
        ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["minus_di"], name="-DI",
            line=dict(color=COLORS["red"], width=1.2),
        ), row=3, col=1)
    fig.add_hline(y=25, line_dash="dot", line_color=COLORS["yellow"], opacity=0.5, row=3, col=1)

    _apply_layout(fig, f"⚡ {ticker} — Momentum Indicators")
    return fig


# ─────────────────────────────────────────────
#  3. Equity Curve + Drawdown
# ─────────────────────────────────────────────

def equity_curve_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.65, 0.35], vertical_spacing=0.05)

    # Normalise to 100
    if "portfolio_value" in df.columns:
        strat = df["portfolio_value"] / df["portfolio_value"].iloc[0] * 100
        bah   = df["bah_value"]       / df["bah_value"].iloc[0]       * 100

        fig.add_trace(go.Scatter(
            x=df.index, y=strat, name="Strategy",
            line=dict(color=COLORS["accent"], width=2),
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=bah, name="Buy & Hold",
            line=dict(color=COLORS["muted"], width=1.5, dash="dash"),
        ), row=1, col=1)

        # Drawdown
        if "strategy_drawdown" in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["strategy_drawdown"] * 100,
                name="Strategy DD", fill="tozeroy",
                line=dict(color=COLORS["red"], width=0),
                fillcolor=f"rgba({int('f8',16)},{int('51',16)},{int('49',16)},0.35)",
            ), row=2, col=1)
            fig.add_trace(go.Scatter(
                x=df.index, y=df["bah_drawdown"] * 100,
                name="B&H DD", fill="tozeroy",
                line=dict(color=COLORS["muted"], width=0),
                fillcolor="rgba(139,148,158,0.2)",
            ), row=2, col=1)

    _apply_layout(fig, f"💰 {ticker} — Strategy vs Buy & Hold Equity Curve")
    fig.update_yaxes(title_text="Indexed to 100", row=1, col=1)
    fig.update_yaxes(title_text="Drawdown %",     row=2, col=1)
    return fig


# ─────────────────────────────────────────────
#  4. ML Prediction Chart
# ─────────────────────────────────────────────

def prediction_chart(df: pd.DataFrame,
                     ml_results: dict,
                     future_preds: pd.Series,
                     ticker: str) -> go.Figure:
    fig = go.Figure()

    # Historical close
    fig.add_trace(go.Scatter(
        x=df.index, y=df["close"],
        name="Actual Price",
        line=dict(color=COLORS["text"], width=1.5),
    ))

    # In-sample predictions (best model)
    best = ml_results["best"]
    pred = ml_results[best]["pred"]
    fig.add_trace(go.Scatter(
        x=pred.index, y=pred,
        name=f"Predicted ({best.replace('_',' ').title()})",
        line=dict(color=COLORS["accent"], width=1.5, dash="dash"),
    ))

    # Future predictions
    if not future_preds.empty:
        fig.add_trace(go.Scatter(
            x=future_preds.index, y=future_preds,
            name=f"Forecast ({len(future_preds)}d)",
            mode="lines+markers",
            line=dict(color=COLORS["yellow"], width=2, dash="dot"),
            marker=dict(size=6, color=COLORS["yellow"]),
        ))

    _apply_layout(fig, f"🤖 {ticker} — ML Price Prediction")
    return fig


# ─────────────────────────────────────────────
#  5. Monte Carlo Simulation Chart
# ─────────────────────────────────────────────

def monte_carlo_chart(df: pd.DataFrame,
                      mc_df: pd.DataFrame,
                      summary: dict,
                      ticker: str,
                      n_paths_display: int = 100) -> go.Figure:
    fig = go.Figure()

    # Show a subset of simulation paths
    step = max(1, len(mc_df.columns) // n_paths_display)
    for i in range(0, len(mc_df.columns), step):
        fig.add_trace(go.Scatter(
            x=mc_df.index, y=mc_df.iloc[:, i],
            mode="lines", showlegend=False,
            line=dict(color=COLORS["accent"], width=0.4),
            opacity=0.2,
        ))

    # Confidence band
    lower = mc_df.quantile(0.05, axis=1)
    upper = mc_df.quantile(0.95, axis=1)
    median = mc_df.median(axis=1)

    fig.add_trace(go.Scatter(
        x=mc_df.index, y=upper, name="95th pct",
        line=dict(color=COLORS["green"], width=1.5),
    ))
    fig.add_trace(go.Scatter(
        x=mc_df.index, y=lower, name="5th pct",
        fill="tonexty", fillcolor="rgba(63,185,80,0.12)",
        line=dict(color=COLORS["red"], width=1.5),
    ))
    fig.add_trace(go.Scatter(
        x=mc_df.index, y=median, name="Median",
        line=dict(color=COLORS["yellow"], width=2),
    ))

    _apply_layout(fig, f"🎲 {ticker} — Monte Carlo Simulation ({len(mc_df.columns)} paths)")
    return fig


# ─────────────────────────────────────────────
#  6. Return Distribution
# ─────────────────────────────────────────────

def return_distribution_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    rets = df["daily_return"].dropna() * 100
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=rets, nbinsx=60,
        name="Daily Returns",
        marker_color=COLORS["accent"],
        opacity=0.75,
    ))
    mean_r = rets.mean()
    fig.add_vline(x=mean_r, line_dash="dash", line_color=COLORS["yellow"],
                  annotation_text=f"Mean {mean_r:.2f}%")
    fig.add_vline(x=rets.quantile(0.05), line_dash="dot", line_color=COLORS["red"],
                  annotation_text="VaR 95%")
    _apply_layout(fig, f"📊 {ticker} — Daily Return Distribution")
    fig.update_xaxes(title_text="Daily Return (%)")
    fig.update_yaxes(title_text="Frequency")
    return fig


# ─────────────────────────────────────────────
#  7. Feature Importance
# ─────────────────────────────────────────────

def feature_importance_chart(ml_results: dict, ticker: str) -> go.Figure:
    fi = ml_results.get("random_forest", {}).get("feature_importance")
    if fi is None:
        return go.Figure()
    fi = fi.head(15)
    fig = go.Figure(go.Bar(
        x=fi.values,
        y=fi.index,
        orientation="h",
        marker_color=COLORS["accent"],
    ))
    _apply_layout(fig, f"🔍 {ticker} — Random Forest Feature Importance")
    fig.update_xaxes(title_text="Importance Score")
    return fig


# ─────────────────────────────────────────────
#  Save all charts to HTML
# ─────────────────────────────────────────────

def save_all_charts(charts: list, output_path: str) -> None:
    """
    Combine all Plotly figures into a single self-contained HTML file.
    """
    html_parts = ["<html><head><meta charset='utf-8'>"
                  "<style>body{background:#0d1117;margin:0;padding:20px;}"
                  "h1{color:#e6edf3;font-family:monospace;} .chart{margin-bottom:30px;}"
                  "</style></head><body>"]

    for name, fig in charts:
        html_parts.append(f"<div class='chart'>")
        html_parts.append(fig.to_html(full_html=False, include_plotlyjs="cdn"))
        html_parts.append("</div>")

    html_parts.append("</body></html>")

    with open(output_path, "w") as f:
        f.write("\n".join(html_parts))

    print(f"[Visualization] Dashboard saved → {output_path}")
