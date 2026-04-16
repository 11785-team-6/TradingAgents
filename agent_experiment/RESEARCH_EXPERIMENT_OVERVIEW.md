# TradingAgents Pure vs. Hybrid: Experiment Overview

**Document type:** internal research summary (for methodology alignment; not a submitted manuscript).  
**Repository:** `hybrid/TradingAgents` (`agent_experiment/`).

---

## 中文摘要

本專案比較 **Pure agent**（市場、新聞、基本面）與 **Hybrid**（再加上 **Model analyst**）。Hybrid 有兩種並存設定：**metrics** 模式讀取各策略之 **歷史績效摘要**（`get_model_metrics`）；**signals** 模式讀取各策略在決策時刻可知的 **部位／方向**（`get_model_signals`，無前瞻）。實驗以 **日曆區間** 與 **`date_stride`** 產生 `signals.csv`，以 **1h OHLCV** 與 deep-trading **同一套績效指標** 評估，並與 **Traditional**（非 LLM 之 forecasting baseline）於相同日曆跨度下並列；全部跑完後可用 **`run_experiment_comparison`** 產出 **Pure / Hybrid / Traditional** 單一對照表。本文檔整理定義、流程與產出，供報告與複現使用。

---

## 1. Motivation and Goals

### 1.1 Idea

Large language model (LLM) agents can synthesize qualitative and quantitative information for trading-style decisions. A **hybrid** design augments the agent team with information from the same **deep-trading** backtests used elsewhere in the project. Two hybrid variants are supported:

- **Metrics mode:** the Model analyst calls **`get_model_metrics`**, which summarizes **historical** performance (returns, Sharpe, drawdown, etc.) using rows **strictly before** the trade date.
- **Signals mode:** the Model analyst calls **`get_model_signals`**, which exposes each configured strategy’s **directional state** (mapped from the last available hourly **`position`** before the trade date — same cutoff semantics, no lookahead).

A **pure** agent baseline omits the Model analyst entirely. **Traditional** refers to non-LLM forecasting strategies evaluated on the same hourly slices (MACD, SMA cross, standalone LSTM, etc.), distinct from any LLM-augmented run.

### 1.2 Objectives

1. **Compare** tri-state decisions from **Pure** vs. **Hybrid (metrics)** vs. **Hybrid (signals)** where applicable, on the **same symbol** and aligned **calendar / stride** settings (LLM choice, debate rounds, retries, `date_stride`, etc.).
2. **Evaluate** each LLM arm with the **same metric code path** as deep-trading (`run_eval` → `deep_trading.metrics.performance`).
3. **Contrast** each LLM arm against **Traditional** forecasting baselines on the **same hourly bars** over the signal calendar span (`run_compare_range` / `run_compare_for_signal_dates`).
4. **Summarize** all arms in one place via **`run_experiment_comparison`** → `comparison_pure_hybrid_traditional.md` (and `.json`).

---

## 2. System Architecture

### 2.1 Orchestration

- **Framework:** LangGraph-style **TradingAgents** graph (`TradingAgentsGraph.propagate`).
- **Experiment driver:** `run_pilot` iterates each **scheduled decision date** within `pilot_windows`, calling `propagate(symbol_agent, trade_date)` once per date (subject to `date_stride`).

### 2.2 Analyst Teams (configuration-driven)

| Role | Typical inputs | Present in Pure? | Present in Hybrid? |
|------|----------------|------------------|---------------------|
| Market | Price / technical context (tooling as implemented) | Yes | Yes |
| News | News-related tooling | Yes | Yes |
| Fundamentals | Fundamentals tooling | Yes | Yes |
| **Model** | See §2.3–2.4 (`get_model_metrics` and/or `get_model_signals`) | **No** | **Yes** |

### 2.3 Hybrid — metrics tool (historical performance)

- **Tool:** `get_model_metrics(symbol, cutoff_date)`.
- **Data read:** `agent_experiment/model_artifacts/<run_id>/<SYMBOL>/<strategy>/backtest.csv`.
- **Which strategies:** YAML field **`model_strategies`** (optional list). If omitted, defaults align with the **full baseline set** used in `experiment/compare.py` (LSTM, XGBoost, ARIMA-GARCH, XGB-LSTM ensemble, MACD, SMA cross, buy-and-hold). Missing folders yield `not_found` for that strategy.
- **Leakage control:** metrics use rows with **timestamp strictly before** `cutoff_date` 00:00 UTC (same rule as `run_eval`’s informational cutoff for “past only”).

### 2.4 Hybrid — signals tool (directional state)

