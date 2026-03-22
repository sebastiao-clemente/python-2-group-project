# AutoTrader: AI-Powered Daily Trading System

**Executive Summary**

Bojana Belincevic, David Carrillo, Sebastião Clemente, Bassem El Halawani, Theo Henry, Ocke Moulijn
March 2026

---

## 1. Introduction

AutoTrader is an end-to-end automated trading system that uses machine learning to forecast next-day stock price direction for five major US companies. The project consists of two interconnected components: an offline data analytics pipeline that processes historical market data and trains a classification model, and an interactive web application that delivers live trading signals, model performance metrics, and strategy backtesting to end users.

The five companies tracked are Apple (AAPL), Microsoft (MSFT), Alphabet (GOOG), Amazon (AMZN), and NVIDIA (NVDA). Together they represent the core of the US technology sector and provide a diverse set of price behaviours for the model to learn from.

The application is publicly deployed on Streamlit Cloud and accessible at [https://autotrader4.streamlit.app](https://autotrader4.streamlit.app). It operates in two modes: live mode, which fetches real market data via a custom SimFin API wrapper when a valid API key is provided, and demo mode, which generates statistically realistic synthetic price data so all features remain fully functional without any external account.

---

## 2. Data Sources

All financial data is sourced from SimFin (simfin.com), a platform that provides free access to fundamental and market data for publicly traded companies.

- **Share Prices.** Daily OHLCV data covering approximately five years of trading history. This dataset is the foundation for all feature engineering and is the only data source used by the current model.
- **Company Information.** Metadata including ticker symbol, company name, and industry sector. Used for display purposes in the web application.
- **Financial Statements.** Quarterly income statements, balance sheets, and cash flow statements are accessible through the API wrapper but are not incorporated as model features in this version.

During the offline training phase, data was obtained via SimFin's bulk CSV download facility. In the live application, data is retrieved in real time through a custom Python API wrapper described in Section 5. When no API key is available, the application falls back to synthetic price data generated using Geometric Brownian Motion, the same mathematical model used in the Black-Scholes option pricing framework. This ensures the full application experience remains accessible in demonstration contexts.

---

## 3. ETL Pipeline

The Extract, Transform, Load (ETL) pipeline is the foundation of the system. It converts raw OHLCV price data into a structured feature matrix suitable for machine learning. The pipeline runs identically in three contexts: the offline training script, the live web application, and the standalone command-line batch scripts. Using the same code across all three contexts eliminates the risk of training-serving inconsistency, a common source of degraded model performance in production systems.

The pipeline follows a 10-step process implemented as a chain of pure functions. Each step receives a Pandas DataFrame and returns an augmented version with new columns added.

| Step | Name | Description |
|------|------|-------------|
| 1 | Clean and validate | Standardises column names, parses dates, removes duplicates, forward-fills gaps, and creates a unified price column using adjusted close where available. |
| 2 | Daily returns | Computes 1-day, 5-day, and 10-day percentage price changes. |
| 3 | Rolling volatility | Calculates the rolling standard deviation of daily returns over 10 and 20-day windows. |
| 4 | Moving averages | Simple Moving Averages (5, 10, 20, 50 days) and Exponential Moving Averages (12, 26 days). All normalised by current price so features are comparable across tickers. |
| 5 | RSI-14 | Relative Strength Index over 14 days. Values above 70 indicate overbought conditions; below 30 indicate oversold. |
| 6 | MACD | Moving Average Convergence Divergence: 12-day EMA minus 26-day EMA, normalised by price, plus a 9-day signal line. |
| 7 | Bollinger Bands | Upper and lower bands at two standard deviations from the 20-day simple moving average, plus band width. All normalised by current price. |
| 8 | Volume features | 10-day average volume (normalised to a 0 to 1 scale) and the ratio of current volume to that average. |
| 9 | ATR-14 | Average True Range over 14 days, normalised by price. Captures overnight gap risk that high-low range alone does not. |
| 10 | Target generation | Binary label: 1 if the next day closing price exceeds today's, 0 otherwise. Omitted during live prediction. |

A key design decision throughout Steps 4 to 9 is price normalisation. Rather than using raw indicator values, all moving average and band features are expressed as percentage deviations from the current price. This makes them directly comparable across tickers at very different price levels and prevents the features from trending upward with the stock price over time, a property known as stationarity that is important for model reliability.

After all steps, any row with a missing value in the essential feature columns is removed. These gaps arise from the rolling window warmup period: a 50-day simple moving average cannot produce a value until 50 days of data have accumulated. In practice, approximately 50 to 60 rows are trimmed from the start of each ticker's history.

---

## 4. Machine Learning Model

The prediction task is binary classification: given today's technical indicators, determine whether the stock's closing price will be higher or lower the following trading day. A result of 1 indicates UP and 0 indicates DOWN.

### Model Architecture

The model is a scikit-learn Pipeline consisting of two sequential steps. First, a StandardScaler normalises all input features to zero mean and unit variance. This step is essential for Logistic Regression, which is sensitive to the relative scale of its input features. Second, a Logistic Regression classifier produces a binary prediction and an associated probability for each class.

The full feature space comprises 21 technical indicators plus 4 one-hot encoded ticker identifiers, giving 25 input dimensions in total. Apple (AAPL) serves as the implicit reference category and does not receive a dedicated dummy column.

### Training Methodology

Historical data for all five tickers is combined into a single dataset of approximately 5,950 samples following ETL. The dataset is split 80/20 into training and test sets with strict temporal ordering preserved. Shuffling is explicitly disabled to prevent any future information from leaking into the training window.

The regularisation strength parameter C was tuned by evaluating test accuracy across the values 0.01, 0.1, 1.0, and 10.0, with C = 10.0 selected as the best-performing configuration. Balanced class weights are applied throughout to prevent the model from defaulting to the majority class when the distribution of UP and DOWN days is uneven.

### Performance

The model achieves approximately 52% accuracy on the held-out test set. This figure is consistent with the inherent difficulty of daily stock price prediction, which is widely regarded as one of the harder short-horizon forecasting problems in quantitative finance. The project is designed to demonstrate a complete, production-grade machine learning pipeline rather than to achieve high directional accuracy. Even a modest edge over random can generate meaningful returns when combined with an appropriate strategy and sound risk management.

The trained Pipeline is serialised using joblib and stored as `all_tickers_model.joblib`. A graceful fallback mechanism is in place: if the model file is absent, the application substitutes a rule-based heuristic classifier that produces sensible-looking signals using RSI, MACD, and return momentum, ensuring the application remains fully demonstrable without a prior training run.

---

## 5. Web Application Architecture

The web application is built using Streamlit and structured as a four-page multi-page application. Navigation between pages is handled automatically by Streamlit's file-based routing convention. The user's SimFin API key is entered once on the Home page and persisted across all pages via Streamlit's session state mechanism, so no re-entry is required when switching between views.

| Page | Purpose |
|------|---------|
| **Home** | System overview, company profiles, team, technology stack, and a step-by-step explanation of how the system works. The API key is entered here and shared with all other pages via session state. |
| **Go Live** | Selects a ticker, fetches OHLCV data, runs the ETL pipeline, and generates a BUY / SELL / HOLD signal with confidence scores. Displays candlestick charts, RSI, MACD, and a rolling prediction history. |
| **Model Insights** | Feature importance rankings, confusion matrix, accuracy, precision, recall, F1 score, and AUC-ROC. Includes a feature correlation heatmap and text explanations of the ETL process and evaluation methodology. |
| **Backtesting** | Compares Buy-and-Hold, Buy-and-Sell, and Benchmark strategies over a configurable historical period. Shows portfolio performance charts, drawdown analysis, a trade log, and monthly returns. |

### API Wrapper: PySimFin

All communication with the SimFin API is handled by PySimFin, a custom object-oriented Python class developed specifically for this project. The class encapsulates authentication, rate limiting, error handling, and response parsing behind a clean public interface. It enforces a minimum interval of 0.5 seconds between requests to comply with SimFin's free-tier limit of two requests per second. A hierarchy of custom exception classes distinguishes between authentication failures (HTTP 401) and rate limit violations (HTTP 429), allowing calling code to handle each case appropriately. Responses are automatically converted from SimFin's compact JSON format into Pandas DataFrames, standardising column names to conventional OHLCV notation.

### Demo Mode

When no API key is provided, the application generates synthetic price data using Geometric Brownian Motion with per-ticker parameters calibrated to approximate each stock's historical drift and volatility profile. The random seed is fixed per ticker, so the same synthetic data is produced on every run, making demonstrations consistent and reproducible.

---

## 6. Trading Strategies

Three trading strategies are implemented in the backtesting module, allowing users to assess whether the machine learning model generates actionable value relative to a passive baseline.

| Strategy | Signal Source | Sell Condition |
|----------|--------------|----------------|
| Buy and Hold | Model predicts UP; 5-day cooldown between purchases | Never sells. Accumulates shares over the full backtest period. |
| Buy and Sell | P(UP) at or above 50% | P(UP) falls below 50%, position held for 3 days, or unrealised loss reaches 2%. |
| Benchmark | None (buys once on Day 1) | Never sells. No ML involvement. Used as the baseline comparator. |

The Buy-and-Hold strategy uses the model exclusively to time entry points, purchasing shares on bullish prediction days while enforcing a five-day cooldown between buys. It never exits a position during the backtest, making it a long-only accumulation approach.

The Buy-and-Sell strategy is more active. It enters a position whenever the model's probability of an UP outcome is at or above 50% and exits when that probability falls below the threshold, when a position has been held for three consecutive days, or when an unrealised loss of 2% is reached. A structural safeguard prevents a buy and a sell from being triggered on the same trading day.

The Benchmark strategy requires no model at all. It purchases the maximum number of whole shares on the first day of the backtest and holds them for the entire period. Its purpose is to establish the return an investor would have achieved simply by buying and holding, providing the reference point against which both ML-driven strategies are evaluated.

Performance across all three strategies is summarised using the following metrics:

| Metric | Description |
|--------|-------------|
| Total Return | (Final portfolio value minus initial capital) divided by initial capital. |
| Annualised Return | Total return extrapolated to a 252 trading-day year for comparability. |
| Sharpe Ratio | Mean daily return divided by its standard deviation, scaled to an annual figure. Measures risk-adjusted performance. |
| Maximum Drawdown | Largest peak-to-trough portfolio decline over the backtest period. |
| Win Rate | Proportion of completed sell trades that closed at a higher price than the corresponding entry. |
| Total Trades | Sum of all BUY and SELL actions executed during the backtest. |

---

## 7. Challenges and Conclusions

### Challenges Encountered

**Class imbalance.** The initial model predicted the majority class almost exclusively, producing no useful DOWN signals. Applying balanced class weights, which adjust the contribution of each class inversely proportional to its frequency, resolved the issue and produced meaningful predictions for both directions.

**Feature stationarity.** Raw price levels and raw moving average values are non-stationary: they tend to grow over time alongside the stock price, making cross-ticker comparison unreliable. Normalising all price-based features as percentage deviations from current price addressed this and allowed a single model to operate across five very different stocks.

**API rate limits.** SimFin's free tier permits only two requests per second. Without careful rate limiting in the API wrapper, pages that fetch data for multiple tickers would have received HTTP 429 errors. The solution, a time-based sleep enforced before every request, resolved this transparently for the rest of the application.

**Team coordination.** The project was developed concurrently across four workstreams: the ETL pipeline, the ML model, the API wrapper, and the frontend. A force-push incident at one point overwrote shared commit history, requiring careful recovery from the remote branch. The experience reinforced the value of branch protection rules and clear module interfaces for parallel development.

**Model metrics accuracy.** An early version of the Model Insights page computed performance metrics against live or synthetic data rather than the actual training test set, producing figures that did not reflect true model behaviour. The fix involved calculating metrics against a proper 80/20 temporal split of the processed historical data.

### Conclusions

AutoTrader demonstrates a complete end-to-end machine learning trading system, from raw data ingestion and feature engineering through model training, real-time inference, and interactive strategy simulation. The system is deployed and publicly accessible, uses live financial data where available, and degrades gracefully to a synthetic fallback when it is not.

The project applies sound engineering and statistical practice throughout: an identical ETL pipeline in training and serving contexts, a temporal train-test split to prevent data leakage, normalised features to support cross-ticker generalisation, and a fallback model to maintain full functionality independent of training infrastructure. The modular architecture, in which each component (ETL, model, API wrapper, strategies, charts) is isolated behind a clear interface, means any one part can be improved or replaced without affecting the others.

While daily stock price direction is inherently difficult to predict with high accuracy, the system provides a rigorous and extensible foundation. The next natural steps would be to incorporate fundamental financial statement data (already accessible via the API wrapper), to evaluate ensemble methods such as Gradient Boosting, and to implement walk-forward cross-validation for more robust out-of-sample performance estimation.
