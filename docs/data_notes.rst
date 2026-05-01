.. _data_notes:

Data Notes
==========

All data is sourced from NSE India via the yfinance library and stored locally
in a DuckDB database file. No data files are committed to the repository.

----

Data Source
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Detail
   * - Provider
     - Yahoo Finance (``yfinance`` library), NSE India feed
   * - Frequency
     - End-of-day (EOD)
   * - Fields
     - Open, High, Low, Close (adjusted), Volume
   * - Auto-update
     - ``ensure_data()`` checks the latest stored date on every app load and
       fetches any missing trading days. Streamlit cache TTL is 24 hours.

----

Tickers
-------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Ticker
     - Name
     - Exchange
     - Asset Class
   * - ``^NSEI``
     - NIFTY 50 Index
     - NSE
     - Equity Index
   * - ``INFY.NS``
     - Nippon India Gold ETF
     - NSE
     - Commodity ETF

----

Date Range
----------

Default start date: **2018-01-01**. Configurable via the sidebar date picker.
Data ends at the most recent available trading day.

----

DuckDB Schema
-------------

.. code-block:: sql

   CREATE TABLE IF NOT EXISTS prices (
       ticker  VARCHAR,
       date    DATE,
       open    DOUBLE,
       high    DOUBLE,
       low     DOUBLE,
       close   DOUBLE,
       volume  BIGINT,
       PRIMARY KEY (ticker, date)
   );

----

Known Data Quality Issues
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Issue
     - Detail
   * - NSE holidays
     - yfinance omits NSE trading holidays automatically; no manual calendar needed
   * - Adjusted close
     - ``auto_adjust=True`` is passed to yfinance; prices reflect corporate actions
   * - GOLDBEES liquidity
     - Pre-2013 volume data for GOLDBEES may be sparse; default start 2018 avoids this
