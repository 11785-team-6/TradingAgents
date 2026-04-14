#!/usr/bin/env python3
"""Compare agent results with forecasting models on the same dates as signals.csv.

Requires ``agent_metrics.json`` from ``run_eval`` and ``signals.csv`` from
``run_pilot``.  Writes ``comparison_agent_vs_forecast_by_signals.md`` (and .json).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

pkg_root = Path(__file__).resolve().parents[2]
if str(pkg_root) not in sys.path:
    sys.path.insert(0, str(pkg_root))

# Repo layout: .../code/hybrid/TradingAgents → deep-trading at .../code/deep-trading
deep_root = pkg_root.parent.parent / "deep-trading"
if deep_root.exists() and str(deep_root) not in sys.path:
    sys.path.insert(0, str(deep_root))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compare agent vs forecasting models on dates present in signals.csv"
        ),
    )
    parser.add_argument(
        "--agent-dir",
        required=True,
        help="Directory containing signals.csv and agent_metrics.json",
    )
    parser.add_argument(
        "--deep-artifacts",
        default=str(pkg_root / "agent_experiment" / "model_artifacts"),
        help="Path to deep-trading artifacts root (contains <run_id>/BTCUSDT/...)",
    )
    parser.add_argument(
        "--run-id",
        required=True,
        help="Deep-trading run folder name under artifacts (e.g. full_universe_...)",
    )
    parser.add_argument(
        "--symbol",
        default="BTCUSDT",
        help="Symbol folder inside the run_id directory",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output directory (default: same as --agent-dir)",
    )
    args = parser.parse_args()

    agent_dir = Path(args.agent_dir)
    if not agent_dir.exists():
        print(f"ERROR: Agent dir not found: {agent_dir}")
        return 1

    deep_artifacts = Path(args.deep_artifacts)
    if not deep_artifacts.exists():
        print(f"ERROR: Deep-trading artifacts not found: {deep_artifacts}")
        return 1

    from agent_experiment.experiment.compare import run_compare_for_signal_dates

    md_path = run_compare_for_signal_dates(
        agent_dir=agent_dir,
        deep_artifacts_dir=deep_artifacts,
        run_id=args.run_id,
        symbol=args.symbol,
        output_path=Path(args.output) if args.output else None,
    )

    print(f"Comparison written to: {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
