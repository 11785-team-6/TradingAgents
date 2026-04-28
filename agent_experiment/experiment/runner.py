"""Batch runner for the pilot experiment.

Iterates over pilot window dates, calls TradingAgentsGraph.propagate()
once per calendar day, collects tri-state decisions, and returns a
DataFrame of results.

On failure (e.g. LLM hallucinating bad tool arguments), the runner
retries with a fresh graph up to ``max_retries`` times before recording
an error for that date and moving on.

This module imports TradingAgents but never modifies it.
"""

from __future__ import annotations

import logging
import sys
import time
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

from .config import ExperimentConfig

logger = logging.getLogger(__name__)

MAX_RETRIES_DEFAULT = 3
RETRY_BACKOFF_S = 5


def _configure_model_metrics_for_pilot(exp_config: ExperimentConfig) -> None:
    """Point get_model_metrics at deep-trading artifacts when running hybrid pilot."""
    from tradingagents.agents.utils.model_metrics_tool import (
        reset_leakage_audit_records,
        set_artifacts_dir,
        set_deep_trading_symbol,
        set_deep_trading_run_id,
        set_model_strategies,
    )

    if exp_config.deep_trading_artifacts_dir:
        artifacts_path = Path(exp_config.deep_trading_artifacts_dir)
        if not artifacts_path.is_absolute():
            artifacts_path = (
                Path(__file__).resolve().parents[2] / artifacts_path
            ).resolve()
        else:
            artifacts_path = artifacts_path.resolve()
        set_artifacts_dir(str(artifacts_path))
    if "model" in exp_config.selected_analysts:
        if not exp_config.deep_trading_artifacts_dir:
            logger.warning(
                "selected_analysts includes 'model' but deep_trading_artifacts_dir "
                "is unset — get_model_metrics may return not_found."
            )
        if not exp_config.deep_trading_run_id:
            logger.warning(
                "selected_analysts includes 'model' but deep_trading_run_id is unset — "
                "artifact lookup may mix versions across runs."
            )
        set_deep_trading_symbol(exp_config.symbol_deep_trading)
        set_deep_trading_run_id(exp_config.deep_trading_run_id)
        set_model_strategies(exp_config.model_strategies)
        reset_leakage_audit_records()
    else:
        set_deep_trading_symbol(None)
        set_deep_trading_run_id(None)
        set_model_strategies(None)
        reset_leakage_audit_records()


@dataclass
class DayResult:
    date: date
    decision_raw: str
    position: float
    latency_s: float
    error: str | None = None
    window_idx: int = 0
    attempts: int = 1


@dataclass
class PilotResult:
    config: ExperimentConfig
    results: list[DayResult] = field(default_factory=list)
    leakage_audit: list[dict[str, Any]] = field(default_factory=list)
    run_id: str = ""

    def to_dataframe(self) -> pd.DataFrame:
        rows = []
        for r in self.results:
            rows.append({
                "date": r.date.isoformat(),
                "window_idx": r.window_idx,
                "decision_raw": r.decision_raw,
                "position": r.position,
                "latency_s": round(r.latency_s, 2),
                "attempts": r.attempts,
                "error": r.error or "",
            })
        return pd.DataFrame(rows)


def _ensure_tradingagents_importable() -> None:
    """Add TradingAgents source root to sys.path if not already importable."""
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph  # noqa: F401
        return
    except ImportError:
        pass

    ta_root = Path(__file__).resolve().parents[2]
    if str(ta_root) not in sys.path:
        sys.path.insert(0, str(ta_root))


def _build_graph(
    exp_config: ExperimentConfig,
) -> Any:
    """Construct a TradingAgentsGraph from the experiment config."""
    _ensure_tradingagents_importable()
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG

    agent_cfg = exp_config.to_agent_config(DEFAULT_CONFIG)

    return TradingAgentsGraph(
        selected_analysts=exp_config.selected_analysts,
        config=agent_cfg,
        debug=False,
    )


