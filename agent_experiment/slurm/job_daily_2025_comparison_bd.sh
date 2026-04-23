#!/bin/bash
#SBATCH --job-name=bd-compare-split
#SBATCH -p GPU-shared
#SBATCH --gres=gpu:v100-16:1
#SBATCH -t 01:00:00
#SBATCH -A cis260081p
#SBATCH --output=/ocean/projects/cis260081p/shared/logs/%x-%j.out
#
# Build final comparison table for bear_drawdown (base + split arms).

set -euo pipefail

PROJECT_ROOT="/ocean/projects/cis260081p/chsu11/hybrid/TradingAgents"
DEEP_ARTIFACTS="${PROJECT_ROOT}/agent_experiment/model_artifacts"
DEEP_RUN_ID="pilot_2025"
SYMBOL="BTCUSDT"

PURE_ROOT="${PROJECT_ROOT}/outputs/bear_drawdown_pure"
WINDOW="bear_drawdown"
WINDOW_SHORT="bd"
BASE_METRICS_ROOT="${PROJECT_ROOT}/outputs/bear_drawdown_hybrid"
BASE_SIGNALS_ROOT="${PROJECT_ROOT}/outputs/bear_drawdown_hybrid_signals"
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

resolve_optional_single_run_dir() {
  local root_dir="$1"
  if [[ ! -d "${root_dir}" ]]; then
    echo ""
    return 0
  fi
  mapfile -t dirs < <(find "${root_dir}" -mindepth 1 -maxdepth 1 -type d | sort)
  if [[ "${#dirs[@]}" -eq 0 ]]; then
    echo ""
    return 0
  fi
  if [[ "${#dirs[@]}" -gt 1 ]]; then
    echo "[WARN] Multiple run dirs under ${root_dir}; picking latest by name" >&2
    printf '%s\n' "${dirs[@]}" >&2 || true
  fi
  echo "${dirs[-1]}"
  return 0
}

module load anaconda3
conda activate dl_project
mkdir -p /ocean/projects/cis260081p/shared/logs

cd "${PROJECT_ROOT}"
mkdir -p "${OUTPUT_DIR}"
TMP_DIR="${OUTPUT_DIR}/tiers"
mkdir -p "${TMP_DIR}"

PURE_DIR="$(resolve_single_run_dir "${PURE_ROOT}")"
BASE_METRICS_DIR="$(resolve_optional_single_run_dir "${BASE_METRICS_ROOT}")"
BASE_SIGNALS_DIR="$(resolve_optional_single_run_dir "${BASE_SIGNALS_ROOT}")"

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

COLS = [
  "cumulative_return", "annualized_return", "sharpe", "sortino", "max_drawdown", "calmar",
  "excess_cumulative_return", "information_ratio", "hit_rate", "profit_factor"
]

def fmt(v):
    if v is None:
        return "-"
    if isinstance(v, (int, float)):
        return f"{v:.4f}"
    return str(v)

def add_row(rows, name, selected_models, agg):
    row = {"strategy": name, "selected models": selected_models}
    for c in COLS:
        row[c] = agg.get(c) if isinstance(agg, dict) else None
    rows.append(row)

out_dir = Path("${OUTPUT_DIR}")
tiers_root = Path("${TMP_DIR}")
pure_dir = Path("${PURE_DIR}")
base_metrics_dir = Path("${BASE_METRICS_DIR}") if "${BASE_METRICS_DIR}" else None
base_signals_dir = Path("${BASE_SIGNALS_DIR}") if "${BASE_SIGNALS_DIR}" else None
print(f"[INFO] BASE_METRICS_DIR={base_metrics_dir}")
print(f"[INFO] BASE_SIGNALS_DIR={base_signals_dir}")

tier_data = {}
for t in ["best2", "mid3", "worst2"]:
    j = tiers_root / t / "comparison_pure_hybrid_traditional.json"
    m = tiers_root / t / "selected_models.json"
    if not j.exists():
        continue
    data = json.loads(j.read_text(encoding="utf-8"))
    models = []
    if m.exists():
        models = json.loads(m.read_text(encoding="utf-8")).get("models", [])
    tier_data[t] = {"data": data, "models": models, "json_path": str(j)}

