# 2025 每日決策實驗（Pure vs Hybrid vs Traditional）

用**白話**說明這份設定在做什麼、要改哪裡、產物在哪裡。

## 你在做什麼

- 在 `pilot_windows` 涵蓋的區間內，依 **`date_stride`** 決定多久呼叫一次多 agent 管線，得到 **BUY / SELL / HOLD**（寫進 `signals.csv` 的 `position`：1 / -1 / 0）。
  - **`date_stride: 1`**：每個日曆日跑一次（預設）。
  - **`date_stride: 2`**：每隔一天跑一次；**沒有跑 LLM 的那幾天**在回測裡會 **沿用上一次決策**（`run_eval` 內 forward-fill；`run_compare_range` 的 baseline 也會用「首末訊號日之間的完整日曆區間」對齊）。
- 日期範圍：**2025-01-01 ～ 2025-12-31**（一整年；`date_stride: 1` 時約 **365 次** LLM，GPU 時間很長）。
- **Pure**：只有 market / news / fundamentals。  
- **Hybrid（metrics）**：再多一個 **model** analyst，呼叫 **`get_model_metrics`**（讀各策略 **過去績效摘要**，無前瞻）。  
- **Hybrid（signals）**：同樣有 model analyst，但呼叫 **`get_model_signals`**（讀各策略在決策前 **最後一根 K 的 position → BUY/SELL/HOLD**，無前瞻）。  
- **Traditional**：**不是**另一次 LLM 實驗，而是 deep-trading 裡 **非 agent** 的 forecasting baseline（MACD、SMA、LSTM 等），在 `run_compare_range` 或最後 **`run_experiment_comparison`** 裡與 LLM 並列。

公平比較時：Pure / Hybrid(metrics) / Hybrid(signals) 應保持 **同一** `pilot_windows`、`date_stride`、LLM 名稱、debate、retry 等，只差 **`model_input_mode`** 與是否啟用 `model`。

## 檔案一覽（要改哪裡）

| 用途 | 路徑 |
|------|------|
| Pure 設定 | `agent_experiment/configs/pilot_daily_2025_pure.yaml` |
| Hybrid（績效摘要） | `agent_experiment/configs/pilot_daily_2025_hybrid.yaml` |
| Hybrid（方向訊號） | `agent_experiment/configs/pilot_daily_2025_hybrid_signals.yaml` |
| 叢集排程（Pure） | `agent_experiment/slurm/job_daily_2025_pure.sh` |
| 叢集排程（Hybrid metrics） | `agent_experiment/slurm/job_daily_2025_hybrid.sh` |
| 依 `signals.csv` 切 baseline | `python -m agent_experiment.scripts.run_compare_range` |
| **全部跑完後** Pure / Hybrid / Traditional 一張總表 | `python -m agent_experiment.scripts.run_experiment_comparison` |

程式上與行為相關的實作（一般**不必**改，除非你要改預設策略清單或工具邏輯）：

| 說明 | 路徑 |
|------|------|
| Pilot 設定型別與載入 YAML | `agent_experiment/experiment/config.py` |
| 跑前設定 artifacts / 策略清單 | `agent_experiment/experiment/runner.py`（呼叫 `set_artifacts_dir`、`set_model_strategies` 等） |
| `metrics` / `signals` 工具 | `tradingagents/agents/utils/model_metrics_tool.py`、`model_signals_tool.py` |
| Graph 綁哪個工具 | `tradingagents/graph/trading_graph.py`（`config["model_input_mode"]`） |
| 方法論長文 | `agent_experiment/RESEARCH_EXPERIMENT_OVERVIEW.md` |

程式上沿用 **`run_pilot`**：在每個 `pilot_windows` 裡，從 `start` 起每隔 **`date_stride`** 天跑一次 `propagate`（該視窗內第 0、stride、2×stride… 個日曆日）。

## 參數一覽（整合表）

編輯對應 **YAML**（本機或複製後給 SLURM 的 `--config`）：

| 參數 | 說明 |
|------|------|
| `pilot_windows` | 改 `start` / `end` 可縮短區間（例如先跑一週做 smoke test）。 |
| `date_stride` | **≥1 的整數**。`1` = 每日決策；`2` = 兩天決策一次（中間日沿用上次部位，見上）。 |
| `selected_analysts` | Pure **不要** `model`；兩種 Hybrid **要**含 `model`。 |
| `symbol_agent` / `symbol_deep_trading` | 換幣種時兩邊一起改；`run_eval` 的 parquet 與 `run_compare_range` 的 `--symbol` 也要對應（例如 `ETHUSDT`）。 |
| `deep_trading_artifacts_dir` | 僅 Hybrid 需要；指向含多個 `run_id` 子目錄的 artifacts **根**目錄。 |
| **`model_input_mode`** | **`metrics`**（預設）：Model analyst 用 `get_model_metrics`。**`signals`**：用 `get_model_signals`。Pure 可省略或任意，因沒有 model analyst。 |
| **`model_strategies`** | **選填**，字串列表；指定要查哪些子資料夾（如 `lstm`、`xgboost`）。**不寫**則使用程式內預設「與 `compare.py` 一致的完整 baseline 清單」。 |
| `artifacts_dir` | 本機預設輸出根目錄；也可用 CLI `--output-dir` 覆寫。 |
| `experiment_name` | 寫進 `metadata.json`，方便辨識；總表也會拿來當列標籤。 |

