"""Compare agent pilot metrics with forecasting baselines on the same pilot windows.

Loads forecasting backtests from deep-trading artifacts, slices to pilot dates,
recomputes metrics, and produces a side-by-side comparison with the agent.
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pandas as pd


# Pilot windows (must match pilot.yaml)
PILOT_WINDOWS = [
    (date(2025, 2, 24), date(2025, 3, 15)),
    (date(2025, 4, 9), date(2025, 4, 28)),
    (date(2025, 11, 3), date(2025, 11, 22)),
]

STRATEGIES = [
    "arima_garch",
    "buy_and_hold",
    "lstm",
    "macd",
    "sma_cross",
    "xgb_lstm_ensemble",
    "xgboost",
]

PERIODS_PER_YEAR = 8766
VOL_REGIME_QUANTILE = 0.7


def _pilot_dates() -> set[date]:
    out: set[date] = set()
    for start, end in PILOT_WINDOWS:
        d = start
        while d <= end:
            out.add(d)
            d += timedelta(days=1)
    return out


def _ensure_deep_trading_importable() -> None:
    try:
        from deep_trading.metrics.performance import compute_performance_metrics  # noqa: F401
        return
    except ImportError:
        pass

    deep_root = Path(__file__).resolve().parents[4] / "deep-trading"
    if deep_root.exists() and str(deep_root) not in sys.path:
        sys.path.insert(0, str(deep_root))


def _metrics_on_slice(df: pd.DataFrame) -> dict[str, Any]:
    """Compute performance metrics on a backtest slice (rebased equity)."""
    _ensure_deep_trading_importable()
    from deep_trading.metrics.performance import (
        compute_performance_metrics,
        compute_regime_metrics,
    )

    df = df.copy()
    df["equity"] = (1.0 + df["net_return"].fillna(0.0)).cumprod()

    metrics = compute_performance_metrics(
        net_returns=df["net_return"],
        equity=df["equity"],
        turnover=df["turnover"],
        position_lag=df["position_lag"],
        asset_return=df["asset_return"],
        periods_per_year=PERIODS_PER_YEAR,
    )

    if "realized_vol_24" in df.columns:
        metrics["regimes"] = compute_regime_metrics(
            df, VOL_REGIME_QUANTILE, PERIODS_PER_YEAR,
        )
    else:
        metrics["regimes"] = {}

    return metrics


def _load_forecast_metrics_on_pilot(
    artifacts_root: Path,
    symbol: str = "BTCUSDT",
) -> dict[str, dict[str, Any]]:
    """Load each strategy backtest, slice to pilot dates, compute metrics."""
    pilot = _pilot_dates()
    results: dict[str, dict[str, Any]] = {}

    for strategy in STRATEGIES:
        path = artifacts_root / symbol / strategy / "backtest.csv"
        if not path.exists():
            results[strategy] = {}
            continue

        df = pd.read_csv(path, parse_dates=["timestamp"], index_col="timestamp")
        if df.index.tz is None:
            df.index = df.index.tz_localize("UTC")

        mask = df.index.map(lambda ts: ts.date() in pilot)
        slice_df = df.loc[mask]
        if len(slice_df) == 0:
            results[strategy] = {}
            continue

        results[strategy] = _metrics_on_slice(slice_df)

    return results


def _fmt_num(v: float) -> str:
    if v is None:
        return "—"
    if abs(v) >= 10 or (abs(v) < 0.001 and v != 0):
        return f"{v:.4g}"
    return f"{v:.4f}"


def _row_for_md(name: str, m: dict) -> dict[str, str]:
    cols = [
        "cumulative_return", "annualized_return", "sharpe", "sortino",
        "max_drawdown", "calmar", "excess_cumulative_return",
        "information_ratio", "hit_rate", "profit_factor",
    ]
    row: dict[str, str] = {"strategy": name}
    for c in cols:
        val = m.get(c)
        row[c] = _fmt_num(val) if val is not None else "—"
    return row


def run_compare(
    agent_dir: Path,
    deep_artifacts_dir: Path,
    run_id: str = "full_universe_2015_2025_20260309",
    symbol: str = "BTCUSDT",
    output_path: Path | None = None,
) -> Path:
    """Compare agent vs forecasting models on pilot windows."""
    agent_metrics_path = agent_dir / "agent_metrics.json"
    if not agent_metrics_path.exists():
        raise FileNotFoundError(f"Agent metrics not found: {agent_metrics_path}")

    with agent_metrics_path.open() as f:
        agent_data = json.load(f)
    agent_agg = agent_data["aggregate"]

    artifacts_root = deep_artifacts_dir / run_id
    if not artifacts_root.exists():
        raise FileNotFoundError(f"Deep-trading artifacts not found: {artifacts_root}")

    forecast_metrics = _load_forecast_metrics_on_pilot(artifacts_root, symbol)

    out = output_path or agent_dir
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# Agent vs Forecasting Models — Pilot Comparison")
    lines.append("")
    lines.append("**Evaluation period:** 60 days across 3 pilot windows (2025)")
    lines.append("- Window 0: 2025-02-24 → 2025-03-15")
    lines.append("- Window 1: 2025-04-09 → 2025-04-28")
    lines.append("- Window 2: 2025-11-03 → 2025-11-22")
    lines.append("")
    lines.append("All strategies evaluated on the **exact same bars** using deep-trading metrics.")
    lines.append("")
    lines.append("---")
    lines.append("")

    cols = ["strategy", "cumulative_return", "annualized_return", "sharpe", "sortino",
            "max_drawdown", "calmar", "excess_cumulative_return",
            "information_ratio", "hit_rate", "profit_factor"]

    rows: list[dict[str, str]] = []
    rows.append(_row_for_md("**trading_agent**", agent_agg))
    for strat in STRATEGIES:
        m = forecast_metrics.get(strat)
        if m:
            rows.append(_row_for_md(strat, m))

    lines.append("## 1. Aggregate Comparison (All Pilot Windows)")
    lines.append("")
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join("---" for _ in cols) + " |")
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(c, "—")) for c in cols) + " |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 2. Benchmark Reference")
    lines.append("")
    bench_cr = agent_agg.get("benchmark_cumulative_return")
    lines.append(f"- **Buy-and-hold (pilot windows):** cumulative return = {_fmt_num(bench_cr)}")
    lines.append("")

    md_path = out / "comparison_agent_vs_forecast.md"
    md_path.write_text("\n".join(lines))

    comparison = {
        "agent": agent_agg,
        "forecast": {k: v for k, v in forecast_metrics.items() if v},
    }
    with (out / "comparison_agent_vs_forecast.json").open("w") as f:
        json.dump(comparison, f, indent=2, default=str)

    return md_path


def _signal_dates_from_csv(signals_path: Path) -> set[date]:
    df = pd.read_csv(signals_path, parse_dates=["date"])
    return set(pd.to_datetime(df["date"]).dt.date)


def _signal_calendar_span_from_csv(signals_path: Path) -> set[date]:
    """All calendar days from min(signal date) through max(signal date), inclusive.

    Matches ``run_eval`` forward-fill so sparse decisions (e.g. ``date_stride`` > 1)
    still align baselines on every day the agent was effectively invested.
    """
    df = pd.read_csv(signals_path, parse_dates=["date"])
    if len(df) == 0:
        return set()
    dmin = pd.to_datetime(df["date"]).dt.date.min()
    dmax = pd.to_datetime(df["date"]).dt.date.max()
    out: set[date] = set()
    d = dmin
    while d <= dmax:
        out.add(d)
        d += timedelta(days=1)
    return out


def _load_forecast_metrics_on_dates(
    artifacts_root: Path,
    symbol: str,
    dates: set[date],
) -> dict[str, dict[str, Any]]:
    """Slice each strategy backtest to calendar dates present in ``dates``."""
    results: dict[str, dict[str, Any]] = {}

    for strategy in STRATEGIES:
        path = artifacts_root / symbol / strategy / "backtest.csv"
        if not path.exists():
            results[strategy] = {}
            continue

        df = pd.read_csv(path, parse_dates=["timestamp"], index_col="timestamp")
        if df.index.tz is None:
            df.index = df.index.tz_localize("UTC")

        mask = df.index.map(lambda ts: ts.date() in dates)
        slice_df = df.loc[mask]
        if len(slice_df) == 0:
            results[strategy] = {}
            continue

        results[strategy] = _metrics_on_slice(slice_df)

    return results


def run_compare_for_signal_dates(
    agent_dir: Path,
    deep_artifacts_dir: Path,
    run_id: str,
    symbol: str = "BTCUSDT",
    output_path: Path | None = None,
) -> Path:
    """Like ``run_compare``, but baseline slices match ``signals.csv`` dates."""
    agent_dir = Path(agent_dir)
    signals_path = agent_dir / "signals.csv"
    agent_metrics_path = agent_dir / "agent_metrics.json"

    if not signals_path.exists():
        raise FileNotFoundError(f"signals.csv not found: {signals_path}")
    if not agent_metrics_path.exists():
        raise FileNotFoundError(
            f"agent_metrics.json not found: {agent_metrics_path} "
            "(run `python -m agent_experiment.scripts.run_eval` first)"
        )

    dates = _signal_calendar_span_from_csv(signals_path)
    if not dates:
        raise ValueError(f"No dates parsed from {signals_path}")

    with agent_metrics_path.open() as f:
        agent_data = json.load(f)
    agent_agg = agent_data["aggregate"]

    artifacts_root = deep_artifacts_dir / run_id
    if not artifacts_root.exists():
        raise FileNotFoundError(f"Deep-trading artifacts not found: {artifacts_root}")

    forecast_metrics = _load_forecast_metrics_on_dates(artifacts_root, symbol, dates)

    out = output_path or agent_dir
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)

    dmin, dmax = min(dates), max(dates)
    lines: list[str] = []
    lines.append("# Agent vs Forecasting Models — Same-Calendar Comparison")
    lines.append("")
    lines.append(
        f"**Evaluation period:** {len(dates)} calendar days (dense span from first "
        f"to last signal date: {dmin} → {dmax}), aligned with ``run_eval`` forward-fill."
    )
    lines.append("")
    lines.append(
        "Forecast strategies are sliced to the **same hourly bars** on those "
        "dates; agent aggregate metrics come from `agent_metrics.json` "
        "(produced by `run_eval`)."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    cols = [
        "strategy",
        "cumulative_return",
        "annualized_return",
        "sharpe",
        "sortino",
        "max_drawdown",
        "calmar",
        "excess_cumulative_return",
        "information_ratio",
        "hit_rate",
        "profit_factor",
    ]

    rows: list[dict[str, str]] = []
    rows.append(_row_for_md("**trading_agent**", agent_agg))
    for strat in STRATEGIES:
        m = forecast_metrics.get(strat)
        if m:
            rows.append(_row_for_md(strat, m))

    lines.append("## Aggregate comparison (agent vs baselines on signal dates)")
    lines.append("")
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join("---" for _ in cols) + " |")
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(c, "—")) for c in cols) + " |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Benchmark reference")
    lines.append("")
    bench_cr = agent_agg.get("benchmark_cumulative_return")
    lines.append(
        f"- **Buy-and-hold (signal dates):** cumulative return = {_fmt_num(bench_cr)}"
    )
    lines.append("")

    md_path = out / "comparison_agent_vs_forecast_by_signals.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")

    comparison = {
        "signal_calendar_span": {
            "min": str(dmin),
            "max": str(dmax),
            "n_calendar_days": len(dates),
        },
        "agent": agent_agg,
        "forecast": {k: v for k, v in forecast_metrics.items() if v},
    }
    with (out / "comparison_agent_vs_forecast_by_signals.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(comparison, f, indent=2, default=str)

    return md_path
