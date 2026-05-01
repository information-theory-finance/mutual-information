.. _finance:

Finance Application
===================

This page explains why Shannon entropy is a meaningful measure for financial
return distributions, describes the methodology applied to NSE data, and
discusses how to interpret the rolling entropy output.

----

Why Entropy Applies to Financial Returns
-----------------------------------------

Asset returns are not normally distributed. They exhibit fat tails, skewness,
and time-varying volatility. Entropy is a natural fit for three reasons:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Reason
     - Explanation
   * - Model-free
     - No distributional assumption required; entropy works on any PMF
   * - Shape-sensitive
     - Captures tail behaviour, multimodality, and asymmetry that variance misses
   * - Regime indicator
     - Rising entropy signals increasing unpredictability; falling entropy signals
       the market is concentrating probability mass (often around a trend or shock)

----

Tickers and Data
----------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Ticker
     - Name
     - Role in This App
   * - ``^NSEI``
     - NIFTY 50 Index
     - Broad equity market benchmark; baseline entropy behaviour
   * - ``INFY.NS``
     - Nippon India Gold ETF
     - Commodity proxy; macro/currency-driven; structurally distinct entropy

The two tickers are chosen to contrast equity and commodity entropy patterns.
During risk-off periods, equity entropy typically rises (increased uncertainty)
while gold entropy may fall (flight to safety concentrates price moves
directionally).

----

Methodology
-----------

1. **Log returns** are computed as :math:`r_t = \ln(P_t / P_{t-1})`.
2. A **rolling window** of configurable length (default 60 trading days) is
   applied.
3. Within each window, the log return series is discretised into a histogram
   with a configurable number of bins (default 25).
4. The empirical PMF is computed and Shannon entropy is applied.
5. The result is a time series of rolling entropy values plotted alongside
   the price series.

.. math::

   H_t = -\sum_{i=1}^{k} \hat{p}_i^{(t)} \, \log_2 \, \hat{p}_i^{(t)}

where :math:`\hat{p}_i^{(t)}` is the empirical probability in bin :math:`i`
over the window ending at time :math:`t`.

----

Interpreting Results
--------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Observation
     - Interpretation
   * - High rolling entropy
     - Returns are spread broadly across bins; market is highly unpredictable
   * - Low rolling entropy
     - Returns are concentrated; market is in a directional or low-volatility regime
   * - Entropy spike
     - Sudden increase in uncertainty; often corresponds to macro events or earnings
   * - Entropy trough
     - Sustained trending or mean-reversion episode
   * - Entropy divergence (NIFTY vs GOLDBEES)
     - Equity and commodity uncertainty are decoupling; potential regime shift

----

Limitations and Caveats
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Limitation
     - Detail
   * - Histogram bias
     - The histogram estimator underestimates true entropy for small windows.
       Windows below 30 days with more than 20 bins should be interpreted cautiously.
   * - Bin sensitivity
     - Entropy values shift with bin count. Do not compare absolute entropy values
       across different bin settings.
   * - No causal direction
     - Entropy measures uncertainty but not its source or direction.
   * - Stationarity assumption
     - Rolling entropy assumes local stationarity within the window.
   * - EOD data only
     - Intraday uncertainty and microstructure effects are not captured.
