# 📈 Stock Market Analysis Dashboard

A complete Python pipeline that fetches real-time market data, computes
technical indicators and financial ratios, and produces:
- Interactive HTML dashboard (standalone, no server needed)
- Formatted Excel files for Power BI
- Per-ticker charts (candlestick, RSI, MACD, Bollinger Bands)
- Sector comparison and correlation analysis

---

## Project Structure

```
stock_dashboard/
├── run_pipeline.py              ← Master runner (start here)
├── requirements.txt
├── scripts/
│   ├── 01_data_ingestion.py     ← Fetch OHLCV + fundamentals → SQLite + Excel
│   ├── 02_feature_engineering.py← Technical indicators → Excel
│   ├── 03_comparative_analysis.py← Sector comparison, ratios, correlation
│   ├── 04_charts.py             ← Plotly charts + standalone HTML dashboard
│   └── 05_powerbi_export.py     ← Formatted Excel for Power BI
├── data/
│   └── market_data.db           ← SQLite database (auto-created)
└── outputs/
    ├── 01_raw_data.xlsx
    ├── 02_indicators.xlsx
    ├── 03_comparative_analysis.xlsx
    ├── powerbi_dataset.xlsx      ← Load this into Power BI
    ├── dashboard.html            ← Open in any browser
    └── charts/                  ← Per-ticker HTML charts
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the full pipeline

```bash
python run_pipeline.py
```

This runs all 5 steps end-to-end. Takes ~2–5 minutes depending on network speed.

### 3. Open the dashboard

```bash
# Open the interactive HTML dashboard
open outputs/dashboard.html       # macOS
start outputs\dashboard.html      # Windows
xdg-open outputs/dashboard.html   # Linux
```

### 4. Connect Power BI

1. Open **Power BI Desktop**
2. **Get Data → Excel Workbook**
3. Select `outputs/powerbi_dataset.xlsx`
4. Load sheets: `fact_prices`, `dim_company`, `dim_calendar`, `sector_comparison`
5. In **Model view**, create relationships:
   - `fact_prices[ticker]` → `dim_company[ticker]` (Many-to-One)
   - `fact_prices[date]` → `dim_calendar[date]` (Many-to-One)
6. Build visuals! Suggested first visuals:
   - Line chart: `date` × `close`, filtered by `ticker` slicer
   - Bar chart: `short_name` × `1y_return_%`, coloured by `sector_label`
   - Matrix: `short_name` × `pe_ratio / pb_ratio / roe`
   - KPI card: `latest_price` with `1y_return_%` as trend

---

## Tickers Covered

| Company      | Ticker        | Sector     |
|--------------|---------------|------------|
| TCS          | TCS.NS        | Technology |
| Infosys      | INFY.NS       | Technology |
| Wipro        | WIPRO.NS      | Technology |
| HCL Tech     | HCLTECH.NS    | Technology |
| HDFC Bank    | HDFCBANK.NS   | Banking    |
| ICICI Bank   | ICICIBANK.NS  | Banking    |
| SBI          | SBIN.NS       | Banking    |
| Axis Bank    | AXISBANK.NS   | Banking    |

Benchmark: **Nifty 50 (^NSEI)**

### To use US stocks instead

Edit the `TICKERS` dict at the top of each script:
```python
TICKERS = {
    "Technology": ["AAPL", "MSFT", "GOOGL", "META"],
    "Banking":    ["JPM", "BAC", "GS", "WFC"],
}
BENCHMARK = "^GSPC"   # S&P 500
```

---

## Indicators Computed

| Category        | Indicator                         |
|-----------------|-----------------------------------|
| Moving Averages | SMA-20, SMA-50, SMA-200           |
| Momentum        | EMA-12, EMA-26, MACD (12/26/9)    |
| Oscillator      | RSI-14                            |
| Volatility      | Bollinger Bands (20-day, 2σ)      |
| Risk            | 30-day rolling volatility (ann.)  |
| Relative        | 252-day rolling Beta vs Nifty     |

---

## Run Individual Steps

```bash
# Only re-fetch prices and fundamentals
python run_pipeline.py --steps 1

# Re-compute indicators without re-fetching
python run_pipeline.py --steps 2 3

# Regenerate dashboard only
python run_pipeline.py --steps 4 5
```

---

## Automate Daily Updates

### Windows Task Scheduler
1. Open Task Scheduler → Create Basic Task
2. Trigger: Daily at 6:00 PM (after market close)
3. Action: `python C:\path\to\stock_dashboard\run_pipeline.py --steps 1 2 3 4 5`

### Linux / macOS (cron)
```bash
crontab -e
# Add: run at 6:30 PM weekdays
30 18 * * 1-5 cd /path/to/stock_dashboard && python run_pipeline.py
```

Power BI will pick up the updated `powerbi_dataset.xlsx` on next scheduled refresh.

---

## Notes

- **Rate limits**: yfinance uses Yahoo Finance's public API. Running too frequently
  may trigger rate limits. Once daily is safe.
- **Fundamentals**: The fundamentals data (P/E, ROE, etc.) is a point-in-time
  snapshot from when the script runs. Re-run quarterly for updated ratios.
- **Data quality**: Some tickers may have missing data for certain periods.
  The scripts handle this gracefully with NaN values.