if not tier_data:
    raise SystemExit("No tier comparison JSON files found")

ref = tier_data["best2"]["data"] if "best2" in tier_data else next(iter(tier_data.values()))["data"]
rows = []

# Base rows: pure + original hybrid arms (if present)
pure_agg = ((ref.get("llm", {}) or {}).get("pure", {}) or {}).get("aggregate", {})
add_row(rows, "LLM Pure", "-", pure_agg)

def read_agent_agg(run_dir: Path):
    p = run_dir / "agent_metrics.json"
    if not p.exists():
        return None
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    if isinstance(payload, dict) and isinstance(payload.get("aggregate"), dict):
        return payload.get("aggregate")
    return payload if isinstance(payload, dict) else None

base_metrics_agg = read_agent_agg(base_metrics_dir) if base_metrics_dir else None
base_signals_agg = read_agent_agg(base_signals_dir) if base_signals_dir else None
if base_metrics_agg:
    add_row(rows, "LLM Hybrid (metrics)", "-", base_metrics_agg)
if base_signals_agg:
    add_row(rows, "LLM Hybrid (signals)", "-", base_signals_agg)

# Split rows
for t in ["best2", "mid3", "worst2"]:
    if t not in tier_data:
        continue
    d = tier_data[t]["data"]
    models = ", ".join(tier_data[t]["models"]) if tier_data[t]["models"] else "-"
    hm = ((d.get("llm", {}) or {}).get("hybrid_metrics", {}) or {}).get("aggregate", {})
    hs = ((d.get("llm", {}) or {}).get("hybrid_signals", {}) or {}).get("aggregate", {})
    add_row(rows, f"hybrid_metrics({t})", models, hm)
    add_row(rows, f"hybrid_signals({t})", models, hs)

# Traditional rows (same reference span)
trad = ref.get("traditional_forecast", {}) or {}
for strat in sorted(trad.keys()):
    add_row(rows, strat, "-", trad.get(strat, {}))

# Write final JSON
summary = {"window": "${WINDOW}", "rows": rows, "source": {k: v["json_path"] for k, v in tier_data.items()}}
(out_dir / "comparison_pure_hybrid_traditional_split.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

# Write final MD in requested format
span = ref.get("signal_calendar_span", {}) or {}
min_d = span.get("min", "?")
max_d = span.get("max", "?")
n_days = span.get("n_calendar_days", "?")

md = []
md.append("# Agent vs Forecasting Models - Same-Calendar Comparison")
md.append("")
md.append(f"**Evaluation period:** {n_days} calendar days (dense span from first to last signal date: {min_d} -> {max_d}), aligned with `run_eval` forward-fill.")
md.append("")
md.append("Forecast strategies are sliced to the **same hourly bars** on those dates; agent aggregate metrics come from `agent_metrics.json` (produced by `run_eval`).")
md.append("")
md.append("---")
md.append("")
md.append("## Aggregate comparison (agent vs baselines on signal dates)")
md.append("")
md.append("| strategy | selected models | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |")
md.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for r in rows:
    md.append(
      f"| {r['strategy']} | {r['selected models']} | {fmt(r['cumulative_return'])} | {fmt(r['annualized_return'])} | {fmt(r['sharpe'])} | {fmt(r['sortino'])} | {fmt(r['max_drawdown'])} | {fmt(r['calmar'])} | {fmt(r['excess_cumulative_return'])} | {fmt(r['information_ratio'])} | {fmt(r['hit_rate'])} | {fmt(r['profit_factor'])} |"
    )
md.append("")
md.append("---")
md.append("")
md.append("## Benchmark reference")
bh = trad.get("buy_and_hold", {})
md.append(f"- **Buy-and-hold (signal dates):** cumulative return = {fmt(bh.get('cumulative_return'))}")
md.append("")
md.append("## Source files")
for k in ["best2", "mid3", "worst2"]:
    if k in tier_data:
        md.append(f"- `{k}`: `{tier_data[k]['json_path']}`")

(out_dir / "comparison_pure_hybrid_traditional.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"[INFO] Wrote final table: {out_dir / 'comparison_pure_hybrid_traditional.md'}")
PY

echo "Done. Final report under: ${OUTPUT_DIR}/comparison_pure_hybrid_traditional.md"
