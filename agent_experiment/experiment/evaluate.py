"""Evaluate agent signals using the deep-trading metrics pipeline.

Loads agent signals.csv, broadcasts daily positions to 1h bars,
and computes the exact same metrics that deep-trading uses for
its forecasting baselines.
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def _ensure_deep_trading_importable() -> None:
    """Add deep-trading to sys.path if needed."""
    try:
        from deep_trading.metrics.performance import compute_performance_metrics  # noqa: F401
        return
    except ImportError:
        pass

    deep_root = Path(__file__).resolve().parents[4] / "deep-trading"
    if deep_root.exists() and str(deep_root) not in sys.path:
        sys.path.insert(0, str(deep_root))


def load_signals(signals_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(signals_path, parse_dates=["date"])
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def load_ohlcv(data_path: str | Path) -> pd.DataFrame:
    df = pd.read_parquet(data_path)
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    return df


def _calendar_day_range(d0: date, d1: date) -> list[date]:
    out: list[date] = []
    d = d0
    while d <= d1:
        out.append(d)
        d += timedelta(days=1)
    return out


def _forward_fill_positions_by_day(signals_df: pd.DataFrame) -> dict[date, float]:
    """Map each calendar day in [min(date), max(date)] to the latest position known by that day."""
    df = signals_df.sort_values("date").drop_duplicates(subset=["date"], keep="last")
    if len(df) == 0:
        return {}

    cal_min = df["date"].min()
    cal_max = df["date"].max()
    rows = list(zip(df["date"].tolist(), df["position"].astype(float).tolist()))

    filled: dict[date, float] = {}
    j = 0
    current = 0.0
    for d in _calendar_day_range(cal_min, cal_max):
        while j < len(rows) and rows[j][0] <= d:
            current = float(rows[j][1])
            j += 1
        filled[d] = current
    return filled


def build_hourly_positions(
    signals_df: pd.DataFrame,
    ohlcv: pd.DataFrame,
) -> pd.DataFrame:
    """Map daily decisions onto 1h bars.

    Decisions may be sparse (e.g. ``date_stride`` > 1). Positions **forward-fill**
    until the next decision: every calendar day from the first to the last signal
    date uses the latest known position as of that day.
    """
    close = ohlcv["close"].astype(float)
    log_ret = np.log(close / close.shift(1))
    asset_return = np.expm1(log_ret.fillna(0.0))

    vol_24 = log_ret.rolling(24).std() * np.sqrt(24)

    day_to_position = _forward_fill_positions_by_day(signals_df)
    if not day_to_position:
        raise ValueError("signals_df has no valid dates")

    cal_min = min(day_to_position.keys())
    cal_max = max(day_to_position.keys())

    mask = ohlcv.index.map(lambda ts: cal_min <= ts.date() <= cal_max)
    eval_df = ohlcv.loc[mask].copy()

    if len(eval_df) == 0:
        raise ValueError("No OHLCV bars match the pilot dates")

    eval_df["position"] = eval_df.index.map(lambda ts: day_to_position[ts.date()])
    eval_df["asset_return"] = asset_return.reindex(eval_df.index).fillna(0.0)
    eval_df["realized_vol_24"] = vol_24.reindex(eval_df.index)
    eval_df["position_lag"] = eval_df["position"].shift(1).fillna(0.0)
    eval_df["turnover"] = eval_df["position"].diff().abs().fillna(
        eval_df["position"].abs()
    )

    return eval_df


def compute_metrics(
    eval_df: pd.DataFrame,
    fee_bps: float = 0.0,
    slippage_bps: float = 0.0,
    periods_per_year: int = 8766,
    vol_regime_quantile: float = 0.7,
) -> dict[str, Any]:
    """Compute the full deep-trading metric suite on the agent's positions."""
    _ensure_deep_trading_importable()
    from deep_trading.metrics.performance import (
        compute_performance_metrics,
        compute_regime_metrics,
    )

    total_cost_bps = float(fee_bps + slippage_bps)
    eval_df = eval_df.copy()
    eval_df["cost"] = eval_df["turnover"] * total_cost_bps / 10_000.0
    eval_df["gross_return"] = eval_df["position_lag"] * eval_df["asset_return"]
    eval_df["net_return"] = eval_df["gross_return"] - eval_df["cost"]
    eval_df["equity"] = (1.0 + eval_df["net_return"]).cumprod()

    metrics = compute_performance_metrics(
        net_returns=eval_df["net_return"],
        equity=eval_df["equity"],
        turnover=eval_df["turnover"],
        position_lag=eval_df["position_lag"],
        asset_return=eval_df["asset_return"],
        periods_per_year=periods_per_year,
    )

    metrics["regimes"] = compute_regime_metrics(
        eval_df, vol_regime_quantile, periods_per_year,
    )

    # Binary decision diagnostics
    positions = eval_df["position"]
    metrics["diagnostics"] = {
        "total_bars": len(positions),
        "fraction_long": float((positions > 0).mean()),
        "fraction_short": float((positions < 0).mean()),
        "fraction_flat": float((positions == 0).mean()),
        "flip_count": int((positions.diff().abs() > 1e-12).sum()),
    }

    return metrics


