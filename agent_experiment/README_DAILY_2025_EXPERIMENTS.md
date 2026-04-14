# 2025 每日決策實驗（Pure vs Hybrid）

用**白話**說明這份設定在做什麼、要改哪裡、產物在哪裡。

## 你在做什麼

- 在 `pilot_windows` 涵蓋的區間內，依 **`date_stride`** 決定多久呼叫一次多 agent 管線，得到 **BUY / SELL / HOLD**（寫進 `signals.csv` 的 `position`：1 / -1 / 0）。
  - **`date_stride: 1`**：每個日曆日跑一次（預設）。
  - **`date_stride: 2`**：每隔一天跑一次；**沒有跑 LLM 的那幾天**在回測裡會 **沿用上一次決策**（`run_eval` 內 forward-fill；`run_compare_range` 的 baseline 也會用「首末訊號日之間的完整日曆區間」對齊）。
- 日期範圍：**2025-01-01 ～ 2025-12-31**（一整年；`date_stride: 1` 時約 **365 次** LLM，GPU 時間很長）。
- **Pure**：只有 market / news / fundamentals。  
- **Hybrid**：再多一個 **model** analyst（讀 deep-trading 的 `backtest.csv` 指標）。

兩條實驗其餘設定（模型名、debate 次數、retry 等）應保持一樣，只差有沒有 `model`，比較才公平。

## 檔案一覽

| 用途 | 路徑 |
|------|------|
| Pure 設定 | `agent_experiment/configs/pilot_daily_2025_pure.yaml` |
| Hybrid 設定 | `agent_experiment/configs/pilot_daily_2025_hybrid.yaml` |
| 分開跑的 SLURM | `agent_experiment/slurm/job_daily_2025_pure.sh`、`job_daily_2025_hybrid.sh` |
| 依 `signals.csv` 日期切 baseline 的比較 | `python -m agent_experiment.scripts.run_compare_range` |

程式上沿用 **`run_pilot`**：在每個 `pilot_windows` 裡，從 `start` 起每隔 **`date_stride`** 天跑一次 `propagate`（該視窗內第 0、stride、2×stride… 個日曆日）。

## 事前準備

1. **Conda 環境**已安裝本 repo（`pip install -e .`）與依賴。  
2. **Ollama** 與設定檔裡的模型（`qwen3:8b`、`qwen3:30b-a3b`）在計算節點可用。  
3. **deep-trading 產物**：Hybrid 需要 `agent_experiment/model_artifacts/<某個 run_id>/BTCUSDT/<strategy>/backtest.csv`。  
4. **`run_eval` 用的 K 線**：預設 `../deep-trading/data/BTCUSDT_1h.parquet`（相對於本 repo 根目錄；在 PSC 請改成你實際路徑）。

## 調整參數（最常改）

編輯對應的 **YAML**：

| 參數 | 說明 |
|------|------|
| `pilot_windows` | 改 `start` / `end` 可縮短區間（例如先跑一週做 smoke test）。 |
| `date_stride` | **≥1 的整數**。`1` = 每日決策；`2` = 兩天決策一次（中間日沿用上次部位，見上）。 |
| `selected_analysts` | Pure **不要** `model`；Hybrid **要** `model`。 |
| `symbol_agent` / `symbol_deep_trading` | 換幣種時兩邊一起改；`run_eval` 的 parquet 與 `run_compare_range` 的 `--symbol` 也要對應（例如 `ETHUSDT`）。 |
| `deep_trading_artifacts_dir` | 僅 Hybrid 需要；指向含多個 `run_id` 子目錄的 artifacts 根目錄。 |
| `artifacts_dir` | 本機預設輸出根目錄；也可用 CLI `--output-dir` 覆寫。 |

SLURM 腳本內請改：**`PROJECT_ROOT`、`YOUR_ID`、Ollama 路徑、`DEEP_RUN_ID`、`OHLCV_PARQUET`**。

## 本機（或互動節點）指令流程

在 **repo 根目錄**（含 `agent_experiment` 的那一層），並已 `conda activate`：

### 1) 跑實驗（擇一）

```bash
# Pure
python -m agent_experiment.scripts.run_pilot \
  --config agent_experiment/configs/pilot_daily_2025_pure.yaml \
  --output-dir outputs/daily_2025_pure \
  -v

# Hybrid（需先啟動 ollama serve）
python -m agent_experiment.scripts.run_pilot \
  --config agent_experiment/configs/pilot_daily_2025_hybrid.yaml \
  --output-dir outputs/daily_2025_hybrid \
  -v
```

每次 run 會新建 `outputs/.../<UTC_run_id>/`，底下有 **`signals.csv`**、**`metadata.json`**、**`summary.txt`**。

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

### 3) 與 deep-trading 各策略「同一批日期的 bar」並列

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

## PSC：兩個 job 並行

1. 編輯 `agent_experiment/slurm/job_daily_2025_pure.sh` 與 `job_daily_2025_hybrid.sh` 頂部變數。  
2. 上傳到叢集後：

```bash
chmod +x agent_experiment/slurm/job_daily_2025_pure.sh
chmod +x agent_experiment/slurm/job_daily_2025_hybrid.sh
sbatch agent_experiment/slurm/job_daily_2025_pure.sh
sbatch agent_experiment/slurm/job_daily_2025_hybrid.sh
```

兩支 job **互不依賴**，可同時排隊。

## 結果在哪裡、怎麼看

| 檔案 | 內容 |
|------|------|
| `signals.csv` | 每天一列：`date`、`position`、原始 `decision_raw`、錯誤欄位。 |
| `metadata.json` | `experiment_name`、`selected_analysts`、錯誤數量等。 |
| `summary_metrics.md` | 人讀的績效摘要（與 deep-trading 同一套指標定義）。 |
| `agent_metrics.json` | `aggregate` + `per_window`（全年只有 window 0 一個窗）。 |
| `comparison_agent_vs_forecast_by_signals.md` | 同一批日曆日的 agent vs 各 baseline 表。 |

**比 Pure vs Hybrid**：各開各自的 `summary_metrics.md` 或比對兩份 `agent_metrics.json` 的 `aggregate`（Sharpe、回撤、累積報酬等）。

## 時間與成本提醒

- **365 天 × 完整多 agent + 雙模型** ≈ 非常久；務必先**縮短 `pilot_windows`** 或 **`--dry-run`** 驗證。  
- 若只跑 Pure，通常仍要跑很久，只是少做 model 相關 tool。

## 程式上改了什麼（供維護）

- `ExperimentConfig` 增加 `deep_trading_artifacts_dir`、`experiment_name`；Hybrid **pilot** 會在 `run_pilot` 裡呼叫 `set_artifacts_dir` / `set_deep_trading_symbol`（與 walk-forward 一致）。  
- `compare.py` 新增 `run_compare_for_signal_dates`，供全年與任意日期區間使用。
