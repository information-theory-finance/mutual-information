.. _overview:

Overview
========

Shannon entropy, introduced by Claude Shannon in 1948, is the foundational
measure of information theory. It quantifies the average number of bits
required to encode the outcome of a random variable — or equivalently, the
average uncertainty before observing an outcome.

----

Why Mutual Information
-------------------

Variance measures the spread of a distribution around its mean, but it is
sensitive only to the second moment. Two distributions — one Gaussian and one
with heavy tails — can share identical variance while carrying very different
information content. Entropy is sensitive to the full shape of the distribution:
its tails, its modes, and its asymmetry.

In financial time series, this distinction is practically significant. Asset
returns are not Gaussian. Entropy provides a model-free measure of uncertainty
that makes no distributional assumption.

----

Core Formula
------------

.. math::

   I(X;Y) = -\sum_{i=1}^{n} p(x_i) \, \log_2 \, p(x_i)

where :math:`p(x_i)` is the probability of outcome :math:`x_i` and the sum
runs over all outcomes with positive probability. The unit is **bits** when
using base-2 logarithm.

----

Technology Stack
----------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Layer
     - Technology
     - Purpose
   * - Frontend
     - Streamlit ≥ 1.30
     - Two-page interactive app
   * - Charts
     - Plotly
     - All visualisations, themed dark navy
   * - Data store
     - DuckDB ≥ 0.10
     - Local OHLCV persistence with upsert
   * - Data source
     - yfinance ≥ 0.2.36
     - NSE EOD data fetch and auto-update
   * - Math
     - NumPy, SciPy
     - Entropy estimation and rolling computation
   * - Docs
     - Sphinx + sphinx-rtd-theme
     - This documentation

----

Feature Summary
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feature
     - Description
   * - Theory explorer
     - Interactive PMF visualisation, entropy gauge, entropy vs. spread curve
   * - Distribution selector
     - Normal, Uniform, Exponential, Laplace with adjustable parameters
   * - Rolling entropy
     - Configurable window and bin count applied to NSE log returns
   * - Auto-update
     - DuckDB store refreshes missing trading days on app start (24 h TTL)
   * - Multi-ticker
     - NIFTY 50 (``^NSEI``) and Nippon Gold ETF (``INFY.NS``)

----

Scope
-----

**This app covers:**

- Discrete Shannon entropy via histogram PMF estimation
- Rolling entropy over financial time series
- Visual comparison of entropy across distribution families
- Application to NSE EOD log return data

**This app does not cover:**

- Differential (continuous) entropy
- Rényi or Tsallis entropy generalisations
- Intraday or tick-level data
- Portfolio optimisation using entropy as an objective

----

Tickers Used
------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Ticker
     - Name
     - Selection Reason
   * - ``^NSEI``
     - NIFTY 50 Index
     - Broad market benchmark; clean EOD data; low noise
   * - ``INFY.NS``
     - Nippon India Gold ETF
     - Distinct entropy profile driven by macro and currency factors
