"""Save pilot experiment outputs to disk.

Produces:
  <artifacts_dir>/<run_id>/signals.csv      — per-day decisions
  <artifacts_dir>/<run_id>/metadata.json    — experiment metadata
  <artifacts_dir>/<run_id>/summary.txt      — human-readable summary
  <artifacts_dir>/<run_id>/leakage_audit.csv / .jsonl — per-iteration leakage checks
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd

from .config import ExperimentConfig
from .runner import PilotResult


def _date_serial(obj: object) -> str:
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Not serializable: {type(obj)}")


def save_pilot_artifacts(result: PilotResult, base_dir: str | Path | None = None) -> Path:
    """Write all pilot artifacts to disk.

    Returns the output directory path.
    """
    base = Path(base_dir or result.config.artifacts_dir)
    out_dir = base / result.run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    _save_signals(result, out_dir)
    _save_metadata(result, out_dir)
    _save_summary(result, out_dir)
    _save_leakage_audit(result, out_dir)

    return out_dir


def _save_signals(result: PilotResult, out_dir: Path) -> None:
    df = result.to_dataframe()
    df.to_csv(out_dir / "signals.csv", index=False)


def _save_metadata(result: PilotResult, out_dir: Path) -> None:
    cfg = result.config
    meta = {
        "run_id": result.run_id,
        "experiment_name": cfg.experiment_name,
        "symbol_agent": cfg.symbol_agent,
        "symbol_deep_trading": cfg.symbol_deep_trading,
        "deep_trading_artifacts_dir": cfg.deep_trading_artifacts_dir,
        "deep_trading_run_id": cfg.deep_trading_run_id,
        "test_pool_start": cfg.test_pool_start.isoformat(),
        "test_pool_end": cfg.test_pool_end.isoformat(),
        "pilot_windows": [
            {"start": w.start.isoformat(), "end": w.end.isoformat(), "days": w.days}
            for w in cfg.pilot_windows
        ],
        "total_pilot_days": cfg.total_pilot_days(),
        "date_stride": cfg.date_stride,
        "hold_position": cfg.hold_position,
        "llm_provider": cfg.llm_provider,
        "quick_think_llm": cfg.quick_think_llm,
        "deep_think_llm": cfg.deep_think_llm,
        "max_debate_rounds": cfg.max_debate_rounds,
        "selected_analysts": cfg.selected_analysts,
        "model_input_mode": cfg.model_input_mode,
        "model_strategies": cfg.model_strategies,
        "total_results": len(result.results),
        "errors": sum(1 for r in result.results if r.error),
        "leakage_checks_total": len(result.leakage_audit),
        "leakage_checks_failed": sum(
            1 for r in result.leakage_audit if not bool(r.get("ok", False))
        ),
    }
    with (out_dir / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, default=_date_serial)


def _save_summary(result: PilotResult, out_dir: Path) -> None:
    cfg = result.config
    lines = [
        f"Pilot Experiment Run: {result.run_id}",
        f"Symbol: {cfg.symbol_agent} (agent) / {cfg.symbol_deep_trading} (deep-trading)",
        f"Provider: {cfg.llm_provider} — quick={cfg.quick_think_llm}, deep={cfg.deep_think_llm}",
        f"Windows: {len(cfg.pilot_windows)}, Total days: {cfg.total_pilot_days()}",
        "",
    ]

    for i, window in enumerate(cfg.pilot_windows):
        w_results = [r for r in result.results if r.window_idx == i]
        buys = sum(1 for r in w_results if r.position > 0)
        sells = sum(1 for r in w_results if r.position < 0)
        holds = sum(1 for r in w_results if r.position == 0)
        errors = sum(1 for r in w_results if r.error)
        retried = sum(1 for r in w_results if r.attempts > 1)
        avg_latency = (
            sum(r.latency_s for r in w_results) / len(w_results)
            if w_results
            else 0
        )
        lines.append(f"Window {i}: {window.start} → {window.end} ({window.days}d)")
        lines.append(f"  BUY={buys}  SELL={sells}  HOLD={holds}  errors={errors}  retried={retried}")
        lines.append(f"  avg latency: {avg_latency:.1f}s")
        lines.append("")

    total_latency = sum(r.latency_s for r in result.results)
    total_retried = sum(1 for r in result.results if r.attempts > 1)
    lines.append(f"Total inference time: {total_latency:.0f}s ({total_latency/60:.1f}min)")
    lines.append(f"Total retried: {total_retried}/{len(result.results)} dates")
    if result.leakage_audit:
        n_total = len(result.leakage_audit)
        n_failed = sum(1 for r in result.leakage_audit if not bool(r.get("ok", False)))
        lines.append(f"Leakage checks: {n_total} total, {n_failed} failed")

    (out_dir / "summary.txt").write_text("\n".join(lines), encoding="utf-8")


def _save_leakage_audit(result: PilotResult, out_dir: Path) -> None:
    rows = result.leakage_audit
    if not rows:
        return

    df = pd.DataFrame(rows)
    sort_cols = [c for c in ["trade_date", "tool", "strategy"] if c in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols)
    df.to_csv(out_dir / "leakage_audit.csv", index=False)

    with (out_dir / "leakage_audit.jsonl").open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, default=_date_serial) + "\n")
