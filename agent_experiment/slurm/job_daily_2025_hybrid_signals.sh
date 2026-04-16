#!/bin/bash
#SBATCH --job-name=daily2025-hybrid-signals
#SBATCH -p GPU-shared
#SBATCH --gres=gpu:v100-32:1
#SBATCH -t 48:00:00
#SBATCH -A cis260081p
#SBATCH --output=/ocean/projects/cis260081p/shared/logs/%x-%j.out
#
# Hybrid (signals mode): one LLM decision per calendar day for 2025.
# Uses model_input_mode=signals (get_model_signals).
# Edit PROJECT_ROOT / DEEP_RUN_ID / paths below for your PSC account.

set -euo pipefail

PROJECT_ROOT="/ocean/projects/cis260081p/chsu11/hybrid/TradingAgents"
OUT_ROOT="${PROJECT_ROOT}/outputs/daily_2025_hybrid_signals"
OHLCV_PARQUET="${PROJECT_ROOT}/../../deep-trading/data/BTCUSDT_1h.parquet"
DEEP_RUN_ID="pilot_2025"

module load anaconda3
conda activate dl_project
mkdir -p /ocean/projects/cis260081p/shared/logs

export PATH="/ocean/projects/cis260081p/chsu11/ollama-install/bin:$PATH"
export OLLAMA_MODELS="/ocean/projects/cis260081p/chsu11/ollama-models"

cd "${PROJECT_ROOT}"

ollama serve &
sleep 15
cleanup() { kill %1 2>/dev/null || true; }
trap cleanup EXIT

nvidia-smi || true

python -m agent_experiment.scripts.run_pilot \
  --config agent_experiment/configs/pilot_daily_2025_hybrid_signals.yaml \
  --output-dir "${OUT_ROOT}" \
  -v

AGENT_DIR="$(find "${OUT_ROOT}" -mindepth 1 -maxdepth 1 -type d | sort | tail -n 1)"
echo "AGENT_DIR=${AGENT_DIR}"

python -m agent_experiment.scripts.run_eval \
  --signals "${AGENT_DIR}/signals.csv" \
  --data "${OHLCV_PARQUET}" \
  --output-dir "${AGENT_DIR}"

python -m agent_experiment.scripts.run_compare_range \
  --agent-dir "${AGENT_DIR}" \
  --deep-artifacts "${PROJECT_ROOT}/agent_experiment/model_artifacts" \
  --run-id "${DEEP_RUN_ID}" \
  --symbol BTCUSDT

echo "Done. Artifacts under: ${AGENT_DIR}"