**SLURM 腳本內**請改（與 YAML 對齊）：**`PROJECT_ROOT`、`YOUR_ID`、Ollama 路徑、`DEEP_RUN_ID`、`OHLCV_PARQUET`、`OUT_ROOT`**；若新增第三種 Hybrid，請改 **`--config`** 與 **`OUT_ROOT`**，避免覆蓋別次實驗輸出。

## 事前準備

1. **Conda 環境**已安裝本 repo（`pip install -e .`）與依賴。  
2. **Ollama** 與設定檔裡的模型（`qwen3:8b`、`qwen3:30b-a3b`）在計算節點可用。  
3. **deep-trading 產物**：Hybrid 需要 `agent_experiment/model_artifacts/<某個 run_id>/BTCUSDT/<strategy>/backtest.csv`（各策略資料夾依 `model_strategies` 或預設清單）。  
4. **`run_eval` 用的 K 線**：預設 `../deep-trading/data/BTCUSDT_1h.parquet`（相對於本 repo 根目錄；在 PSC 請改成你實際路徑）。

## 本機（或互動節點）指令流程

在 **repo 根目錄**（含 `agent_experiment` 的那一層），並已 `conda activate`：

### 1) 跑實驗（擇一或多條）

```bash
# Pure
python -m agent_experiment.scripts.run_pilot \
  --config agent_experiment/configs/pilot_daily_2025_pure.yaml \
  --output-dir outputs/daily_2025_pure \
  -v

# Hybrid（metrics：歷史績效摘要）
python -m agent_experiment.scripts.run_pilot \
  --config agent_experiment/configs/pilot_daily_2025_hybrid.yaml \
  --output-dir outputs/daily_2025_hybrid \
  -v

# Hybrid（signals：各模型當下方向）
python -m agent_experiment.scripts.run_pilot \
  --config agent_experiment/configs/pilot_daily_2025_hybrid_signals.yaml \
  --output-dir outputs/daily_2025_hybrid_signals \
  -v
```

每次 run 會新建 `outputs/.../<UTC_run_id>/`，底下有 **`signals.csv`**、**`metadata.json`**（含 `model_input_mode`、`model_strategies`）、**`summary.txt`**。

快速驗證管線（不呼叫真 LLM）：

```bash
python -m agent_experiment.scripts.run_pilot \
  --config agent_experiment/configs/pilot_daily_2025_pure.yaml \
  --dry-run
```

### 2) 產生效能 JSON / CSV / Markdown

對**該次 run 的目錄**（內含 `signals.csv`）：

```bash
AGENT_DIR="outputs/daily_2025_pure/20260409T120000Z"   # 改成你的 run 資料夾
OHLCV="/path/to/deep-trading/data/BTCUSDT_1h.parquet"

python -m agent_experiment.scripts.run_eval \
  --signals "${AGENT_DIR}/signals.csv" \
  --data "${OHLCV}" \
  --output-dir "${AGENT_DIR}"
```

會多：`agent_metrics.json`、`agent_metrics.csv`、`agent_backtest.csv`、`summary_metrics.md`。

### 3) 與 deep-trading 各策略「同一批日期的 bar」並列（單次 LLM run）

**必須先做第 2 步**（要有 `agent_metrics.json`）。`<RUN_ID>` 是 `model_artifacts` 下面的資料夾名稱。

```bash
python -m agent_experiment.scripts.run_compare_range \
  --agent-dir "${AGENT_DIR}" \
  --deep-artifacts agent_experiment/model_artifacts \
  --run-id "<RUN_ID>" \
  --symbol BTCUSDT
```

會多：`comparison_agent_vs_forecast_by_signals.md`、`comparison_agent_vs_forecast_by_signals.json`。

> **舊指令 `run_compare`（無 `_range`）**：仍只適用原本「三段固定 pilot 窗」的 60 天設定；**全年每日實驗請用 `run_compare_range`**。

### 4) 全部實驗跑完後：Pure / Hybrid / Traditional 總表（選用）

在 **Pure、Hybrid(metrics)、（可選）Hybrid(signals)** 都完成 **第 2 步** 之後，且你知道各次 run 的**輸出目錄**：

