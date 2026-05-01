# utils/fetch.py
# NSE data fetching with DuckDB upsert and self-update logic.
# Information Theory × Finance series — github.com/information-theory-finance

import pandas as pd
import yfinance as yf
import duckdb
from pathlib import Path
from datetime import date, timedelta

DB_PATH = Path("data/nse.duckdb")

CREATE_TABLE_SQL = """
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
"""


def _get_connection() -> duckdb.DuckDBPyConnection:
    DB_PATH.parent.mkdir(exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    con.execute(CREATE_TABLE_SQL)
    return con


def ensure_data(ticker: str, start: str = "2018-01-01") -> pd.DataFrame:
    """
    Ensure DuckDB contains up-to-date OHLCV data for ``ticker``.

    Steps:
    1. Connect to DuckDB (create if not exists).
    2. Check the latest date stored for this ticker.
    3. If the stored data is behind today, fetch the missing window via yfinance.
    4. Upsert new rows (INSERT OR REPLACE) to avoid duplicates.
    5. Return the full OHLCV DataFrame for the ticker.
    """
    con = _get_connection()

    row = con.execute(
        "SELECT MAX(date) FROM prices WHERE ticker = ?", [ticker]
    ).fetchone()
    latest = row[0] if row else None

    fetch_start = start
    if latest is not None:
        next_day = latest + timedelta(days=1)
        today = date.today()
        if next_day >= today:
            # Already up to date
            df = con.execute(
                "SELECT * FROM prices WHERE ticker = ? ORDER BY date", [ticker]
            ).df()
            con.close()
            return df
        fetch_start = next_day.strftime("%Y-%m-%d")

    raw = yf.download(ticker, start=fetch_start, progress=False, auto_adjust=True)

    if not raw.empty:
        raw = raw.reset_index()
        # yfinance >= 0.2 may return MultiIndex columns
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = [col[0] for col in raw.columns]
        raw.columns = [c.lower() for c in raw.columns]
        raw = raw.rename(columns={"adj close": "close"})
        for col in ["open", "high", "low", "close"]:
            if col not in raw.columns:
                raw[col] = float("nan")
        if "volume" not in raw.columns:
            raw["volume"] = 0
        raw["ticker"] = ticker
        raw["date"] = pd.to_datetime(raw["date"]).dt.date
        raw = raw[["ticker", "date", "open", "high", "low", "close", "volume"]].dropna(
            subset=["close"]
        )
        raw["volume"] = raw["volume"].fillna(0).astype("int64")
        con.register("_new_data", raw)
        con.execute("INSERT OR REPLACE INTO prices SELECT * FROM _new_data")

    df = con.execute(
        "SELECT * FROM prices WHERE ticker = ? ORDER BY date", [ticker]
    ).df()
    con.close()
    return df


def get_ohlcv(ticker: str, start: str = "2018-01-01") -> pd.DataFrame:
    """Public entry point. Returns full OHLCV DataFrame for a ticker."""
    return ensure_data(ticker, start=start)


def get_log_returns(ticker: str, start: str = "2018-01-01") -> pd.Series:
    """Return log returns series for a ticker (index = date)."""
    import numpy as np
    df = get_ohlcv(ticker, start=start)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()
    returns = np.log(df["close"] / df["close"].shift(1)).dropna()
    return returns
