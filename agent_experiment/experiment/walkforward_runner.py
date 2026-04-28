"""Walk-forward batch runner for the Agent + Model experiment.

Iterates over 45-day walk-forward windows (matching deep-trading's
default.yaml), calls TradingAgentsGraph.propagate() once per window,
and collects tri-state decisions.

At each window the Model Analyst sees only metrics computed from data
*before* the window start date — no data leakage.
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

from .walkforward_config import WalkForwardConfig, SymbolPair, WalkForwardWindow

logger = logging.getLogger(__name__)

MAX_RETRIES_DEFAULT = 3
RETRY_BACKOFF_S = 5


@dataclass
class WindowResult:
    symbol: str
    window_idx: int
    window_start: date
    window_end: date
    decision_raw: str
    position: float
    latency_s: float
    error: str | None = None
    attempts: int = 1


@dataclass
class WalkForwardResult:
    config: WalkForwardConfig
    symbol_pair: SymbolPair
    results: list[WindowResult] = field(default_factory=list)
    run_id: str = ""

    def to_dataframe(self) -> pd.DataFrame:
        rows = []
        for r in self.results:
            rows.append({
                "symbol": r.symbol,
                "window_idx": r.window_idx,
                "window_start": r.window_start.isoformat(),
                "window_end": r.window_end.isoformat(),
                "decision_raw": r.decision_raw,
                "position": r.position,
                "latency_s": round(r.latency_s, 2),
                "attempts": r.attempts,
                "error": r.error or "",
            })
        return pd.DataFrame(rows)


def _ensure_tradingagents_importable() -> None:
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph  # noqa: F401
        return
    except ImportError:
        pass
    ta_root = Path(__file__).resolve().parents[2]
    if str(ta_root) not in sys.path:
        sys.path.insert(0, str(ta_root))


def _build_graph(
    wf_config: WalkForwardConfig,
) -> Any:
    """Construct a TradingAgentsGraph from the walk-forward config."""
    _ensure_tradingagents_importable()
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG

    agent_cfg = wf_config.to_agent_config(DEFAULT_CONFIG)

    return TradingAgentsGraph(
        selected_analysts=wf_config.selected_analysts,
        config=agent_cfg,
        debug=False,
    )


def _run_single_window(
    graph: Any,
    wf_config: WalkForwardConfig,
    symbol_pair: SymbolPair,
    window: WalkForwardWindow,
    max_retries: int,
) -> WindowResult:
    """Run propagate for one walk-forward window with retry logic.

    The agent is called with the window START date as the trade date.
    It makes one decision (BUY/SELL/HOLD) that applies for the entire
    45-day window.
    """
    from .signal_map import parse_decision, decision_to_position

    trade_date_str = window.start.isoformat()
    last_error: str | None = None
    total_elapsed = 0.0

    for attempt in range(1, max_retries + 1):
        t0 = time.time()
        try:
            _final_state, decision_raw = graph.propagate(
                symbol_pair.symbol_agent, trade_date_str
            )
            elapsed = time.time() - t0
            total_elapsed += elapsed

            decision = parse_decision(decision_raw)
            position = decision_to_position(
                decision,
                hold_position=wf_config.hold_position,
            )

            logger.info(
                "  Window %d [%s → %s] → %s (pos=%.1f) in %.1fs%s",
                window.index,
                window.start,
                window.end,
                decision,
                position,
                total_elapsed,
                f" [attempt {attempt}]" if attempt > 1 else "",
            )

            return WindowResult(
                symbol=symbol_pair.symbol_agent,
                window_idx=window.index,
                window_start=window.start,
                window_end=window.end,
                decision_raw=decision_raw.strip(),
                position=position,
                latency_s=total_elapsed,
                attempts=attempt,
            )

        except Exception as exc:
            elapsed = time.time() - t0
            total_elapsed += elapsed
            last_error = str(exc)

            if attempt < max_retries:
                logger.warning(
                    "  Window %d attempt %d/%d FAILED: %s — retrying in %ds",
                    window.index, attempt, max_retries, exc, RETRY_BACKOFF_S,
                )
                time.sleep(RETRY_BACKOFF_S)
                try:
                    graph = _build_graph(wf_config)
                except Exception as rebuild_exc:
                    logger.error(
                        "  Graph rebuild failed: %s — aborting retries",
                        rebuild_exc,
                    )
                    break
            else:
                logger.error(
                    "  Window %d FAILED after %d attempts (%.1fs): %s",
                    window.index, max_retries, total_elapsed, exc,
                )

    return WindowResult(
        symbol=symbol_pair.symbol_agent,
        window_idx=window.index,
        window_start=window.start,
        window_end=window.end,
        decision_raw="",
        position=wf_config.hold_position,
        latency_s=total_elapsed,
        error=last_error,
        attempts=max_retries,
    )


def run_walkforward(
    wf_config: WalkForwardConfig,
    symbol_pair: SymbolPair,
    *,
    dry_run: bool = False,
    max_retries: int = MAX_RETRIES_DEFAULT,
) -> WalkForwardResult:
    """Run the full walk-forward experiment for one symbol.

    Args:
        wf_config: Loaded walk-forward configuration.
        symbol_pair: The symbol to run (agent + deep-trading names).
        dry_run: If True, use mock provider.
        max_retries: Max attempts per window before recording an error.

    Returns:
        WalkForwardResult with one WindowResult per walk-forward window.
    """
    # Set the deep-trading artifacts directory so the model metrics tool
    # knows where to find backtest.csv files.
    from tradingagents.agents.utils.model_metrics_tool import (
        set_artifacts_dir,
        set_deep_trading_symbol,
    )
    
    artifacts_path = Path(wf_config.deep_trading_artifacts_dir)
    if not artifacts_path.is_absolute():
        # Resolve relative to this file's location
        artifacts_path = (Path(__file__).resolve().parents[2] / artifacts_path).resolve()
    set_artifacts_dir(str(artifacts_path))
    set_deep_trading_symbol(symbol_pair.symbol_deep_trading)

    if dry_run:
        wf_config = _as_mock(wf_config)

    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    result = WalkForwardResult(
        config=wf_config,
        symbol_pair=symbol_pair,
        run_id=run_id,
    )

    windows = wf_config.generate_windows()

    logger.info(
        "Starting walk-forward run %s — %d windows, symbol=%s, provider=%s",
        run_id,
        len(windows),
        symbol_pair.symbol_agent,
        wf_config.llm_provider,
    )

    graph = _build_graph(wf_config)

    for window in windows:
        logger.info(
            "Window %d: %s → %s (%d days)",
            window.index, window.start, window.end, window.days,
        )

        win_result = _run_single_window(
            graph, wf_config, symbol_pair, window, max_retries,
        )
        result.results.append(win_result)

    return result


def _as_mock(cfg: WalkForwardConfig) -> WalkForwardConfig:
    from dataclasses import replace
    return replace(
        cfg,
        llm_provider="mock",
        quick_think_llm="mock-quick",
        deep_think_llm="mock-deep",
    )