```bash
python -m agent_experiment.scripts.run_experiment_comparison \
  --pure-dir "outputs/daily_2025_pure/<PURE_RUN_ID>" \
  --hybrid-metrics-dir "outputs/daily_2025_hybrid/<HYBRID_METRICS_RUN_ID>" \
  --hybrid-signals-dir "outputs/daily_2025_hybrid_signals/<HYBRID_SIGNALS_RUN_ID>" \
  --deep-artifacts agent_experiment/model_artifacts \
  --run-id "<RUN_ID>" \
  --symbol BTCUSDT
```

- 若**沒跑** Hybrid(signals)，可**省略** `--hybrid-signals-dir`。  
- 預設用 **Pure** 目錄裡的 `signals.csv` 定義「評估用日曆區間」；若要改用別條 arm，加 **`--signals-reference-dir`**。  
- 產出：`comparison_pure_hybrid_traditional.md`、`comparison_pure_hybrid_traditional.json`（寫在 `--output` 若指定，否則在 `--pure-dir`）。

## PSC：SLURM 要跑幾支？

目前 repo 內建 **兩支**：

| 腳本 | 內容 |
|------|------|
| `job_daily_2025_pure.sh` | Pure：`run_pilot` → `run_eval` → `run_compare_range` |
| `job_daily_2025_hybrid.sh` | Hybrid **metrics**（`pilot_daily_2025_hybrid.yaml`）：同上 |
| `job_daily_2025_hybrid_signals.sh` | Hybrid **signals**（`pilot_daily_2025_hybrid_signals.yaml`）：同上 |
| `job_daily_2025_comparison.sh` | 最後總表：`run_experiment_comparison` |

- 兩支 job **互不依賴**，可 **`sbatch` 並行**。  
- 建議流程：先跑 `pure`、`hybrid`、`hybrid_signals` 三支；都完成後再跑 `comparison`。
- `job_daily_2025_comparison.sh` 需要你先填入 `<PURE_RUN_ID>` / `<HYBRID_METRICS_RUN_ID>` / `<HYBRID_SIGNALS_RUN_ID>`。

範例：

```bash
chmod +x agent_experiment/slurm/job_daily_2025_pure.sh
chmod +x agent_experiment/slurm/job_daily_2025_hybrid.sh
chmod +x agent_experiment/slurm/job_daily_2025_hybrid_signals.sh
chmod +x agent_experiment/slurm/job_daily_2025_comparison.sh
sbatch agent_experiment/slurm/job_daily_2025_pure.sh
sbatch agent_experiment/slurm/job_daily_2025_hybrid.sh
sbatch agent_experiment/slurm/job_daily_2025_hybrid_signals.sh
# 等前三支完成，且你把 comparison.sh 的 <...RUN_ID> 改成實際資料夾名
sbatch agent_experiment/slurm/job_daily_2025_comparison.sh
```

## 結果在哪裡、怎麼看

| 檔案 | 內容 |
|------|------|
| `signals.csv` | 每天一列：`date`、`position`、原始 `decision_raw`、錯誤欄位。 |
| `metadata.json` | `experiment_name`、`selected_analysts`、**`model_input_mode`**、**`model_strategies`**、錯誤數量等。 |
| `summary_metrics.md` | 人讀的績效摘要（與 deep-trading 同一套指標定義）。 |
| `agent_metrics.json` | `aggregate` + `per_window`（全年只有 window 0 一個窗）。 |
| `comparison_agent_vs_forecast_by_signals.md` | **該次** LLM run vs 各 baseline（單臂表）。 |
| `comparison_pure_hybrid_traditional.md` | **多臂** LLM vs Traditional 總表（需第 4 步）。 |

**比 Pure vs Hybrid**：可各開 `summary_metrics.md`，或用 **`run_experiment_comparison`** 一次對齊。

## 時間與成本提醒

- **365 天 × 完整多 agent + 雙模型** ≈ 非常久；務必先**縮短 `pilot_windows`** 或 **`--dry-run`** 驗證。  
- 若只跑 Pure，通常仍要跑很久，只是少做 model 相關 tool。  
- 多跑一條 Hybrid(signals) ≈ 與 Hybrid(metrics) **同量級** LLM 成本（多一次全年 pilot）。

## 程式上改了什麼（供維護）

- `ExperimentConfig`：`deep_trading_artifacts_dir`、`experiment_name`、**`model_input_mode`**、**`model_strategies`**、`date_stride`；Hybrid pilot 會設定 artifacts、symbol override、**`set_model_strategies`**。  
- `compare.py`：`run_compare_for_signal_dates`、`run_pure_hybrid_traditional_comparison`。  
- Model analyst：`get_model_metrics` / `get_model_signals` 二擇一（由 `model_input_mode` 決定）。