def compute_per_window_metrics(
    signals_df: pd.DataFrame,
    ohlcv: pd.DataFrame,
    fee_bps: float = 0.0,
    slippage_bps: float = 0.0,
    periods_per_year: int = 8766,
    vol_regime_quantile: float = 0.7,
) -> list[dict[str, Any]]:
    """Compute metrics separately for each pilot window."""
    results = []
    for widx in sorted(signals_df["window_idx"].unique()):
        w_signals = signals_df[signals_df["window_idx"] == widx]
        w_eval = build_hourly_positions(w_signals, ohlcv)
        w_metrics = compute_metrics(
            w_eval, fee_bps, slippage_bps, periods_per_year, vol_regime_quantile,
        )
        w_metrics["window_idx"] = int(widx)
        w_metrics["window_start"] = str(w_signals["date"].min())
        w_metrics["window_end"] = str(w_signals["date"].max())
        results.append(w_metrics)
    return results


def evaluate_pilot(
    signals_path: str | Path,
    data_path: str | Path,
    output_dir: str | Path | None = None,
    fee_bps: float = 0.0,
    slippage_bps: float = 0.0,
) -> dict[str, Any]:
    """Full evaluation: load signals, compute aggregate + per-window metrics, save."""
    signals_df = load_signals(signals_path)
    ohlcv = load_ohlcv(data_path)

    eval_df = build_hourly_positions(signals_df, ohlcv)
    aggregate = compute_metrics(eval_df, fee_bps, slippage_bps)
    per_window = compute_per_window_metrics(
        signals_df, ohlcv, fee_bps, slippage_bps,
    )

    result = {
        "aggregate": aggregate,
        "per_window": per_window,
    }

    if output_dir:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        with (out / "agent_metrics.json").open("w") as f:
            json.dump(result, f, indent=2, default=str)

        _print_summary(aggregate, per_window)

        flat = _flatten_for_csv(aggregate, per_window)
        pd.DataFrame(flat).to_csv(out / "agent_metrics.csv", index=False)

        eval_df.to_csv(out / "agent_backtest.csv")

        _write_summary_md(result, out)

    return result


# Same metric column order as deep-trading summary_metrics / forecasting models
_PRIMARY_COLS = [
    "strategy",
    "cumulative_return",
    "annualized_return",
    "annualized_volatility",
    "downside_volatility_annualized",
    "sharpe",
    "sortino",
    "max_drawdown",
    "calmar",
    "var_95",
    "cvar_95",
    "ulcer_index",
    "time_under_water_ratio",
]
_BENCHMARK_COLS = [
    "benchmark_cumulative_return",
    "benchmark_annualized_return",
    "excess_cumulative_return",
    "tracking_error_annualized",
    "information_ratio",
]
_EXECUTION_COLS = [
    "turnover_mean",
    "turnover_annualized",
    "hit_rate",
    "avg_holding_bars",
    "profit_factor",
]


def _fmt_num(v: float) -> str:
    if abs(v) >= 10 or (abs(v) < 0.001 and v != 0):
        return f"{v:.4g}"
    return f"{v:.4f}"


def _metrics_row(name: str, m: dict) -> dict[str, str]:
    """Build a row dict for markdown table (strategy + metric cols)."""
    row: dict[str, str] = {"strategy": name}
    for col in _PRIMARY_COLS[1:] + _BENCHMARK_COLS + _EXECUTION_COLS:
        val = m.get(col)
        if val is not None:
            row[col] = _fmt_num(val)
        else:
            row[col] = "—"
    return row