def _run_single_day(
    graph: Any,
    exp_config: ExperimentConfig,
    date_str: str,
    d: date,
    window_idx: int,
    max_retries: int,
) -> tuple[DayResult, list[dict[str, Any]]]:
    """Run propagate for one date with retry logic.

    On each failure the graph is rebuilt to get a fresh LLM context,
    then retried after a short backoff.  Non-deterministic LLM errors
    (e.g. hallucinated tool arguments) typically succeed on retry.
    """
    from .signal_map import parse_decision, decision_to_position
    from tradingagents.agents.utils.model_metrics_tool import (
        get_leakage_audit_records,
        reset_leakage_audit_records,
    )

    last_error: str | None = None
    total_elapsed = 0.0

    for attempt in range(1, max_retries + 1):
        reset_leakage_audit_records()
        t0 = time.time()
        try:
            _final_state, decision_raw = graph.propagate(
                exp_config.symbol_agent, date_str
            )
            elapsed = time.time() - t0
            total_elapsed += elapsed

            decision = parse_decision(decision_raw)
            position = decision_to_position(
                decision,
                hold_position=exp_config.hold_position,
            )

            if attempt > 1:
                logger.info(
                    "    %s → %s (pos=%.1f) in %.1fs [succeeded on attempt %d]",
                    date_str, decision, position, total_elapsed, attempt,
                )
            else:
                logger.info(
                    "    %s → %s (pos=%.1f) in %.1fs",
                    date_str, decision, position, elapsed,
                )

            return DayResult(
                date=d,
                decision_raw=decision_raw.strip(),
                position=position,
                latency_s=total_elapsed,
                window_idx=window_idx,
                attempts=attempt,
            ), get_leakage_audit_records()

        except Exception as exc:
            elapsed = time.time() - t0
            total_elapsed += elapsed
            last_error = str(exc)

            if attempt < max_retries:
                logger.warning(
                    "    %s attempt %d/%d FAILED: %s — rebuilding graph and retrying in %ds",
                    date_str, attempt, max_retries, exc, RETRY_BACKOFF_S,
                )
                time.sleep(RETRY_BACKOFF_S)
                try:
                    graph = _build_graph(exp_config)
                except Exception as rebuild_exc:
                    logger.error(
                        "    Graph rebuild failed: %s — aborting retries for %s",
                        rebuild_exc, date_str,
                    )
                    break
            else:
                logger.error(
                    "    %s FAILED after %d attempts (%.1fs total): %s",
                    date_str, max_retries, total_elapsed, exc,
                )

    return DayResult(
        date=d,
        decision_raw="",
        position=exp_config.hold_position,
        latency_s=total_elapsed,
        error=last_error,
        window_idx=window_idx,
        attempts=max_retries,
    ), get_leakage_audit_records()


def run_pilot(
    exp_config: ExperimentConfig,
    *,
    dry_run: bool = False,
    max_retries: int = MAX_RETRIES_DEFAULT,
) -> PilotResult:
    """Run the full pilot experiment.

    Args:
        exp_config: Loaded experiment configuration.
        dry_run: If True, use mock provider (no GPU needed).
        max_retries: Max attempts per date before recording an error.

    Returns:
        PilotResult with one DayResult per scheduled decision date (respecting
        ``date_stride`` within each pilot window).
    """
    if dry_run:
        exp_config = _as_mock(exp_config)

    _configure_model_metrics_for_pilot(exp_config)

    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    pilot = PilotResult(config=exp_config, run_id=run_id)

    logger.info(
        "Starting pilot run %s — %d decision dates (date_stride=%d), symbol=%s, "
        "provider=%s, max_retries=%d",
        run_id,
        exp_config.total_pilot_days(),
        exp_config.date_stride,
        exp_config.symbol_agent,
        exp_config.llm_provider,
        max_retries,
    )

    graph = _build_graph(exp_config)

    for window_idx, window in enumerate(exp_config.pilot_windows):
        logger.info(
            "Window %d: %s → %s (%d days)",
            window_idx,
            window.start,
            window.end,
            window.days,
        )

        for d in exp_config.dates_for_window(window):
            date_str = d.isoformat()
            logger.info("  Running %s ...", date_str)

            result, leakage_rows = _run_single_day(
                graph, exp_config, date_str, d, window_idx, max_retries,
            )
            pilot.results.append(result)
            pilot.leakage_audit.extend(leakage_rows)

    return pilot


def _as_mock(cfg: ExperimentConfig) -> ExperimentConfig:
    """Return a copy with the mock LLM provider for dry-run testing."""
    from dataclasses import replace
    return replace(
        cfg,
        llm_provider="mock",
        quick_think_llm="mock-quick",
        deep_think_llm="mock-deep",
    )
