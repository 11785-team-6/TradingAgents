#!/bin/bash
#SBATCH --job-name=bb-hybrid
#SBATCH -p GPU-shared
#SBATCH --gres=gpu:v100-32:1
#SBATCH -t 48:00:00
#SBATCH -A cis260081p
#SBATCH --output=/ocean/projects/cis260081p/shared/logs/%x-%j.out
#
# Hybrid (metrics) — bull_breakout window.

set -euo pipefail

PROJECT_ROOT="/ocean/projects/cis260081p/chsu11/hybrid/TradingAgents"
CONFIG_PATH="agent_experiment/configs/pilot_bull_breakout_hybrid.yaml"
export CONFIG_PATH
OLLAMA_PORT=11441
BACKEND_URL="http://127.0.0.1:${OLLAMA_PORT}/v1"
OHLCV_PARQUET="${PROJECT_ROOT}/../../deep-trading/data/BTCUSDT_1h.parquet"
DEEP_RUN_ID="pilot_2025"

module load anaconda3
conda activate dl_project
mkdir -p /ocean/projects/cis260081p/shared/logs

export PATH="/ocean/projects/cis260081p/chsu11/ollama-install/bin:$PATH"
export OLLAMA_MODELS="/ocean/projects/cis260081p/chsu11/ollama-models"

cd "${PROJECT_ROOT}"

source "agent_experiment/slurm/lib/ollama_bootstrap.sh"
start_ollama_or_die "127.0.0.1:${OLLAMA_PORT}" "ollama-${OLLAMA_PORT}.log" 45
trap stop_ollama_if_started EXIT

nvidia-smi || true

RUNTIME_CONFIG="${SLURM_TMPDIR:-/tmp}/$(basename "${CONFIG_PATH%.yaml}")_${SLURM_JOB_ID:-local}.yaml"
create_runtime_config_with_backend "${CONFIG_PATH}" "${BACKEND_URL}" "${RUNTIME_CONFIG}"
export CONFIG_PATH="${RUNTIME_CONFIG}"

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
