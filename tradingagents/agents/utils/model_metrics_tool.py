"""Tool for reading deep-trading model metrics.

Reads backtest.csv from the deep-trading artifacts directory and computes
performance metrics for a given strategy up to (but NOT including) a
specified cutoff date, ensuring no data leakage.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import numpy as np
import pandas as pd
from langchain_core.tools import tool

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

# Will be set at runtime by the experiment runner before agents are invoked.
_DEEP_TRADING_ARTIFACTS_DIR: str | None = None

# When set (e.g. "BTC/USDT"), path lookup uses this instead of the LLM-provided
# symbol so folders like BTCUSDT match even if the agent passes "BTC-USD".
_DEEP_TRADING_SYMBOL_OVERRIDE: str | None = None


def set_artifacts_dir(path: str) -> None:
    """Set the path to the deep-trading artifacts directory."""
    global _DEEP_TRADING_ARTIFACTS_DIR
    _DEEP_TRADING_ARTIFACTS_DIR = path


def set_deep_trading_symbol(symbol: str | None) -> None:
    """Set the deep-trading symbol used to locate backtest.csv (e.g. BTC/USDT).
    Pass None to clear. Walk-forward runner sets this per SymbolPair so
    artifact paths align with on-disk names (BTCUSDT) while the LLM may
    still pass the yfinance ticker (BTC-USD).
    """
    global _DEEP_TRADING_SYMBOL_OVERRIDE
    _DEEP_TRADING_SYMBOL_OVERRIDE = symbol


def _resolve_backtest_csv(symbol: str, strategy: str) -> Path | None:
    """Find the backtest.csv for a given symbol + strategy under artifacts."""
    if _DEEP_TRADING_ARTIFACTS_DIR is None:
        return None

    base = Path(_DEEP_TRADING_ARTIFACTS_DIR)
    # artifacts/<run_id>/<symbol>/<strategy>/backtest.csv
    # We search for the first match across run_ids.
    symbol_clean = symbol.replace("/", "").replace("-", "")
    for run_dir in sorted(base.iterdir()):
        if not run_dir.is_dir():
            continue
        for sym_dir in run_dir.iterdir():
            if not sym_dir.is_dir():
                continue
            if sym_dir.name == symbol_clean or sym_dir.name == symbol:
                csv_path = sym_dir / strategy / "backtest.csv"
                if csv_path.exists():
                    return csv_path
    return None


def _compute_metrics_before(df: pd.DataFrame, cutoff: str) -> dict:
    """Compute performance metrics from backtest rows strictly before *cutoff*.

    Returns a dict with standard performance metrics, or an explanatory
    message if there is insufficient data.
    """
    mask = df.index < pd.Timestamp(cutoff, tz="UTC")
    sub = df.loc[mask]

    if len(sub) < 48:  # less than 2 days of hourly bars
        return {"status": "insufficient_data", "bars": int(len(sub))}

    net = sub["net_return"].dropna()
    if len(net) == 0:
        return {"status": "no_returns", "bars": int(len(sub))}

    equity = (1 + net).cumprod()
    cum_ret = float(equity.iloc[-1] - 1)

    hours = (sub.index[-1] - sub.index[0]).total_seconds() / 3600
    years = hours / 8760 if hours > 0 else 1e-9
    ann_ret = float((1 + cum_ret) ** (1 / years) - 1) if years > 0 else 0.0

    ann_vol = float(net.std() * np.sqrt(8760)) if len(net) > 1 else 0.0
    downside = net[net < 0]
    ds_vol = float(downside.std() * np.sqrt(8760)) if len(downside) > 1 else 0.0

    sharpe = ann_ret / ann_vol if ann_vol > 0 else 0.0
    sortino = ann_ret / ds_vol if ds_vol > 0 else 0.0

    rolling_max = equity.cummax()
    drawdown = (equity - rolling_max) / rolling_max
    max_dd = float(drawdown.min())
    calmar = ann_ret / abs(max_dd) if max_dd != 0 else 0.0

    # Hit rate
    positions = sub["position_lag"].dropna()
    aligned_ret = sub["asset_return"].reindex(positions.index)
    wins = ((positions * aligned_ret) > 0).sum()
    total = (positions != 0).sum()
    hit_rate = float(wins / total) if total > 0 else 0.0

    turnover = sub["turnover"].dropna()
    turnover_mean = float(turnover.mean()) if len(turnover) > 0 else 0.0

    return {
        "status": "ok",
        "bars": int(len(sub)),
        "cumulative_return": round(cum_ret, 6),
        "annualized_return": round(ann_ret, 6),
        "annualized_volatility": round(ann_vol, 6),
        "sharpe": round(sharpe, 4),
        "sortino": round(sortino, 4),
        "max_drawdown": round(max_dd, 6),
        "calmar": round(calmar, 4),
        "hit_rate": round(hit_rate, 4),
        "turnover_mean": round(turnover_mean, 6),
    }


# ---------------------------------------------------------------------------
# LangChain tool
# ---------------------------------------------------------------------------

_STRATEGIES = ["lstm", "xgboost", "arima_garch", "xgb_lstm_ensemble"]


@tool
def get_model_metrics(
    symbol: Annotated[str, "Trading symbol, e.g. BTC/USDT or ETH/USDT"],
    cutoff_date: Annotated[str, "Cutoff date in YYYY-MM-DD format. Only data BEFORE this date is used."],
) -> str:
    """Retrieve historical performance metrics for all deep-learning / ML trading
    models (LSTM, XGBoost, ARIMA-GARCH, Ensemble) up to but NOT including the
    cutoff date.  This prevents data leakage — you will only see past performance.

    Returns a JSON string with per-model metrics including cumulative return,
    Sharpe ratio, max drawdown, hit rate, etc.
    """
    effective_symbol = _DEEP_TRADING_SYMBOL_OVERRIDE or symbol
    results: dict[str, dict] = {}

    for strategy in _STRATEGIES:
        csv_path = _resolve_backtest_csv(effective_symbol, strategy)
        if csv_path is None:
            results[strategy] = {
                "status": "not_found",
                "message": (
                    f"No backtest.csv found for {effective_symbol}/{strategy}"
                ),
            }
            continue

        try:
            df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            if df.index.tz is None:
                df.index = df.index.tz_localize("UTC")
            results[strategy] = _compute_metrics_before(df, cutoff_date)
        except Exception as exc:
            results[strategy] = {"status": "error", "message": str(exc)}

    return json.dumps(results, indent=2)
