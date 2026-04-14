#!/usr/bin/env python3
"""Run the agent pilot experiment.

Usage:
    # Full run with Ollama (default config)
    python -m agent_experiment.scripts.run_pilot

    # Custom config
    python -m agent_experiment.scripts.run_pilot --config agent_experiment/configs/pilot.yaml

    # Dry run with mock LLM (no GPU, ~30s)
    python -m agent_experiment.scripts.run_pilot --dry-run
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the agent vs forecast pilot experiment",
    )
    parser.add_argument(
        "--config",
        default=str(
            Path(__file__).resolve().parents[1] / "configs" / "pilot.yaml"
        ),
        help="Path to experiment YAML config (default: configs/pilot.yaml)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Use mock LLM provider (no GPU needed, fast validation)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Override artifacts output directory",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s  %(message)s",
        datefmt="%H:%M:%S",
    )

    from agent_experiment.experiment.config import load_config
    from agent_experiment.experiment.runner import run_pilot
    from agent_experiment.experiment.artifacts import save_pilot_artifacts

    config_path = Path(args.config)
    if not config_path.exists():
        logging.error("Config not found: %s", config_path)
        return 1

    exp_config = load_config(config_path)

    logging.info("Loaded config: %s", config_path)
    logging.info(
        "  Symbol: %s | Windows: %d | Decision days: %d | date_stride: %d | Provider: %s",
        exp_config.symbol_agent,
        len(exp_config.pilot_windows),
        exp_config.total_pilot_days(),
        exp_config.date_stride,
        exp_config.llm_provider,
    )
    for i, w in enumerate(exp_config.pilot_windows):
        logging.info("  Window %d: %s → %s (%dd)", i, w.start, w.end, w.days)

    if args.dry_run:
        logging.info("DRY RUN: using mock LLM provider")

    result = run_pilot(
        exp_config,
        dry_run=args.dry_run,
        max_retries=exp_config.max_retries,
    )

    out_dir = save_pilot_artifacts(result, base_dir=args.output_dir)
    logging.info("Artifacts saved to: %s", out_dir)

    df = result.to_dataframe()
    errors = df[df["error"] != ""]
    if len(errors) > 0:
        logging.warning("%d/%d dates had errors", len(errors), len(df))

    print()
    print(f"Run ID: {result.run_id}")
    print(f"Output: {out_dir}")
    print(f"Days:   {len(df)} ({len(errors)} errors)")
    print()
    print(df[["date", "decision_raw", "position", "latency_s"]].to_string(index=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
