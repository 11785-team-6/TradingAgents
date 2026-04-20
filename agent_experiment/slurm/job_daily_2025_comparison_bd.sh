#!/bin/bash
#SBATCH --job-name=bd-compare
#SBATCH -p GPU-shared
#SBATCH --gres=gpu:v100-16:1
#SBATCH -t 01:00:00
#SBATCH -A cis260081p
#SBATCH --output=/ocean/projects/cis260081p/shared/logs/%x-%j.out
#
# Build final Pure / Hybrid / Traditional comparison table after run_eval is done.
# Edit paths and run IDs below for your PSC account.

set -euo pipefail

PROJECT_ROOT="/ocean/projects/cis260081p/chsu11/hybrid/TradingAgents"
PURE_DIR="${PROJECT_ROOT}/outputs/bear_drawdown_pure/20260418T121803Z"
HYBRID_METRICS_DIR="${PROJECT_ROOT}/outputs/bear_drawdown_hybrid/20260418T114623Z"
HYBRID_SIGNALS_DIR="${PROJECT_ROOT}/outputs/bear_drawdown_hybrid_signals/20260418T120224Z"
DEEP_ARTIFACTS="${PROJECT_ROOT}/agent_experiment/model_artifacts"
DEEP_RUN_ID="pilot_2025"
SYMBOL="BTCUSDT"

module load anaconda3
conda activate dl_project
mkdir -p /ocean/projects/cis260081p/shared/logs

cd "${PROJECT_ROOT}"

python -m agent_experiment.scripts.run_experiment_comparison \
  --pure-dir "${PURE_DIR}" \
  --hybrid-metrics-dir "${HYBRID_METRICS_DIR}" \
  --hybrid-signals-dir "${HYBRID_SIGNALS_DIR}" \
  --deep-artifacts "${DEEP_ARTIFACTS}" \
  --run-id "${DEEP_RUN_ID}" \
  --symbol "${SYMBOL}" \
  --output "${PROJECT_ROOT}/outputs/bear_drawdown_final_comparison"

echo "Done. Final report under: ${PROJECT_ROOT}/outputs/bear_drawdown_final_comparison"
