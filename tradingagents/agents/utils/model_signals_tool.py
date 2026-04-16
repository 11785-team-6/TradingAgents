"""Tool for exposing deep-trading **positional signals** (no lookahead).

Reads the last available hourly bar **strictly before** ``as_of_date`` (UTC midnight)
for each configured strategy, maps ``position`` to BUY / SELL / HOLD, and returns JSON.
"""

from __future__ import annotations

import json
from typing import Annotated

import pandas as pd
from langchain_core.tools import tool

import tradingagents.agents.utils.model_metrics_tool as _mmt
from tradingagents.agents.utils.model_metrics_tool import (
    _resolve_backtest_csv,
    get_model_strategies,
)

# Same cutoff semantics as ``_compute_metrics_before``: decision on calendar day D
# uses only bars with timestamp < D 00:00 UTC.
EPS_POSITION = 1e-6


def _position_to_label(position: float) -> str:
    if position > EPS_POSITION:
        return "BUY"
    if position < -EPS_POSITION:
        return "SELL"
    return "HOLD"


def _signals_for_strategy(
    symbol: str,
    strategy: str,
    as_of_date: str,
) -> dict:
    csv_path = _resolve_backtest_csv(symbol, strategy)
    if csv_path is None:
        return {
            "status": "not_found",
            "message": f"No backtest.csv found for {symbol}/{strategy}",
        }

    try:
        df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
        if df.index.tz is None:
            df.index = df.index.tz_localize("UTC")
    except Exception as exc:
        return {"status": "error", "message": str(exc)}

    cutoff = pd.Timestamp(as_of_date, tz="UTC")
    sub = df.loc[df.index < cutoff]
    if len(sub) < 1:
        return {"status": "insufficient_data", "bars": 0}

    row = sub.iloc[-1]
    pos = float(row["position"]) if "position" in row.index else float("nan")
    if pd.isna(pos):
        return {"status": "no_position", "bars": int(len(sub))}

    sig = float(row["signal"]) if "signal" in row.index else float("nan")
    ts = sub.index[-1]

    return {
        "status": "ok",
        "bars_before_cutoff": int(len(sub)),
        "bar_timestamp_utc": str(ts),
        "position": round(pos, 6),
        "signal": None if pd.isna(sig) else round(sig, 6),
        "direction_label": _position_to_label(pos),
    }


@tool
def get_model_signals(
    symbol: Annotated[str, "Trading symbol, e.g. BTC/USDT or ETH/USDT"],
    as_of_date: Annotated[
        str,
        "Trade date YYYY-MM-DD. Uses the last hourly bar strictly BEFORE this date (UTC).",
    ],
) -> str:
    """Return each forecasting model's **current** directional state from backtest.csv
    using only data strictly BEFORE ``as_of_date`` (no lookahead).

    For every configured strategy folder under deep-trading artifacts, reads the last
    available row before the cutoff and maps ``position`` to BUY (long), SELL (short),
    or HOLD (flat).  Complements ``get_model_metrics``, which summarizes past
    performance; this tool exposes **what position each model would be in** at
    decision time.
    """
    effective_symbol = _mmt._DEEP_TRADING_SYMBOL_OVERRIDE or symbol
    results: dict[str, dict] = {}

    for strategy in get_model_strategies():
        results[strategy] = _signals_for_strategy(effective_symbol, strategy, as_of_date)

    return json.dumps(results, indent=2)