- **Tool:** `get_model_signals(symbol, as_of_date)`.
- **Data read:** same `backtest.csv` paths as §2.3.
- **Leakage control:** uses the **last hourly row** with **timestamp strictly before** `as_of_date` 00:00 UTC; maps column **`position`** to **BUY** / **SELL** / **HOLD** (near-zero positions count as HOLD). This is **not** a performance summary; it is the **mechanical position** each strategy would have been in at decision time, given only past bars.
- **Which strategies:** same **`model_strategies`** list as metrics mode (shared via `set_model_strategies` in the pilot runner).

### 2.5 Configuration: `model_input_mode`

- **`metrics`** (default): Model analyst only has `get_model_metrics` (legacy hybrid behavior for ongoing runs).
- **`signals`:** Model analyst only has `get_model_signals`. Use a separate YAML / output directory (e.g. `pilot_daily_2025_hybrid_signals.yaml`) so experiments do not overwrite each other.

### 2.6 Baselines — Traditional (non-LLM)

Defined in **deep-trading** backtests: e.g. buy-and-hold, MACD, SMA cross, LSTM, XGBoost, XGB-LSTM ensemble, ARIMA-GARCH, etc. Their **hourly** `backtest.csv` series are sliced to the evaluation calendar span for side-by-side tables.

---

## 3. Data Sources

| Data | Role | Notes |
|------|------|--------|
| **OHLCV parquet** (e.g. `BTCUSDT_1h.parquet`) | Converts daily decisions into **hourly** positions and returns in `run_eval` | Path must match `symbol_deep_trading`; must cover the calendar span implied by `signals.csv`. |
| **`model_artifacts/.../backtest.csv`** | Hybrid **Model analyst** inputs; **baseline** metrics in `run_compare_range` | `run_id` subfolder must exist on the machine running the job. |
| **News / market / fundamentals** | Retrieved via TradingAgents tools during `propagate` | Depends on live tool configuration (APIs, caches, rate limits). |
| **LLM weights** | Ollama (or configured provider) | GPU jobs typically start `ollama serve` before `run_pilot`. |

---

## 4. Time Horizon and Scheduling

### 4.1 Calendar windows

- **Primary control:** `pilot_windows` in YAML (`start`, `end`). All dates in the union of windows are candidates; within each window, dates are sampled with **`date_stride`**:
  - `date_stride: 1` → every calendar day in the window.
  - `date_stride: N>1` → every *N*th day from window start (0, N, 2N, …).

### 4.2 Metadata fields `test_pool_start` / `test_pool_end`

Documentary bounds stored in `metadata.json`; **execution** follows `pilot_windows`. Keep them **consistent** with the actual pilot span to avoid confusion in reports.

### 4.3 Example (group-internal)

A **January 2025** pilot uses `2025-01-01`–`2025-01-31` (31 decision days when `date_stride: 1`). A full-year design uses `2025-01-01`–`2025-12-31` (much higher LLM cost).

---

## 5. Experimental Protocol (End-to-End)

### Phase A — Configuration

- Edit `pilot_daily_2025_pure.yaml` vs. `pilot_daily_2025_hybrid.yaml` / `pilot_daily_2025_hybrid_signals.yaml` (or copies): differ in **`selected_analysts`** (`model` on/off), Hybrid’s **`deep_trading_artifacts_dir`**, and **`model_input_mode`** (`metrics` vs `signals`).
- Optionally set **`model_strategies`** to query a subset of artifact folders; default matches the full baseline list (see §2.3).
- Align **symbol**, **`date_stride`**, LLM names, debate rounds, retries across arms for a fair comparison.

### Phase B — Agent run (`run_pilot`)

**Inputs:** YAML + Ollama (non–dry-run).  
**Outputs (per run directory):** `signals.csv`, `metadata.json`, `summary.txt`.

### Phase C — Performance evaluation (`run_eval`)

**Inputs:** `signals.csv` + OHLCV parquet.  
**Mechanics:** Positions are mapped to hourly bars; **forward-fill** applies between sparse decision dates so intermediate calendar days carry the last decision until the next one.  
**Outputs:** `agent_metrics.json`, `agent_metrics.csv`, `agent_backtest.csv`, `summary_metrics.md`.

### Phase D — Baseline comparison (`run_compare_range`)

**Inputs:** `agent_metrics.json`, `signals.csv`, `model_artifacts/<run_id>/...` backtests.  
**Mechanics:** Build the **dense calendar span** from first to last signal date; slice each baseline’s hourly `backtest.csv` to those dates; compare aggregate metrics to the agent row from `agent_metrics.json`.  
**Outputs:** `comparison_agent_vs_forecast_by_signals.md`, `comparison_agent_vs_forecast_by_signals.json`.

### Phase E — Three-way LLM vs Traditional table (`run_experiment_comparison`)

