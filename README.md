<div align="center">

<pre>
 __  __ _   _ _____ _   _   _    _      ___ _   _ _____ ___  
|  \/  | | | |_   _| | | | / \  | |    |_ _| \ | |  ___/ _ \ 
| |\/| | | | | | | | | | |/ _ \ | |     | ||  \| | |_ | | | |
| |  | | |_| | | | | |_| / ___ \| |___  | || |\  |  _|| |_| |
|_|  |_|\___/  |_|  \___/_/   \_\_____|___|_| \_|_|   \___/ 
</pre>

**Mutual Information — Information Theory × NSE Finance**

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![DuckDB](https://img.shields.io/badge/DuckDB-Latest-FFF000?style=flat-square)](https://duckdb.org)
[![NSE](https://img.shields.io/badge/Data-NSE%20India-0055A5?style=flat-square)](https://nseindia.com)
[![License](https://img.shields.io/badge/License-MIT-8B949E?style=flat-square)](LICENSE.md)

[![Docs](https://img.shields.io/badge/📖%20Documentation-RTD-1ABC9C?style=for-the-badge&logo=readthedocs&logoColor=white)](#)
[![Live Demo](https://img.shields.io/badge/▶%20Live%20Demo-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](#)

<br/>

*Measuring nonlinear dependence between NSE assets — beyond Pearson correlation.*

</div>

<br/>

---

## Run Locally

<details>
<summary><strong>🐍 Run from Source</strong></summary>
<br/>

```bash
git clone https://github.com/information-theory-finance/mutual-information.git
cd mutual-information
pip install -r requirements.txt
streamlit run app.py
```

Data is fetched automatically from NSE via yfinance on first run and stored in `data/nse.duckdb`.

</details>

---

## What This App Shows

| Page | Content |
|------|---------|
| **Theory** | Bivariate joint PMF, MI vs. Pearson ρ (estimated and theoretical), heatmap — on synthetic data |
| **Finance** | Rolling MI between RELIANCE.NS and INFY.NS returns vs. rolling correlation |

---

## Screenshots

<div align="center">

<table>
  <tr>
    <td><img src="images/i1.png" width="100%" /></td>
    <td><img src="images/i2.png" width="100%" /></td>
  </tr>
  <tr>
    <td><img src="images/i3.png" width="100%" /></td>
    <td><img src="images/i4.png" width="100%" /></td>
  </tr>
</table>

</div>

---

## Core Formula

$$I(X;Y) = \sum_{x,y} P(x,y) \, \log_2 \frac{P(x,y)}{P(x)\,P(y)}$$

---

## Features

<details>
<summary><strong>📐 Theory Page</strong></summary>
<br/>

- Adjust Pearson correlation ρ from −0.99 to 0.99 with a live slider
- View the bivariate scatter plot and joint PMF heatmap
- MI vs. ρ curve: histogram-estimated vs. closed-form theoretical comparison
- Side-by-side estimated and theoretical MI values

</details>

<details>
<summary><strong>📈 Finance Page</strong></summary>
<br/>

- Rolling MI between RELIANCE.NS and INFY.NS on configurable window
- Rolling Pearson correlation plotted alongside for direct comparison
- Joint return scatter and joint PMF heatmap for the full sample
- KPI row: current MI, mean MI, full-sample MI, current and full-sample correlation

</details>

<details>
<summary><strong>🔄 Data</strong></summary>
<br/>

- Source: NSE India via yfinance (adjusted close, EOD)
- Tickers: RELIANCE.NS, INFY.NS
- Stored in a local DuckDB file (`data/nse.duckdb`) — not committed to the repo
- Self-updating: missing trading days are fetched automatically on app load

</details>

---

## Data Notes

> EOD OHLCV data for `RELIANCE.NS` and `INFY.NS` sourced from NSE India via yfinance.
> Default date range: 2018-01-01 to present. Data is stored locally in DuckDB and
> refreshed automatically; no manual updates required.

---

## Part of

> This project is part of the **Information Theory × Finance** series by
> [Pranava BA](https://github.com/pranava-ba).  
> [View all projects →](https://github.com/information-theory-finance)

---

<div align="center">

**Pranava BA** · Chennai, India · © 2025–2026

</div>
