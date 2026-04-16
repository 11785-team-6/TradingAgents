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


def _load_agent_aggregate(agent_dir: Path) -> dict[str, Any]:
    path = agent_dir / "agent_metrics.json"
    if not path.exists():
        raise FileNotFoundError(f"agent_metrics.json not found: {path}")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data["aggregate"]


def _label_from_metadata(agent_dir: Path, fallback: str) -> str:
    meta_path = agent_dir / "metadata.json"
    if not meta_path.exists():
        return fallback
    try:
        with meta_path.open(encoding="utf-8") as f:
            meta = json.load(f)
        name = meta.get("experiment_name") or meta.get("run_id")
        return str(name) if name else fallback
    except (json.JSONDecodeError, OSError):
        return fallback


def run_pure_hybrid_traditional_comparison(
    pure_dir: Path,
    hybrid_metrics_dir: Path,
    deep_artifacts_dir: Path,
    run_id: str,
    symbol: str = "BTCUSDT",
    hybrid_signals_dir: Path | None = None,
    output_path: Path | None = None,
    signals_reference_dir: Path | None = None,
) -> Path:
    """Single report: LLM runs (Pure + Hybrid variants) vs traditional forecast baselines.

    Traditional strategies use the same hourly slice as ``run_compare_for_signal_dates``,
    with the calendar span taken from ``signals_reference_dir`` (default: ``pure_dir``).
    Each LLM arm must have ``agent_metrics.json`` from ``run_eval``.
    """
    pure_dir = Path(pure_dir)
    hybrid_metrics_dir = Path(hybrid_metrics_dir)
    ref = Path(signals_reference_dir) if signals_reference_dir else pure_dir
    signals_path = ref / "signals.csv"
    if not signals_path.exists():
        raise FileNotFoundError(f"signals.csv not found (reference): {signals_path}")

    dates = _signal_calendar_span_from_csv(signals_path)
    if not dates:
        raise ValueError(f"No dates in {signals_path}")

    pure_agg = _load_agent_aggregate(pure_dir)
    hy_m_agg = _load_agent_aggregate(hybrid_metrics_dir)
    hy_s_agg = None
    if hybrid_signals_dir is not None:
        hsp = Path(hybrid_signals_dir)
        if not hsp.is_dir():
            raise FileNotFoundError(f"hybrid_signals_dir not found: {hsp}")
        hy_s_agg = _load_agent_aggregate(hsp)

    artifacts_root = deep_artifacts_dir / run_id
    if not artifacts_root.exists():
        raise FileNotFoundError(f"Deep-trading artifacts not found: {artifacts_root}")

    forecast_metrics = _load_forecast_metrics_on_dates(artifacts_root, symbol, dates)

    out = Path(output_path) if output_path else pure_dir
    out.mkdir(parents=True, exist_ok=True)

    dmin, dmax = min(dates), max(dates)

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
    rows.append(
        _row_for_md(
            f"**LLM Pure** ({_label_from_metadata(pure_dir, 'pure')})",
            pure_agg,
        )
    )
    rows.append(
        _row_for_md(
            f"**LLM Hybrid (metrics)** ({_label_from_metadata(hybrid_metrics_dir, 'hybrid_metrics')})",
            hy_m_agg,
        )
    )
    if hy_s_agg is not None:
        rows.append(
            _row_for_md(
                f"**LLM Hybrid (signals)** ({_label_from_metadata(Path(hybrid_signals_dir), 'hybrid_signals')})",
                hy_s_agg,
            )
        )

    lines: list[str] = []
    lines.append("# Pure vs Hybrid vs Traditional — Combined Comparison")
    lines.append("")
    lines.append(
        f"**Evaluation window:** {len(dates)} calendar days (dense span {dmin} → {dmax}), "
        f"from reference `signals.csv` in `{ref}`."
    )
    lines.append("")
    lines.append(
        "LLM rows use `agent_metrics.json` (post–`run_eval`). Traditional rows are "
        "non-agent forecast baselines sliced to the **same** hourly bars on those dates."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## LLM agents vs traditional forecasts")
    lines.append("")
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join("---" for _ in cols) + " |")
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(c, "—")) for c in cols) + " |")

    lines.append("")
    lines.append("## Traditional forecasting baselines (same dates)")
    lines.append("")
    trad_rows: list[dict[str, str]] = []
    for strat in STRATEGIES:
        m = forecast_metrics.get(strat)
        if m:
            trad_rows.append(_row_for_md(strat, m))
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join("---" for _ in cols) + " |")
    for r in trad_rows:
        lines.append("| " + " | ".join(str(r.get(c, "—")) for c in cols) + " |")
    lines.append("")

    md_path = out / "comparison_pure_hybrid_traditional.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")

    payload: dict[str, Any] = {
        "signal_calendar_span": {
            "min": str(dmin),
            "max": str(dmax),
            "n_calendar_days": len(dates),
            "signals_reference_dir": str(ref),
        },
        "deep_artifacts": {"root": str(deep_artifacts_dir), "run_id": run_id, "symbol": symbol},
        "llm": {
            "pure": {"aggregate": pure_agg, "dir": str(pure_dir)},
            "hybrid_metrics": {"aggregate": hy_m_agg, "dir": str(hybrid_metrics_dir)},
            "hybrid_signals": (
                {"aggregate": hy_s_agg, "dir": str(hybrid_signals_dir)}
                if hy_s_agg is not None
                else None
            ),
        },
        "traditional_forecast": {k: v for k, v in forecast_metrics.items() if v},
    }
    json_path = out / "comparison_pure_hybrid_traditional.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)

    return md_path