**When:** After **Pure**, **Hybrid (metrics)**, and optionally **Hybrid (signals)** have each completed Phases B–C (and Phase D per run if desired).  
**Inputs:** directories containing `agent_metrics.json` for each LLM arm; `--deep-artifacts` and `--run-id` for Traditional baselines; reference `signals.csv` (default: Pure run) defines the evaluation calendar.  
**Outputs:** `comparison_pure_hybrid_traditional.md`, `comparison_pure_hybrid_traditional.json` — one Markdown table for **LLM Pure / Hybrid (metrics) / Hybrid (signals)** and a second table for **Traditional** strategies on the same dates.

### Phase F — HPC (optional)

SLURM templates `slurm/job_daily_2025_pure.sh` and `job_daily_2025_hybrid.sh` run Phases B–D sequentially per variant; additional Hybrid (signals) jobs can be added analogously. After all complete, run Phase E locally or add a final aggregation step.

---

## 6. Metrics and Diagnostics

### 6.1 Headline metrics (in `summary_metrics.md` and comparison tables)

Examples: cumulative return, annualized return, volatility, Sharpe, Sortino, max drawdown, Calmar, excess vs. benchmark, information ratio, hit rate, turnover, profit factor—computed by **deep-trading**’s `compute_performance_metrics`.

### 6.2 Regime split (`high_vol` / `low_vol`)

**Not** a separate experiment arm. Hourly bars are partitioned by **`realized_vol_24`** relative to the sample **quantile** (default 0.7): “high” vs. “low” volatility subsets, each with its own metric block—useful to see whether returns concentrate in calm vs. turbulent hours.

### 6.3 Benchmark row

**`buy_and_hold`** in comparison tables is the reference for **excess** metrics; it is **not** identical to the LLM agent’s strategy.

---

## 7. Expected Artifacts (successful full pipeline)

Per run directory (`<artifacts_root>/<UTC_run_id>/`), **nine** files after Phases B–D:

1. `signals.csv`  
2. `metadata.json`  
3. `summary.txt`  
4. `agent_metrics.json`  
5. `agent_metrics.csv`  
6. `agent_backtest.csv`  
7. `summary_metrics.md`  
8. `comparison_agent_vs_forecast_by_signals.md`  
9. `comparison_agent_vs_forecast_by_signals.json`  

Pure and Hybrid runs each produce their **own** nine-file bundle under their respective output roots.

---

## 8. Fairness Checklist (internal QA)

- [ ] Same `pilot_windows` and `date_stride` for Pure and Hybrid.  
- [ ] Same `symbol_agent` / `symbol_deep_trading` and matching **OHLCV** parquet.  
- [ ] Same LLM provider and model names, debate limits, `max_retries`.  
- [ ] Hybrid has valid **`deep_trading_artifacts_dir`** and correct **`run_id`** for `run_compare_range`.  
- [ ] Logs do **not** show persistent `get_model_metrics` / `get_model_signals` `not_found` for configured strategies.  
- [ ] **`model_input_mode`** and YAML **`model_strategies`** match the intended research arm (metrics vs signals; full vs subset).  
- [ ] `run_eval` uses a parquet path that **exists** on the cluster (common failure mode).

---

## 9. Limitations (explicit)

1. **Sample length:** Short windows (e.g. one month) support only **local** conclusions.  
2. **LLM stochasticity:** Re-runs may differ unless sampling is controlled.  
3. **Backtest vs. live:** Slippage, fees, liquidity, and execution latency are only partially modeled (see `run_eval` fee/slippage flags).  
4. **Information set:** Hybrid strictly has **more** information than Pure (either summarized **past** performance in metrics mode, or **current mechanical positions** in signals mode). State which variant was used when interpreting results.  
5. **Additional logs:** TradingAgents may emit other files (e.g. under `eval_results/`) depending on graph settings; they are **not** part of the nine-file contract above.

---

## 10. Reference Documentation in Repo

| Topic | Path |
|-------|------|
| Daily / stride / PSC commands | `agent_experiment/README_DAILY_2025_EXPERIMENTS.md` |
| Pure / Hybrid YAML templates | `agent_experiment/configs/pilot_daily_2025_pure.yaml`, `pilot_daily_2025_hybrid.yaml`, `pilot_daily_2025_hybrid_signals.yaml` |
| Three-way comparison script | `agent_experiment/scripts/run_experiment_comparison.py` |
| SLURM examples | `agent_experiment/slurm/job_daily_2025_pure.sh`, `job_daily_2025_hybrid.sh` |

---

## Revision log

| Item | Note |
|------|------|
| Created | Consolidates current `agent_experiment` behavior as understood from code and internal docs. |
| Updated | Hybrid **metrics** vs **signals**; YAML **`model_strategies`**; Phase E **Pure / Hybrid / Traditional** comparison artifacts. |

*If any item above disagrees with your deployed branch, update this file or the code—this document is meant as a single source of truth for “what we claim we did.”*
