#!/bin/bash
#SBATCH --job-name=bb-pure
#SBATCH -p GPU-shared
#SBATCH --gres=gpu:v100-32:1
#SBATCH -t 48:00:00
#SBATCH -A cis260081p
#SBATCH --output=/ocean/projects/cis260081p/shared/logs/%x-%j.out
#
# Pure agent — bull_breakout window (2025-04-09 .. 2025-05-08).

set -euo pipefail

PROJECT_ROOT="/ocean/projects/cis260081p/chsu11/hybrid/TradingAgents"
CONFIG_TEMPLATE="agent_experiment/configs/pilot_bull_breakout_pure.yaml"
OHLCV_PARQUET="${PROJECT_ROOT}/../../deep-trading/data/BTCUSDT_1h.parquet"
DEEP_RUN_ID="pilot_2025"

module load anaconda3
conda activate dl_project
mkdir -p /ocean/projects/cis260081p/shared/logs

export PATH="/ocean/projects/cis260081p/chsu11/ollama-install/bin:$PATH"
export OLLAMA_MODELS="/ocean/projects/cis260081p/chsu11/ollama-models"

cd "${PROJECT_ROOT}"

mkdir -p "agent_experiment/configs/frozen"
JOB_TAG="${SLURM_JOB_ID:-local}"
FROZEN_CONFIG="agent_experiment/configs/frozen/job_${JOB_TAG}_pilot_bull_breakout_pure.yaml"
cp "${CONFIG_TEMPLATE}" "${FROZEN_CONFIG}"
export CONFIG_PATH="${FROZEN_CONFIG}"

ollama serve &
sleep 15
cleanup() { kill %1 2>/dev/null || true; }
trap cleanup EXIT

nvidia-smi || true

python -m agent_experiment.scripts.run_pilot \
  --config "${CONFIG_PATH}" \
  -v

OUT_ROOT="$(python - <<'PY'
import os
from agent_experiment.experiment.config import load_config
c = load_config(os.environ["CONFIG_PATH"])
print(c.artifacts_dir)
PY
)"
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