def _write_summary_md(result: dict[str, Any], out: Path) -> None:
    """Write summary_metrics.md in same format as deep-trading forecasting models."""
    agg = result["aggregate"]
    per_window = result["per_window"]

    lines: list[str] = []
    lines.append("# Agent Pilot — Summary Metrics")
    lines.append("")
    lines.append("Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Aggregate (All Pilot Windows)")
    lines.append("")
    row = _metrics_row("trading_agent", agg)
    cols = list(row.keys())
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join("---" for _ in cols) + " |")
    lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
    lines.append("")

    diag = agg.get("diagnostics", {})
    if diag:
        lines.append("**Diagnostics:** ")
        lines.append(f"- Bars: {diag.get('total_bars', '—')} | "
                    f"Long: {diag.get('fraction_long', 0):.1%} | "
                    f"Short: {diag.get('fraction_short', 0):.1%} | "
                    f"Flat: {diag.get('fraction_flat', 0):.1%} | "
                    f"Flips: {diag.get('flip_count', '—')}")
        lines.append("")

    regimes = agg.get("regimes", {})
    if regimes:
        lines.append("### 1.1 Regime Metrics (Aggregate)")
        lines.append("")
        lines.append("| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for regime, r in regimes.items():
            parts = [regime]
            for c in ["cumulative_return", "annualized_return", "annualized_volatility",
                      "sharpe", "sortino", "max_drawdown", "calmar", "cvar_95"]:
                parts.append(_fmt_num(r.get(c, 0)) if r.get(c) is not None else "—")
            lines.append("| " + " | ".join(parts) + " |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 2. Per-Window Metrics")
    lines.append("")
    for w in per_window:
        label = f"Window {w['window_idx']}: {w['window_start']} → {w['window_end']}"
        lines.append(f"### 2.{w['window_idx'] + 1} {label}")
        lines.append("")
        row = _metrics_row(f"trading_agent (w{w['window_idx']})", w)
        cols = list(row.keys())
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("| " + " | ".join("---" for _ in cols) + " |")
        lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
        lines.append("")
        w_regimes = w.get("regimes", {})
        if w_regimes:
            lines.append("| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |")
            lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
            for regime, r in w_regimes.items():
                parts = [regime]
                for c in ["cumulative_return", "annualized_return", "sharpe", "sortino",
                          "max_drawdown", "calmar", "cvar_95"]:
                    parts.append(_fmt_num(r.get(c, 0)) if r.get(c) is not None else "—")
                lines.append("| " + " | ".join(parts) + " |")
            lines.append("")
        w_diag = w.get("diagnostics", {})
        if w_diag:
            lines.append(f"*Bars: {w_diag.get('total_bars', '—')} | "
                        f"Long: {w_diag.get('fraction_long', 0):.1%} | "
                        f"Short: {w_diag.get('fraction_short', 0):.1%} | "
                        f"Flat: {w_diag.get('fraction_flat', 0):.1%} | "
                        f"Flips: {w_diag.get('flip_count', '—')}*")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 3. Metric Definitions (from deep-trading)")
    lines.append("")
    lines.append("| Metric | Description |")
    lines.append("| --- | --- |")
    lines.append("| cumulative_return | Total strategy return |")
    lines.append("| annualized_return | Annualized return |")
    lines.append("| sharpe | Sharpe ratio |")
    lines.append("| max_drawdown | Maximum drawdown |")
    lines.append("| sortino | Sortino ratio |")
    lines.append("| calmar | Calmar ratio (return / max drawdown) |")
    lines.append("| excess_cumulative_return | Strategy − benchmark |")
    lines.append("| information_ratio | Excess return / tracking error |")
    lines.append("| hit_rate | Fraction of bars with correct direction |")
    lines.append("| turnover_annualized | Annualized turnover |")
    lines.append("| profit_factor | Gains / losses |")
    lines.append("")

    (out / "summary_metrics.md").write_text("\n".join(lines))


def _flatten_for_csv(
    aggregate: dict, per_window: list[dict],
) -> list[dict[str, Any]]:
    rows = []
    rows.append(_flatten_one("aggregate", aggregate))
    for w in per_window:
        label = f"window_{w['window_idx']}_{w['window_start']}_{w['window_end']}"
        rows.append(_flatten_one(label, w))
    return rows


def _flatten_one(label: str, metrics: dict) -> dict[str, Any]:
    row: dict[str, Any] = {"scope": label}
    for k, v in metrics.items():
        if isinstance(v, dict):
            continue
        row[k] = v
    diag = metrics.get("diagnostics", {})
    for k, v in diag.items():
        row[f"diag_{k}"] = v
    return row


def _print_summary(aggregate: dict, per_window: list[dict]) -> None:
    print()
    print("=" * 60)
    print("AGENT PILOT EVALUATION")
    print("=" * 60)

    def _fmt(m: dict, label: str) -> None:
        print(f"\n--- {label} ---")
        print(f"  Cumulative return:  {m['cumulative_return']:+.4f}")
        print(f"  Annualized return:  {m['annualized_return']:+.4f}")
        print(f"  Sharpe:             {m['sharpe']:+.4f}")
        print(f"  Sortino:            {m['sortino']:+.4f}")
        print(f"  Max drawdown:       {m['max_drawdown']:+.4f}")
        print(f"  Hit rate:           {m['hit_rate']:.4f}")
        print(f"  Turnover (mean):    {m['turnover_mean']:.4f}")
        print(f"  Profit factor:      {m['profit_factor']:.4f}")
        diag = m.get("diagnostics", {})
        if diag:
            print(f"  Bars: {diag.get('total_bars', '?')}  "
                  f"Long: {diag.get('fraction_long', 0):.0%}  "
                  f"Short: {diag.get('fraction_short', 0):.0%}  "
                  f"Flat: {diag.get('fraction_flat', 0):.0%}  "
                  f"Flips: {diag.get('flip_count', '?')}")

    _fmt(aggregate, "AGGREGATE (all windows)")
    for w in per_window:
        _fmt(w, f"Window {w['window_idx']}: {w['window_start']} → {w['window_end']}")

    print()
    print("=" * 60)
