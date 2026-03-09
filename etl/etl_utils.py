# etl/etl_utils.py

from pathlib import Path
import pandas as pd


def load_share_prices(path: Path) -> pd.DataFrame:
    """Load full SimFin daily share prices CSV."""
    df = pd.read_csv(
        path,
        sep=";",        # SimFin bulk files use ';'
        engine="python"
    )
    return df


def filter_ticker(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Filter prices for a single ticker and sort by date."""
    out = df[df["Ticker"] == ticker].copy()
    out["Date"] = pd.to_datetime(out["Date"])
    out = out.sort_values("Date")
    return out


def add_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add daily return and moving averages."""
    df = df.copy()
    df["return_1d"] = df["Close"].pct_change()
    df["ma_5"] = df["Close"].rolling(window=5).mean()
    df["ma_10"] = df["Close"].rolling(window=10).mean()
    df["ma_ratio_5_10"] = df["ma_5"] / df["ma_10"]
    return df


def add_target_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add next-day return and binary target:
    target_up = 1 if next day's close > today's close, else 0.
    """
    df = df.copy()
    df["close_next_day"] = df["Close"].shift(-1)
    df["return_next_day"] = (df["close_next_day"] - df["Close"]) / df["Close"]
    df["target_up"] = (df["return_next_day"] > 0).astype(int)
    return df


def select_feature_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only the columns needed for ML and rename to a clean schema."""
    cols = [
        "Ticker",
        "Date",
        "Close",
        "return_1d",
        "ma_5",
        "ma_10",
        "ma_ratio_5_10",
        "return_next_day",
        "target_up",
    ]
    out = df[cols].rename(
        columns={
            "Ticker": "ticker",
            "Date": "date",
            "Close": "close",
        }
    )
    out = out.dropna().reset_index(drop=True)
    return out


def save_features(df: pd.DataFrame, output_path: Path) -> None:
    """Save processed features as parquet."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)


def run_etl_for_ticker(
    ticker: str,
    share_prices_path: Path,
    output_path: Path,
) -> None:
    """
    Full ETL for a single ticker:
    load raw CSV -> filter -> features -> target -> save.
    """
    prices = load_share_prices(share_prices_path)
    prices_ticker = filter_ticker(prices, ticker)
    prices_feat = add_technical_features(prices_ticker)
    prices_labeled = add_target_column(prices_feat)
    features = select_feature_columns(prices_labeled)
    save_features(features, output_path)

