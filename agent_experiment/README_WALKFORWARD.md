# Agent + Model Walk-Forward Experiment

This experiment integrates the **TradingAgents** multi-agent framework with **deep-trading** ML model metrics to evaluate whether LLM agents can make better trading decisions when informed by quantitative model performance data.

## Experiment Design

### Three-Way Comparison

| Experiment | Description | Status |
|---|---|---|
| Pure Model | LSTM, XGBoost, ARIMA, Ensemble predictions via deep-trading backtest | Done |
| Pure Agent | TradingAgents multi-agent decisions without model input | Done |
| **Agent + Model** | Agents receive all four model metrics as input, then decide | **This experiment** |

### How It Works

1. **deep-trading** runs a walk-forward backtest (45-day retrain windows, test period 2023–2025) and produces `backtest.csv` for each model (LSTM, XGBoost, ARIMA, Ensemble).
2. At the start of each 45-day window, a new **Model Analyst** agent reads the four models' historical metrics (cumulative return, Sharpe, max drawdown, hit rate, etc.) computed from data **strictly before** the current window — no data leakage.
3. The Model Analyst report joins the existing analyst reports (Market, News, Fundamentals) and flows through the standard TradingAgents pipeline: Bull/Bear Debate → Trader → Risk Debate → Final Decision.
4. The agent outputs one **BUY / SELL / HOLD** decision per 45-day window.
5. Results are saved as `signals.csv` for comparison against pure-model and pure-agent baselines.

### Anti–Data Leakage Measures

- Model metrics are computed only from bars **before** the window start date.
- All agent prompts include a strict constraint: *"You must ONLY base your analysis on data returned by your tools. Do NOT use any knowledge from your training data about market prices, historical events, or asset performance."*
- The Model Analyst tool enforces the cutoff at the code level — future data is never exposed.

## Prerequisites

1. **deep-trading backtest results** are already bundled in this repo at `agent_experiment/model_artifacts/`:

```
agent_experiment/model_artifacts/full_universe_2015_2025_20260309/
├── BTCUSDT/
│   ├── lstm/backtest.csv
│   ├── xgboost/backtest.csv
│   ├── arima_garch/backtest.csv
│   └── xgb_lstm_ensemble/backtest.csv
└── ETHUSDT/
    ├── lstm/backtest.csv
    ├── xgboost/backtest.csv
    ├── arima_garch/backtest.csv
    └── xgb_lstm_ensemble/backtest.csv
```

If you need to regenerate them from deep-trading:

```bash
cd deep-trading
python -m deep_trading.cli compare-universe --config configs/default.yaml
# Then copy artifacts into TradingAgents:
cp -r artifacts/<run_id> ../TradingAgents/agent_experiment/model_artifacts/
```

2. **TradingAgents** installed:

```bash
cd TradingAgents
pip install -e .
```

3. **LLM backend** running. Default config uses Ollama:

```bash
ollama pull qwen3:8b
ollama pull qwen3:30b-a3b
ollama serve
```

## Configuration

Edit `agent_experiment/configs/walkforward.yaml`:

```yaml
# Symbols (must match deep-trading config)
symbols:
  - symbol_agent: "BTC-USD"        # yfinance ticker for agent tools
    symbol_deep_trading: "BTC/USDT" # deep-trading symbol name
  - symbol_agent: "ETH-USD"
    symbol_deep_trading: "ETH/USDT"

# Walk-forward settings (must match deep-trading default.yaml)
test_start: "2023-01-01"
test_end: "2025-12-31"
walk_forward_retrain_days: 45

# Path to model artifacts (bundled in this repo)
deep_trading_artifacts_dir: "agent_experiment/model_artifacts"

# LLM provider
llm_provider: "ollama"
quick_think_llm: "qwen3:8b"
deep_think_llm: "qwen3:30b-a3b"
backend_url: "http://localhost:11434/v1"

# Analysts (include "model" to enable the Model Analyst)
selected_analysts:
  - market
  - news
  - fundamentals
  - model
```

### Using a Different LLM Provider

**OpenAI:**
```yaml
llm_provider: "openai"
quick_think_llm: "gpt-4o-mini"
deep_think_llm: "gpt-4o"
```
Set `OPENAI_API_KEY` in your environment.

**Anthropic:**
```yaml
llm_provider: "anthropic"
quick_think_llm: "claude-sonnet-4-6"
deep_think_llm: "claude-sonnet-4-6"
```
Set `ANTHROPIC_API_KEY` in your environment.

