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
_DEEP_TRADING_RUN_ID: str | None = None

# When set (e.g. "BTC/USDT"), path lookup uses this instead of the LLM-provided
# symbol so folders like BTCUSDT match even if the agent passes "BTC-USD".
_DEEP_TRADING_SYMBOL_OVERRIDE: str | None = None
_LEAKAGE_AUDIT_RECORDS: list[dict] = []


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


def set_deep_trading_run_id(run_id: str | None) -> None:
    """Fix lookup to one artifacts run folder (e.g. 20260413)."""
    global _DEEP_TRADING_RUN_ID
    _DEEP_TRADING_RUN_ID = run_id


def reset_leakage_audit_records() -> None:
    global _LEAKAGE_AUDIT_RECORDS
    _LEAKAGE_AUDIT_RECORDS = []


def append_leakage_audit_record(record: dict) -> None:
    _LEAKAGE_AUDIT_RECORDS.append(dict(record))


def get_leakage_audit_records() -> list[dict]:
    return list(_LEAKAGE_AUDIT_RECORDS)


def _resolve_backtest_csv(symbol: str, strategy: str) -> Path | None:
    """Find the backtest.csv for a given symbol + strategy under artifacts."""
    if _DEEP_TRADING_ARTIFACTS_DIR is None:
        return None

    base = Path(_DEEP_TRADING_ARTIFACTS_DIR)
    # artifacts/<run_id>/<symbol>/<strategy>/backtest.csv
    # We search for the first match across run_ids.
    symbol_clean = symbol.replace("/", "").replace("-", "")
    run_dirs = []
    if _DEEP_TRADING_RUN_ID:
        pinned = base / _DEEP_TRADING_RUN_ID
        if pinned.exists() and pinned.is_dir():
            run_dirs = [pinned]
        else:
            return None
    else:
        run_dirs = [d for d in sorted(base.iterdir()) if d.is_dir()]

    for run_dir in run_dirs:
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
# Configurable strategy list (YAML / runner sets this before graph build)
# ---------------------------------------------------------------------------

# Aligns with ``agent_experiment.experiment.compare.STRATEGIES`` (forecast baselines).
DEFAULT_MODEL_STRATEGIES: list[str] = [
    "arima_garch",
    "buy_and_hold",
    "lstm",
    "macd",
    "sma_cross",
    "xgb_lstm_ensemble",
    "xgboost",
]

_MODEL_STRATEGIES: list[str] = list(DEFAULT_MODEL_STRATEGIES)


def set_model_strategies(names: list[str] | None) -> None:
    """Restrict which artifact subfolders are queried (empty/None → full default list)."""
    global _MODEL_STRATEGIES
    if not names:
        _MODEL_STRATEGIES = list(DEFAULT_MODEL_STRATEGIES)
    else:
        _MODEL_STRATEGIES = list(names)


def get_model_strategies() -> list[str]:
    return list(_MODEL_STRATEGIES)


# ---------------------------------------------------------------------------
# LangChain tool
# ---------------------------------------------------------------------------


@tool
def get_model_metrics(
    symbol: Annotated[str, "Trading symbol, e.g. BTC/USDT or ETH/USDT"],
    cutoff_date: Annotated[str, "Cutoff date in YYYY-MM-DD format. Only data BEFORE this date is used."],
) -> str:
    """Retrieve historical performance metrics for each configured forecasting strategy
    (folders under deep-trading artifacts) up to but NOT including the cutoff date.
    This prevents data leakage — you will only see past performance.

    Returns a JSON string with per-strategy metrics including cumulative return,
    Sharpe ratio, max drawdown, hit rate, etc.
    """
    effective_symbol = _DEEP_TRADING_SYMBOL_OVERRIDE or symbol
    results: dict[str, dict] = {}

    for strategy in _MODEL_STRATEGIES:
        csv_path = _resolve_backtest_csv(effective_symbol, strategy)
        if csv_path is None:
            append_leakage_audit_record(
                {
                    "tool": "get_model_metrics",
                    "symbol": effective_symbol,
                    "strategy": strategy,
                    "trade_date": cutoff_date,
                    "cutoff_timestamp_utc": f"{cutoff_date} 00:00:00+00:00",
                    "max_timestamp_used_utc": None,
                    "strictly_before_cutoff": None,
                    "status": "not_found",
                    "ok": False,
                    "run_id_constraint": _DEEP_TRADING_RUN_ID,
                }
            )
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
            cutoff_ts = pd.Timestamp(cutoff_date, tz="UTC")
            sub = df.loc[df.index < cutoff_ts]
            max_ts = sub.index.max() if len(sub) > 0 else None
            strictly_before = bool(max_ts < cutoff_ts) if max_ts is not None else None
            status = "ok"
            if max_ts is not None and not strictly_before:
                status = "leakage_violation"
            append_leakage_audit_record(
                {
                    "tool": "get_model_metrics",
                    "symbol": effective_symbol,
                    "strategy": strategy,
                    "trade_date": cutoff_date,
                    "cutoff_timestamp_utc": str(cutoff_ts),
                    "max_timestamp_used_utc": str(max_ts) if max_ts is not None else None,
                    "strictly_before_cutoff": strictly_before,
                    "status": status,
                    "ok": status == "ok",
                    "run_id_constraint": _DEEP_TRADING_RUN_ID,
                }
            )
            if status == "leakage_violation":
                results[strategy] = {
                    "status": status,
                    "message": (
                        f"Leakage check failed: max timestamp {max_ts} is not < cutoff {cutoff_ts}"
                    ),
                }
                continue
            results[strategy] = _compute_metrics_before(df, cutoff_date)
        except Exception as exc:
            append_leakage_audit_record(
                {
                    "tool": "get_model_metrics",
                    "symbol": effective_symbol,
                    "strategy": strategy,
                    "trade_date": cutoff_date,
                    "cutoff_timestamp_utc": f"{cutoff_date} 00:00:00+00:00",
                    "max_timestamp_used_utc": None,
                    "strictly_before_cutoff": None,
                    "status": "error",
                    "ok": False,
                    "error": str(exc),
                    "run_id_constraint": _DEEP_TRADING_RUN_ID,
                }
            )
            results[strategy] = {"status": "error", "message": str(exc)}

    return json.dumps(results, indent=2)
