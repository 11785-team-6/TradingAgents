"""Experiment configuration loader.

Reads pilot.yaml and produces typed config objects without touching
any TradingAgents internals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import yaml


@dataclass
class PilotWindow:
    start: date
    end: date

    @property
    def days(self) -> int:
        return (self.end - self.start).days + 1

    def date_list(self) -> list[date]:
        return [self.start + timedelta(days=i) for i in range(self.days)]


@dataclass
class ExperimentConfig:
    symbol_agent: str
    symbol_deep_trading: str
    test_pool_start: date
    test_pool_end: date
    pilot_windows: list[PilotWindow]

    # Tri-state: BUY=1, SELL=-1, HOLD=0
    hold_position: float = 0.0

    llm_provider: str = "ollama"
    quick_think_llm: str = "qwen3:8b"
    deep_think_llm: str = "qwen3:30b-a3b"
    backend_url: str = "http://localhost:11434/v1"

    max_debate_rounds: int = 1
    max_risk_discuss_rounds: int = 1
    selected_analysts: list[str] = field(
        default_factory=lambda: ["market", "news", "fundamentals"]
    )

    artifacts_dir: str = "outputs"
    max_retries: int = 3

    # Hybrid only: path to deep-trading artifacts root (…/model_artifacts). When
    # set and "model" is in selected_analysts, the pilot runner configures the
    # get_model_metrics tool before building the graph.
    deep_trading_artifacts_dir: str | None = None

    # Hybrid Model analyst: "metrics" = historical performance summary;
    # "signals" = per-strategy BUY/SELL/HOLD from last bar before trade date.
    model_input_mode: str = "metrics"

    # Subfolders under <run_id>/<SYMBOL>/… to query (default: full baseline set).
    model_strategies: list[str] | None = None
    # Optional fixed run folder under deep_trading_artifacts_dir; when set,
    # model tools only read this run to prevent accidental cross-run mixing.
    deep_trading_run_id: str | None = None

    # Optional label stored in metadata.json (e.g. daily_2025_pure).
    experiment_name: str | None = None

    # Run propagate every Nth calendar day within each pilot window (1 = daily).
    date_stride: int = 1

    # LlamaCpp-specific (optional)
    local_model_path_deep: str | None = None
    local_model_path_quick: str | None = None
    local_n_gpu_layers: int = -1
    local_n_ctx: int = 4096

    def dates_for_window(self, w: PilotWindow) -> list[date]:
        """Calendar dates in ``w`` sampled every ``date_stride`` days (first day always)."""
        dl = w.date_list()
        step = max(1, int(self.date_stride))
        return dl[::step]

    def all_pilot_dates(self) -> list[date]:
        dates: list[date] = []
        for w in self.pilot_windows:
            dates.extend(self.dates_for_window(w))
        return sorted(set(dates))

    def total_pilot_days(self) -> int:
        return len(self.all_pilot_dates())

    def to_agent_config(self, base_config: dict[str, Any]) -> dict[str, Any]:
        """Overlay experiment settings onto TradingAgents DEFAULT_CONFIG."""
        cfg = base_config.copy()
        cfg["llm_provider"] = self.llm_provider
        cfg["quick_think_llm"] = self.quick_think_llm
        cfg["deep_think_llm"] = self.deep_think_llm
        cfg["backend_url"] = self.backend_url
        cfg["max_debate_rounds"] = self.max_debate_rounds
        cfg["max_risk_discuss_rounds"] = self.max_risk_discuss_rounds

        if self.local_model_path_deep:
            cfg["local_model_path_deep"] = self.local_model_path_deep
        if self.local_model_path_quick:
            cfg["local_model_path_quick"] = self.local_model_path_quick
        if self.llm_provider == "llamacpp":
            cfg["local_n_gpu_layers"] = self.local_n_gpu_layers
            cfg["local_n_ctx"] = self.local_n_ctx

        cfg["model_input_mode"] = self.model_input_mode

        return cfg


def _parse_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def load_config(path: str | Path) -> ExperimentConfig:
    with Path(path).open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    windows = [
        PilotWindow(start=_parse_date(w["start"]), end=_parse_date(w["end"]))
        for w in raw.get("pilot_windows", [])
    ]

    stride = int(raw.get("date_stride", 1))
    if stride < 1:
        raise ValueError("date_stride must be >= 1")

    mode = (raw.get("model_input_mode") or "metrics").lower().strip()
    if mode not in ("metrics", "signals"):
        raise ValueError("model_input_mode must be 'metrics' or 'signals'")

    mstrat = raw.get("model_strategies")
    if mstrat is not None and not isinstance(mstrat, list):
        raise TypeError("model_strategies must be a list of strings or omitted")

    return ExperimentConfig(
        symbol_agent=raw["symbol_agent"],
        symbol_deep_trading=raw.get("symbol_deep_trading", raw["symbol_agent"]),
        test_pool_start=_parse_date(raw["test_pool_start"]),
        test_pool_end=_parse_date(raw["test_pool_end"]),
        pilot_windows=windows,
        hold_position=float(raw.get("hold_position", 0.0)),
        llm_provider=raw.get("llm_provider", "ollama"),
        quick_think_llm=raw.get("quick_think_llm", "qwen3:8b"),
        deep_think_llm=raw.get("deep_think_llm", "qwen3:30b-a3b"),
        backend_url=raw.get("backend_url", "http://localhost:11434/v1"),
        max_debate_rounds=int(raw.get("max_debate_rounds", 1)),
        max_risk_discuss_rounds=int(raw.get("max_risk_discuss_rounds", 1)),
        selected_analysts=raw.get(
            "selected_analysts", ["market", "news", "fundamentals"]
        ),
        artifacts_dir=raw.get("artifacts_dir", "outputs"),
        max_retries=int(raw.get("max_retries", 3)),
        deep_trading_artifacts_dir=raw.get("deep_trading_artifacts_dir"),
        model_input_mode=mode,
        model_strategies=mstrat,
        deep_trading_run_id=raw.get("deep_trading_run_id"),
        experiment_name=raw.get("experiment_name"),
        date_stride=stride,
        local_model_path_deep=raw.get("local_model_path_deep"),
        local_model_path_quick=raw.get("local_model_path_quick"),
        local_n_gpu_layers=int(raw.get("local_n_gpu_layers", -1)),
        local_n_ctx=int(raw.get("local_n_ctx", 4096)),
    )
