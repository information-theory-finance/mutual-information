"""
Mutual Information — Information Theory × NSE Finance
app.py: Landing / home page.
"""

import streamlit as st

st.set_page_config(
    page_title="Mutual Information · ITF",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Mutual Information")
st.caption("Information Theory × NSE Finance · [information-theory-finance](https://github.com/information-theory-finance)")

st.markdown(
    """
Mutual information $I(X;Y)$ measures the **statistical dependence** between
two random variables — how much knowing $X$ reduces uncertainty about $Y$.
Unlike Pearson correlation, it captures **nonlinear** and **non-Gaussian**
dependence structures.
"""
)

st.latex(
    r"I(X;Y) = \sum_{x,y} P(x,y) \, \log_2 \frac{P(x,y)}{P(x)\,P(y)}"
)

st.latex(r"I(X;Y) = H(X) + H(Y) - H(X,Y)")

st.markdown(
    """
In finance, MI between asset returns reveals dependencies that linear correlation
misses entirely — such as tail co-movement and regime-dependent coupling.
Two assets can have near-zero correlation but substantial mutual information.
"""
)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Theory.py", label="📐 Theory — bivariate dependence explorer", icon="📐")
    st.caption("Joint PMF, MI vs. correlation, theoretical vs. estimated MI.")
with col2:
    st.page_link("pages/2_Finance.py", label="📈 Finance — NSE application", icon="📈")
    st.caption("Rolling MI between RELIANCE and INFY log returns vs. rolling Pearson correlation.")

st.divider()
st.caption("Data: NSE India via yfinance · Stored locally in DuckDB · Auto-updated daily")
st.caption("Part of the [Information Theory × Finance](https://github.com/information-theory-finance) series · Pranava BA · Chennai")
