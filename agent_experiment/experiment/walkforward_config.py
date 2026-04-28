"""Walk-forward experiment configuration loader.

Reads walkforward.yaml and produces typed config objects for the
Agent + Model walk-forward experiment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import yaml


@dataclass
class SymbolPair:
    symbol_agent: str        # yfinance ticker (e.g. BTC-USD)
    symbol_deep_trading: str  # deep-trading symbol (e.g. BTC/USDT)


@dataclass
class WalkForwardWindow:
    """A single 45-day walk-forward window."""
    start: date
    end: date
    index: int

    @property
    def days(self) -> int:
        return (self.end - self.start).days + 1

    def date_list(self) -> list[date]:
        return [self.start + timedelta(days=i) for i in range(self.days)]


@dataclass
class WalkForwardConfig:
    symbols: list[SymbolPair]
    test_start: date
    test_end: date
    walk_forward_retrain_days: int
    deep_trading_artifacts_dir: str

    hold_position: float = 0.0

    llm_provider: str = "ollama"
    quick_think_llm: str = "qwen3:8b"
    deep_think_llm: str = "qwen3:30b-a3b"
    backend_url: str = "http://localhost:11434/v1"

    max_debate_rounds: int = 1
    max_risk_discuss_rounds: int = 1
    selected_analysts: list[str] = field(
        default_factory=lambda: ["market", "news", "fundamentals", "model"]
    )

    artifacts_dir: str = "outputs"
    max_retries: int = 3

    # LlamaCpp-specific (optional)
    local_model_path_deep: str | None = None
    local_model_path_quick: str | None = None
    local_n_gpu_layers: int = -1
    local_n_ctx: int = 4096

    def generate_windows(self) -> list[WalkForwardWindow]:
        """Generate walk-forward windows from test_start to test_end."""
        windows = []
        idx = 0
        current = self.test_start
        while current < self.test_end:
            window_end = min(
                current + timedelta(days=self.walk_forward_retrain_days - 1),
                self.test_end,
            )
            windows.append(WalkForwardWindow(
                start=current,
                end=window_end,
                index=idx,
            ))
            idx += 1
            current = current + timedelta(days=self.walk_forward_retrain_days)
        return windows

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

        return cfg


def _parse_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def load_walkforward_config(path: str | Path) -> WalkForwardConfig:
    with Path(path).open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    symbols = [
        SymbolPair(
            symbol_agent=s["symbol_agent"],
            symbol_deep_trading=s["symbol_deep_trading"],
        )
        for s in raw.get("symbols", [])
    ]

    return WalkForwardConfig(
        symbols=symbols,
        test_start=_parse_date(raw["test_start"]),
        test_end=_parse_date(raw["test_end"]),
        walk_forward_retrain_days=int(raw.get("walk_forward_retrain_days", 45)),
        deep_trading_artifacts_dir=raw["deep_trading_artifacts_dir"],
        hold_position=float(raw.get("hold_position", 0.0)),
        llm_provider=raw.get("llm_provider", "ollama"),
        quick_think_llm=raw.get("quick_think_llm", "qwen3:8b"),
        deep_think_llm=raw.get("deep_think_llm", "qwen3:30b-a3b"),
        backend_url=raw.get("backend_url", "http://localhost:11434/v1"),
        max_debate_rounds=int(raw.get("max_debate_rounds", 1)),
        max_risk_discuss_rounds=int(raw.get("max_risk_discuss_rounds", 1)),
        selected_analysts=raw.get(
            "selected_analysts", ["market", "news", "fundamentals", "model"]
        ),
        artifacts_dir=raw.get("artifacts_dir", "outputs"),
        max_retries=int(raw.get("max_retries", 3)),
        local_model_path_deep=raw.get("local_model_path_deep"),
        local_model_path_quick=raw.get("local_model_path_quick"),
        local_n_gpu_layers=int(raw.get("local_n_gpu_layers", -1)),
        local_n_ctx=int(raw.get("local_n_ctx", 4096)),
    )