**LlamaCpp (local GPU):**
```yaml
llm_provider: "llamacpp"
local_model_path_deep: "/path/to/large-model.gguf"
local_model_path_quick: "/path/to/small-model.gguf"
local_n_gpu_layers: -1
local_n_ctx: 4096
```

## Usage

All commands run from the `TradingAgents/` directory.

### Dry Run (validate pipeline, no GPU needed)

```bash
python -m agent_experiment.scripts.run_walkforward --dry-run
```

Uses a mock LLM to verify the full pipeline works end-to-end in ~30 seconds.

### Full Run

```bash
# Both symbols (BTC + ETH)
python -m agent_experiment.scripts.run_walkforward

# Single symbol
python -m agent_experiment.scripts.run_walkforward --symbol BTC-USD

# Custom config file
python -m agent_experiment.scripts.run_walkforward --config path/to/config.yaml

# Custom output directory
python -m agent_experiment.scripts.run_walkforward --output-dir /data/results

# Verbose logging
python -m agent_experiment.scripts.run_walkforward -v
```

### On a Compute Cluster (SLURM example)

```bash
#!/bin/bash
#SBATCH --job-name=agent-model-wf
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=48:00:00
#SBATCH --output=logs/walkforward_%j.log

module load python/3.11 cuda

cd /path/to/TradingAgents

# Start Ollama in background (if using Ollama)
ollama serve &
sleep 5

# Run experiment
python -m agent_experiment.scripts.run_walkforward --verbose 2>&1 | tee logs/run.log
```

## Output

```
outputs/walkforward_<run_id>/
├── BTC-USD/
│   ├── signals.csv        # One row per 45-day window
│   └── metadata.json      # Experiment configuration snapshot
├── ETH-USD/
│   ├── signals.csv
│   └── metadata.json
└── all_signals.csv         # Combined results for both symbols
```

### signals.csv Columns

| Column | Type | Description |
|---|---|---|
| `symbol` | string | Agent ticker (e.g., `BTC-USD`) |
| `window_idx` | int | Walk-forward window index (0, 1, 2, ...) |
| `window_start` | date | Window start date (YYYY-MM-DD) |
| `window_end` | date | Window end date (YYYY-MM-DD) |
| `decision_raw` | string | Raw agent output (BUY / SELL / HOLD) |
| `position` | float | Mapped position: 1.0, -1.0, or 0.0 |
| `latency_s` | float | Inference time in seconds |
| `attempts` | int | Number of attempts (>1 means retries occurred) |
| `error` | string | Error message if the window failed |

## Architecture

### New Components

```
tradingagents/agents/utils/model_metrics_tool.py   — LangChain tool that reads
                                                      deep-trading backtest.csv
                                                      and computes metrics up to
                                                      a cutoff date

tradingagents/agents/analysts/model_analyst.py     — Model Analyst agent node

agent_experiment/experiment/walkforward_config.py  — Config loader for YAML
agent_experiment/experiment/walkforward_runner.py  — Walk-forward batch runner
agent_experiment/scripts/run_walkforward.py        — CLI entry point
agent_experiment/configs/walkforward.yaml          — Default experiment config
```

### Modified Components

| File | Change |
|---|---|
| `tradingagents/agents/utils/agent_states.py` | Added `model_report` field to `AgentState` |
| `tradingagents/agents/__init__.py` | Exported `create_model_analyst` |
| `tradingagents/graph/conditional_logic.py` | Added `should_continue_model()` |
| `tradingagents/graph/setup.py` | Registered model analyst node in graph |
| `tradingagents/graph/trading_graph.py` | Added model tool node + log model_report |
| All analyst/researcher/trader prompts | Added anti–data leakage constraints |

### Data Flow

```
deep-trading artifacts/
  └── backtest.csv (LSTM, XGBoost, ARIMA, Ensemble)
         │
         ▼  get_model_metrics(symbol, cutoff_date)
         │  (only reads bars BEFORE cutoff)
         │
TradingAgents Graph:
  ┌──────────────┐
  │ Model Analyst │ → reads metrics, writes model_report
  ├──────────────┤
  │ Market Analyst│ → technical indicators
  │ News Analyst  │ → news & macro
  │ Fundamentals  │ → financials
  └──────┬───────┘
         ▼
  Bull/Bear Debate (sees all reports including model_report)
         ▼
  Trader (synthesizes all inputs)
         ▼
  Risk Debate (Aggressive / Conservative / Neutral)
         ▼
  Final Decision: BUY / SELL / HOLD
         ▼
  signals.csv (one decision per 45-day window)
```
