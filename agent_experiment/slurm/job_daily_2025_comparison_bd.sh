#!/bin/bash
#SBATCH --job-name=bd-compare-split
#SBATCH -p GPU-shared
#SBATCH --gres=gpu:v100-16:1
#SBATCH -t 01:00:00
#SBATCH -A cis260081p
#SBATCH --output=/ocean/projects/cis260081p/shared/logs/%x-%j.out
#
# Build Pure vs Hybrid vs Traditional comparisons for bear_drawdown split arms.
# Write one consolidated summary table with selected model lists.

set -euo pipefail

PROJECT_ROOT="/ocean/projects/cis260081p/chsu11/hybrid/TradingAgents"
DEEP_ARTIFACTS="${PROJECT_ROOT}/agent_experiment/model_artifacts"
DEEP_RUN_ID="pilot_2025"
SYMBOL="BTCUSDT"

PURE_ROOT="${PROJECT_ROOT}/outputs/bear_drawdown_pure"
WINDOW="bear_drawdown"
WINDOW_SHORT="bd"
OUTPUT_DIR="${PROJECT_ROOT}/outputs/bear_drawdown_final_comparison"

resolve_single_run_dir() {
  local root_dir="$1"
  if [[ ! -d "${root_dir}" ]]; then
    echo "[FATAL] Missing directory: ${root_dir}" >&2
    return 1
  fi
  mapfile -t dirs < <(find "${root_dir}" -mindepth 1 -maxdepth 1 -type d | sort)
  if [[ "${#dirs[@]}" -ne 1 ]]; then
    echo "[FATAL] Expected exactly one run dir under ${root_dir}, found ${#dirs[@]}" >&2
    printf '%s\n' "${dirs[@]}" >&2 || true
    return 1
  fi
  echo "${dirs[0]}"
}

module load anaconda3
conda activate dl_project
mkdir -p /ocean/projects/cis260081p/shared/logs

cd "${PROJECT_ROOT}"
mkdir -p "${OUTPUT_DIR}"
TMP_DIR="${OUTPUT_DIR}/tiers"
mkdir -p "${TMP_DIR}"

PURE_DIR="$(resolve_single_run_dir "${PURE_ROOT}")"

for tier in best2 mid3 worst2; do
  HYBRID_METRICS_ROOT="${PROJECT_ROOT}/outputs/${WINDOW}_hybrid_metrics_${tier}"
  HYBRID_SIGNALS_ROOT="${PROJECT_ROOT}/outputs/${WINDOW}_hybrid_signals_${tier}"

  HYBRID_METRICS_DIR="$(resolve_single_run_dir "${HYBRID_METRICS_ROOT}")"
  HYBRID_SIGNALS_DIR="$(resolve_single_run_dir "${HYBRID_SIGNALS_ROOT}")"

  TIER_OUT="${TMP_DIR}/${tier}"
  mkdir -p "${TIER_OUT}"

  echo "[INFO] Running comparison for tier=${tier}"
  python -m agent_experiment.scripts.run_experiment_comparison \
    --pure-dir "${PURE_DIR}" \
    --hybrid-metrics-dir "${HYBRID_METRICS_DIR}" \
    --hybrid-signals-dir "${HYBRID_SIGNALS_DIR}" \
    --deep-artifacts "${DEEP_ARTIFACTS}" \
    --run-id "${DEEP_RUN_ID}" \
    --symbol "${SYMBOL}" \
    --output "${TIER_OUT}"

  python - <<PY
import json
from pathlib import Path
import yaml
tier = "${tier}"
window_short = "${WINDOW_SHORT}"
project_root = Path("${PROJECT_ROOT}")
cfg = project_root / "agent_experiment" / "configs" / window_short / f"pilot_{window_short}_hybrid_metrics_{tier}.yaml"
out = Path("${TIER_OUT}") / "selected_models.json"
with cfg.open("r", encoding="utf-8") as f:
    y = yaml.safe_load(f) or {}
models = y.get("model_strategies") or []
out.write_text(json.dumps({"tier": tier, "models": models}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[INFO] models[{tier}] = {models}")
PY

  echo "[INFO] Done tier=${tier} -> ${TIER_OUT}"
done

python - <<PY
import json
from pathlib import Path

out_dir = Path("${OUTPUT_DIR}")
tiers_root = Path("${TMP_DIR}")
tiers = ["best2", "mid3", "worst2"]
rows = []
for t in tiers:
    j = tiers_root / t / "comparison_pure_hybrid_traditional.json"
    m = tiers_root / t / "selected_models.json"
    if not j.exists() or not m.exists():
        continue
    data = json.loads(j.read_text(encoding="utf-8"))
    models = json.loads(m.read_text(encoding="utf-8")).get("models", [])
    llm = data.get("llm", {})
    hm = (llm.get("hybrid_metrics", {}) or {}).get("aggregate", {})
    hs = (llm.get("hybrid_signals", {}) or {}).get("aggregate", {})
    rows.append({
        "tier": t,
        "selected_models": models,
        "hybrid_metrics_cumret": hm.get("cumulative_return"),
        "hybrid_metrics_sharpe": hm.get("sharpe"),
        "hybrid_signals_cumret": hs.get("cumulative_return"),
        "hybrid_signals_sharpe": hs.get("sharpe"),
        "json_path": str(j),
    })

summary = {"window": "${WINDOW}", "rows": rows}
(out_dir / "comparison_split_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

md = []
md.append(f"# Split Comparison Summary ({summary['window']})")
md.append("")
md.append("| tier | selected_models | hybrid_metrics_cumret | hybrid_metrics_sharpe | hybrid_signals_cumret | hybrid_signals_sharpe |")
md.append("| --- | --- | ---: | ---: | ---: | ---: |")
for r in rows:
    models = ", ".join(r["selected_models"]) if r["selected_models"] else "-"
    md.append(f"| {r['tier']} | {models} | {r['hybrid_metrics_cumret']} | {r['hybrid_metrics_sharpe']} | {r['hybrid_signals_cumret']} | {r['hybrid_signals_sharpe']} |")
md.append("")
md.append("## Source files")
for r in rows:
    md.append(f"- `{r['tier']}`: `{r['json_path']}`")
(out_dir / "comparison_split_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"[INFO] Wrote summary: {out_dir / 'comparison_split_summary.md'}")
PY

echo "Done. Consolidated report under: ${OUTPUT_DIR}/comparison_split_summary.md"
