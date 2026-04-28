#!/usr/bin/env python3
"""Run the Agent + Model walk-forward experiment.

Usage:
    # Full run with Ollama (default config)
    python -m agent_experiment.scripts.run_walkforward

    # Custom config
    python -m agent_experiment.scripts.run_walkforward --config agent_experiment/configs/walkforward.yaml

    # Dry run with mock LLM (no GPU, validates pipeline)
    python -m agent_experiment.scripts.run_walkforward --dry-run

    # Run only one symbol
    python -m agent_experiment.scripts.run_walkforward --symbol BTC-USD
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import pandas as pd


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run Agent+Model walk-forward experiment",
    )
    parser.add_argument(
        "--config",
        default=str(
            Path(__file__).resolve().parents[1] / "configs" / "walkforward.yaml"
        ),
        help="Path to experiment YAML config (default: configs/walkforward.yaml)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Use mock LLM provider (no GPU needed, fast validation)",
    )
    parser.add_argument(
        "--symbol",
        default=None,
        help="Run only this symbol (agent ticker, e.g. BTC-USD)",
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

    from agent_experiment.experiment.walkforward_config import load_walkforward_config
    from agent_experiment.experiment.walkforward_runner import run_walkforward

    config_path = Path(args.config)
    if not config_path.exists():
        logging.error("Config not found: %s", config_path)
        return 1

    wf_config = load_walkforward_config(config_path)

    windows = wf_config.generate_windows()
    logging.info("Loaded config: %s", config_path)
    logging.info(
        "  Test period: %s → %s | Windows: %d × %d days",
        wf_config.test_start,
        wf_config.test_end,
        len(windows),
        wf_config.walk_forward_retrain_days,
    )
    logging.info(
        "  Symbols: %s | Provider: %s | Analysts: %s",
        [s.symbol_agent for s in wf_config.symbols],
        wf_config.llm_provider,
        wf_config.selected_analysts,
    )
    logging.info(
        "  Deep-trading artifacts: %s",
        wf_config.deep_trading_artifacts_dir,
    )

    if args.dry_run:
        logging.info("DRY RUN: using mock LLM provider")

    # Filter symbols if --symbol is specified
    symbols_to_run = wf_config.symbols
    if args.symbol:
        symbols_to_run = [
            s for s in wf_config.symbols if s.symbol_agent == args.symbol
        ]
        if not symbols_to_run:
            logging.error("Symbol %s not found in config", args.symbol)
            return 1

    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out_base = Path(args.output_dir or wf_config.artifacts_dir)
    all_dfs = []

    for symbol_pair in symbols_to_run:
        logging.info("=" * 60)
        logging.info("Running symbol: %s", symbol_pair.symbol_agent)
        logging.info("=" * 60)

        result = run_walkforward(
            wf_config,
            symbol_pair,
            dry_run=args.dry_run,
            max_retries=wf_config.max_retries,
        )

        # Override run_id for consistent naming
        result.run_id = run_id

        df = result.to_dataframe()
        all_dfs.append(df)

        # Save per-symbol results
        sym_dir = out_base / f"walkforward_{run_id}" / symbol_pair.symbol_agent
        sym_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(sym_dir / "signals.csv", index=False)

        # Save metadata
        meta = {
            "run_id": run_id,
            "experiment_type": "agent_plus_model_walkforward",
            "symbol_agent": symbol_pair.symbol_agent,
            "symbol_deep_trading": symbol_pair.symbol_deep_trading,
            "test_start": wf_config.test_start.isoformat(),
            "test_end": wf_config.test_end.isoformat(),
            "walk_forward_retrain_days": wf_config.walk_forward_retrain_days,
            "num_windows": len(windows),
            "llm_provider": wf_config.llm_provider,
            "quick_think_llm": wf_config.quick_think_llm,
            "deep_think_llm": wf_config.deep_think_llm,
            "selected_analysts": wf_config.selected_analysts,
            "total_results": len(result.results),
            "errors": sum(1 for r in result.results if r.error),
        }
        with (sym_dir / "metadata.json").open("w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        # Print summary
        errors = df[df["error"] != ""]
        print()
        print(f"Symbol:  {symbol_pair.symbol_agent}")
        print(f"Windows: {len(df)} ({len(errors)} errors)")
        print(f"Output:  {sym_dir}")
        print()
        print(df[["window_idx", "window_start", "window_end", "decision_raw", "position", "latency_s"]].to_string(index=False))
        print()

    # Save combined results
    if len(all_dfs) > 1:
        combined = pd.concat(all_dfs, ignore_index=True)
        combined_dir = out_base / f"walkforward_{run_id}"
        combined.to_csv(combined_dir / "all_signals.csv", index=False)
        logging.info("Combined results saved to: %s", combined_dir / "all_signals.csv")

    print(f"\nRun ID: {run_id}")
    print(f"Output: {out_base / f'walkforward_{run_id}'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
