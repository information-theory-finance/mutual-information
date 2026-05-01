"""
Mutual Information — Theory Page
Interactive exploration of I(X;Y) on bivariate synthetic data.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from utils.math_core import (
    mi_from_correlation,
    mi_vs_correlation_grid,
    mutual_information,
)
from utils.theme import AMBER, AMBER_LIGHT, BLUE_ACCENT, GREEN_UP, NAVY_DARK, NAVY_MID, SILVER_LIGHT, plotly_layout

st.set_page_config(
    page_title="Theory · Mutual Information · ITF",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Mutual Information — Theory")
st.caption("Interactive exploration on synthetic bivariate data")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Parameters")
    rho = st.slider("Correlation ρ", min_value=-0.99, max_value=0.99, value=0.5, step=0.01)
    bins = st.slider("Joint PMF bins (each axis)", 10, 40, 20, step=2)
    n_samples = st.select_slider("Monte Carlo samples", [1_000, 5_000, 10_000], value=5_000)
    log_base = st.selectbox("Entropy units", ["bits (base 2)", "nats (base e)"], index=0)
    base = {"bits (base 2)": 2.0, "nats (base e)": np.e}[log_base]
    unit = {"bits (base 2)": "bits", "nats (base e)": "nats"}[log_base]
    st.divider()
    st.caption("All charts update immediately.")

# ── Generate data ─────────────────────────────────────────────────────────────
rng = np.random.default_rng(42)
cov = [[1.0, rho], [rho, 1.0]]
data = rng.multivariate_normal([0, 0], cov, n_samples)
x, y = data[:, 0], data[:, 1]

mi_est  = mutual_information(x, y, bins=bins, base=base)
mi_theo = mi_from_correlation(rho, base=base)

# ── Layout ────────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Definition")
    st.latex(r"I(X;Y) = \sum_{x,y} P(x,y)\,\log_b\frac{P(x,y)}{P(x)\,P(y)}")
    st.latex(r"I(X;Y) = H(X) + H(Y) - H(X,Y)")
    st.markdown(
        f"""
**Key properties:**
- $I(X;Y) \\geq 0$ always
- $I(X;Y) = 0$ if and only if $X$ and $Y$ are independent
- $I(X;Y) = I(Y;X)$ — symmetric
- For bivariate normal: $I = -\\frac{{1}}{{2}} \\log_b(1 - \\rho^2)$

**Current configuration (ρ = {rho}):**

| Quantity | Value |
|----------|-------|
| Estimated I(X;Y) | **{mi_est:.4f} {unit}** |
| Theoretical I(X;Y) | {mi_theo:.4f} {unit} |
| Pearson ρ | {rho} |
| Bins | {bins}×{bins} = {bins**2} cells |
"""
    )

    st.subheader("MI vs. Correlation")
    st.markdown("Estimated (histogram) vs. theoretical (closed-form) MI:")
    rho_grid = np.linspace(-0.99, 0.99, 60)
    mi_est_grid, mi_theo_grid = mi_vs_correlation_grid(
        rho_grid, bins=bins, n_samples=3_000, base=base
    )
    fig_curve = go.Figure()
    fig_curve.add_trace(go.Scatter(x=rho_grid, y=mi_theo_grid, mode="lines",
        line=dict(color=AMBER, width=2), name="Theoretical"))
    fig_curve.add_trace(go.Scatter(x=rho_grid, y=mi_est_grid, mode="lines",
        line=dict(color=BLUE_ACCENT, width=1.5, dash="dot"), name="Estimated"))
    fig_curve.add_vline(x=rho, line=dict(color=GREEN_UP, dash="dash", width=1.5),
        annotation_text=f"ρ = {rho}", annotation_font_color=GREEN_UP)
    fig_curve.update_layout(**plotly_layout(
        title="I(X;Y) vs. ρ", x_title="Pearson ρ", y_title=f"I(X;Y) [{unit}]"))
    st.plotly_chart(fig_curve, use_container_width=True)

with right:
    st.subheader("Joint Distribution")
    fig_joint = make_subplots(rows=1, cols=1)
    fig_joint.add_trace(go.Scatter(
        x=x[:2000], y=y[:2000], mode="markers",
        marker=dict(color=AMBER, opacity=0.25, size=3),
        name="samples",
    ))
    fig_joint.update_layout(**plotly_layout(
        title=f"Bivariate Normal (ρ = {rho})", x_title="X", y_title="Y"))
    st.plotly_chart(fig_joint, use_container_width=True)

    st.subheader("Joint PMF Heatmap")
    from utils.math_core import joint_pmf
    jp = joint_pmf(x, y, bins=bins)
    fig_heat = go.Figure(go.Heatmap(
        z=jp.T,
        colorscale=[[0, NAVY_DARK], [0.5, "#1a3a6e"], [1, AMBER]],
        showscale=True,
        colorbar=dict(tickcolor=SILVER_LIGHT, tickfont=dict(color=SILVER_LIGHT)),
    ))
    fig_heat.update_layout(**plotly_layout(title=f"Joint PMF P(X,Y) — {bins}×{bins} bins",
        x_title="X bin", y_title="Y bin"))
    st.plotly_chart(fig_heat, use_container_width=True)

st.divider()
st.caption("MI is estimated via histogram binning of the joint distribution. The theoretical value assumes exact bivariate normality.")
