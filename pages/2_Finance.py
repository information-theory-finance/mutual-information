"""
Mutual Information — Finance Page
Rolling MI between RELIANCE.NS and INFY.NS log returns vs. rolling Pearson correlation.

Tickers: RELIANCE.NS, INFY.NS
Reason: Both are large-cap NSE equities from different sectors (energy/conglomerate vs. IT).
Their MI structure reveals non-linear co-movement that correlation understates,
especially during stress periods and earnings seasons.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from utils.fetch import get_log_returns
from utils.math_core import mutual_information, rolling_mi
from utils.theme import AMBER, AMBER_LIGHT, BLUE_ACCENT, GREEN_UP, RED_DOWN, SILVER_LIGHT, plotly_layout

st.set_page_config(
    page_title="Finance · Mutual Information · ITF",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Mutual Information — NSE Application")
st.caption("Rolling MI between RELIANCE.NS and INFY.NS · NSE data via yfinance · Auto-updated daily")

with st.sidebar:
    st.header("Data Controls")
    start_date = st.date_input("Start date", value=pd.Timestamp("2018-01-01"))
    st.divider()
    st.header("MI Parameters")
    window = st.slider("Rolling window (trading days)", 30, 120, 60, step=5)
    bins = st.slider("Joint PMF bins (each axis)", 8, 30, 15, step=1)
    log_base = st.selectbox("Entropy units", ["bits (base 2)", "nats (base e)"], index=0)
    base = {"bits (base 2)": 2.0, "nats (base e)": np.e}[log_base]
    unit = {"bits (base 2)": "bits", "nats (base e)": "nats"}[log_base]
    st.divider()
    st.caption("Data fetches on first load and auto-refreshes every 24 h.")


@st.cache_data(ttl=86400)
def load_returns(start: str):
    r1 = get_log_returns("RELIANCE.NS", start=start)
    r2 = get_log_returns("INFY.NS", start=start)
    df = pd.DataFrame({"RELIANCE": r1, "INFY": r2}).dropna()
    return df


with st.spinner("Fetching RELIANCE.NS and INFY.NS data…"):
    df = load_returns(str(start_date))

if df.empty:
    st.error("No data returned. Check your internet connection.")
    st.stop()

r1 = df["RELIANCE"].values
r2 = df["INFY"].values
dates = df.index

# Rolling MI and rolling Pearson correlation
roll_mi_vals = rolling_mi(r1, r2, window=window, bins=bins, base=base)
roll_corr = pd.Series(r1).rolling(window).corr(pd.Series(r2)).values

mi_series   = pd.Series(roll_mi_vals, index=dates)
corr_series = pd.Series(roll_corr,    index=dates)

valid_mi = mi_series.dropna()
current_mi   = valid_mi.iloc[-1] if len(valid_mi) else float("nan")
mean_mi      = valid_mi.mean()   if len(valid_mi) else float("nan")
full_mi      = mutual_information(r1, r2, bins=bins, base=base)
full_corr    = float(np.corrcoef(r1, r2)[0, 1])
current_corr = corr_series.dropna().iloc[-1] if len(corr_series.dropna()) else float("nan")

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Current MI", f"{current_mi:.4f} {unit}", delta=f"{current_mi - mean_mi:+.4f} vs avg")
k2.metric("Mean Rolling MI", f"{mean_mi:.4f} {unit}")
k3.metric("Full-sample MI", f"{full_mi:.4f} {unit}")
k4.metric("Current Pearson ρ", f"{current_corr:.4f}")
k5.metric("Full-sample ρ", f"{full_corr:.4f}")

st.divider()

# ── Main chart ────────────────────────────────────────────────────────────────
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    row_heights=[0.35, 0.35, 0.30],
    vertical_spacing=0.05,
    subplot_titles=[
        "Log Returns — RELIANCE.NS vs INFY.NS",
        f"Rolling Mutual Information ({window}-day window)",
        f"Rolling Pearson Correlation ({window}-day window)",
    ],
)

fig.add_trace(go.Scatter(x=dates, y=r1, mode="lines",
    line=dict(color=AMBER, width=1), name="RELIANCE"), row=1, col=1)
fig.add_trace(go.Scatter(x=dates, y=r2, mode="lines",
    line=dict(color=BLUE_ACCENT, width=1), name="INFY"), row=1, col=1)

fig.add_trace(go.Scatter(x=mi_series.index, y=mi_series.values, mode="lines",
    line=dict(color=AMBER, width=1.5), name=f"I(X;Y) [{unit}]"), row=2, col=1)
fig.add_hline(y=mean_mi, line=dict(color=AMBER_LIGHT, dash="dot", width=1),
    annotation_text=f"mean {mean_mi:.3f}", annotation_font_color=AMBER_LIGHT, row=2, col=1)

fig.add_trace(go.Scatter(x=corr_series.index, y=corr_series.values, mode="lines",
    line=dict(color=BLUE_ACCENT, width=1.5), name="Pearson ρ"), row=3, col=1)
fig.add_hline(y=0, line=dict(color=SILVER_LIGHT, dash="dot", width=1), row=3, col=1)

layout = plotly_layout(title="RELIANCE vs INFY — Rolling MI and Correlation")
layout.update({"height": 680, "showlegend": True})
fig.update_layout(**layout)
fig.update_xaxes(gridcolor="#2a3a5c", zerolinecolor="#2a3a5c", color=SILVER_LIGHT)
fig.update_yaxes(gridcolor="#2a3a5c", zerolinecolor="#2a3a5c", color=SILVER_LIGHT)

st.plotly_chart(fig, use_container_width=True)

# ── Scatter + joint heatmap ───────────────────────────────────────────────────
st.subheader("Joint Return Structure")
c1, c2 = st.columns(2)

with c1:
    fig_sc = go.Figure()
    fig_sc.add_trace(go.Scatter(x=r1, y=r2, mode="markers",
        marker=dict(color=AMBER, opacity=0.2, size=3), name="returns"))
    fig_sc.update_layout(**plotly_layout(
        title="RELIANCE vs INFY Log Returns",
        x_title="RELIANCE log return", y_title="INFY log return"))
    st.plotly_chart(fig_sc, use_container_width=True)

with c2:
    from utils.math_core import joint_pmf
    jp = joint_pmf(r1, r2, bins=20)
    fig_heat = go.Figure(go.Heatmap(
        z=jp.T,
        colorscale=[[0, "#0f1629"], [0.5, "#1a3a6e"], [1, AMBER]],
        showscale=True,
        colorbar=dict(tickcolor=SILVER_LIGHT, tickfont=dict(color=SILVER_LIGHT)),
    ))
    fig_heat.update_layout(**plotly_layout(
        title="Joint PMF P(RELIANCE, INFY)",
        x_title="RELIANCE bin", y_title="INFY bin"))
    st.plotly_chart(fig_heat, use_container_width=True)

st.divider()
st.caption(
    f"Tickers: RELIANCE.NS, INFY.NS · Source: NSE via yfinance · "
    f"Window: {window} days · Bins: {bins}×{bins}"
)
