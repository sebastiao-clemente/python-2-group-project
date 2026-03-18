# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
# From the app/ directory
streamlit run Home.py
```

Requires Python 3.11+. Install dependencies with `pip install -r requirements.txt`.

Demo mode activates automatically when no SimFin API key is provided (synthetic data via geometric Brownian motion). API key is entered in the sidebar at runtime.

## Training the ML Model

```bash
# From project root — requires SimFin bulk CSV in data/raw/
python ml/train_model.py
```

After training, verify `TICKER_DUMMIES` in `app/utils/config.py` matches the printed output. The trained pipeline is saved to `ml/model/all_tickers_model.joblib`.

## No Tests or Linting

There is no test suite, linting, or formatting configuration.

## Architecture

**Streamlit multi-page app** with an offline ML training pipeline and an online prediction system.

### Offline (ml/)
`train_model.py` loads SimFin bulk CSV, runs the ETL pipeline per ticker, combines into one dataset (~5,950 samples), trains a LogisticRegression pipeline (StandardScaler + balanced class weights, C=10.0) with an 80/20 temporal split, and exports to `.joblib`.

### Online (app/)
Each page load fetches data (SimFin API via `utils/pysimfin.py`, or synthetic fallback via `utils/data_helpers.py`), runs the **same ETL pipeline** (`utils/etl.py`) to produce 21 technical indicator features + 4 ticker dummies, then loads the trained model (`utils/model.py`) for inference. If no `.joblib` exists, a `DummyClassifier` with heuristic scoring is used.

### Key modules in app/utils/
- **config.py** — All constants: tickers, feature lists, ticker dummies, colors, team members
- **etl.py** — 10-step feature engineering pipeline (returns, volatility, MAs, RSI, MACD, Bollinger, volume, ATR, target). Used both offline and online.
- **model.py** — `ModelWrapper` (wraps sklearn pipeline) and `DummyClassifier` (fallback). Handles ticker one-hot encoding alignment via `_prepare_model_input()`.
- **pysimfin.py** — OOP SimFin API wrapper with rate limiting (max 2 req/s) and custom exceptions
- **data_helpers.py** — Bridges API/demo data to ETL. `load_processed_data()` is the main entry point (cached 5min).
- **trading_strategy.py** — Three strategies: `strategy_buy_and_hold()`, `strategy_buy_and_sell()`, `benchmark_buy_and_hold()`. Runs at backtest time in the web app.
- **charts.py** — All Plotly chart builders
- **style.py** — Full custom CSS theme injection

### Pages
| File | Role |
|------|------|
| `Home.py` | Landing page, architecture overview, team profiles |
| `pages/1_Go_Live.py` | Ticker selector, live predictions (BUY/SELL/HOLD), price charts |
| `pages/2_Model_Insights.py` | Feature importance, confusion matrix, accuracy metrics |
| `pages/3_Backtesting.py` | Strategy simulator with portfolio charts and trade logs |

### Data flow (online)
PySimFin/demo data -> ETL pipeline -> features DataFrame -> model.predict() -> Streamlit UI

### Deployment
Streamlit Cloud. Config in `app/.streamlit/config.toml` (dark theme, headless mode). Secrets via `.streamlit/secrets.toml` (gitignored).
