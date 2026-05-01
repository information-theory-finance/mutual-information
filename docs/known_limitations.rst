.. _known_limitations:

Known Limitations
=================

----

Mathematical Limitations
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Limitation
     - Detail
   * - Histogram estimator bias
     - Empirical PMF underestimates true entropy. Bias decreases with sample size.
   * - Bin count sensitivity
     - Entropy values are not comparable across different bin settings.
   * - Discrete approximation
     - Log returns are continuous; binning introduces discretisation error.
   * - No differential entropy
     - The continuous (differential) entropy formula is not implemented.

----

Data Limitations
----------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Limitation
     - Detail
   * - EOD only
     - Intraday uncertainty is not captured.
   * - Two tickers
     - Only NIFTY 50 and INFY.NS are supported in the Finance page.
   * - yfinance dependency
     - Data availability depends on Yahoo Finance uptime and NSE feed accuracy.

----

UI Limitations
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Limitation
     - Detail
   * - No export
     - Chart and data export is not implemented in v0.1.
   * - Single asset
     - The Finance page analyses one ticker at a time; no side-by-side comparison.
   * - Streamlit Cloud sleep
     - The app sleeps after inactivity; first load after sleep triggers a data refresh.
