#!/usr/bin/env python3
"""After Pure / Hybrid runs are evaluated, build one Pure vs Hybrid vs Traditional table.

Requires ``agent_metrics.json`` in each LLM run directory (from ``run_eval``).
Traditional baselines are sliced from deep-trading ``backtest.csv`` files using the
same calendar span as the reference ``signals.csv`` (default: Pure run).

Writes ``comparison_pure_hybrid_traditional.md`` and ``.json`` under ``--output``
(or ``--pure-dir``).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

pkg_root = Path(__file__).resolve().parents[2]
if str(pkg_root) not in sys.path:
    sys.path.insert(0, str(pkg_root))

deep_root = pkg_root.parent.parent / "deep-trading"
if deep_root.exists() and str(deep_root) not in sys.path:
    sys.path.insert(0, str(deep_root))


def main() -> int:
    p = argparse.ArgumentParser(
        description="Combined Pure / Hybrid / Traditional comparison (post run_eval).",
    )
    p.add_argument(
        "--pure-dir",
        required=True,
        help="Directory with signals.csv + agent_metrics.json (Pure LLM run)",
    )
    p.add_argument(
        "--hybrid-metrics-dir",
        required=True,
        help="Hybrid run using get_model_metrics (historical stats)",
    )
    p.add_argument(
        "--hybrid-signals-dir",
        default=None,
        help="Optional Hybrid run using get_model_signals (directional tool)",
    )
    p.add_argument(
        "--deep-artifacts",
        default=str(pkg_root / "agent_experiment" / "model_artifacts"),
        help="Deep-trading artifacts root (contains <run_id>/SYMBOL/...)",
    )
    p.add_argument("--run-id", required=True, help="Artifact folder name under deep-artifacts")
    p.add_argument("--symbol", default="BTCUSDT", help="Symbol folder under run-id")
    p.add_argument(
        "--signals-reference-dir",
        default=None,
        help="Whose signals.csv defines the evaluation calendar (default: pure-dir)",
    )
    p.add_argument(
        "--output",
        default=None,
        help="Output directory (default: same as --pure-dir)",
    )
    args = p.parse_args()

    from agent_experiment.experiment.compare import run_pure_hybrid_traditional_comparison

    out = run_pure_hybrid_traditional_comparison(
        pure_dir=Path(args.pure_dir),
        hybrid_metrics_dir=Path(args.hybrid_metrics_dir),
        deep_artifacts_dir=Path(args.deep_artifacts),
        run_id=args.run_id,
        symbol=args.symbol,
        hybrid_signals_dir=Path(args.hybrid_signals_dir) if args.hybrid_signals_dir else None,
        output_path=Path(args.output) if args.output else None,
        signals_reference_dir=Path(args.signals_reference_dir)
        if args.signals_reference_dir
        else None,
    )
    print(f"Written: {out}")
    json_path = out.parent / "comparison_pure_hybrid_traditional.json"
    print(f"Written: {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
