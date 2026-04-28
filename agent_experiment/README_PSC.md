# Agent + Model 实验 — PSC Bridges-2 运行指南

在 PSC Bridges-2 GPU 集群上运行 Agent + Model Walk-Forward 实验的完整步骤。

## 实验概述

三组对比实验：

| 实验 | 说明 | 入口脚本 |
|------|------|----------|
| Pure Model | 仅用 LSTM/XGBoost/ARIMA/Ensemble 预测 | deep-trading 侧完成 |
| Pure Agent | 仅用 TradingAgents 多 agent 决策（不含 model 输入） | `run_pilot.py` |
| **Agent + Model** | Agent 接收四个模型的历史指标作为额外输入后决策 | `run_walkforward.py` |

Agent + Model 实验的核心流程：
1. Model Analyst 读取 deep-trading 的 backtest.csv，计算截止日前的模型指标（无数据泄漏）
2. 指标报告与 Market/News/Fundamentals 报告一起进入 Bull/Bear Debate → Trader → Risk Debate
3. 每个 45 天窗口输出一个 BUY / SELL / HOLD 决策

## 一、首次设置（只需做一次）

### 1.1 登录 PSC

```bash
ssh <your_andrew_id>@bridges2.psc.edu
```

### 1.2 创建 Conda 环境

```bash
cd /ocean/projects/cis260081p/<your_id>/
module load anaconda3
conda create -n dl_project python=3.10 -y
conda activate dl_project
```

### 1.3 克隆仓库并安装

```bash
cd /ocean/projects/cis260081p/<your_id>/
git clone <repo_url> TradingAgents
cd TradingAgents
git checkout AgentAndModel
pip install -e .
pip install pyyaml
```

### 1.4 安装 Ollama

PSC 登录节点无法从 `ollama.com` 直接下载二进制，但可以从 GitHub Releases 下载压缩包。

**第一步：下载并解压**

```bash
# 创建安装目录
mkdir -p ~/bin

# 从 GitHub 下载压缩包（~1.9GB，约 20 秒）
curl -L https://github.com/ollama/ollama/releases/download/v0.20.2/ollama-linux-amd64.tar.zst -o /tmp/ollama.tar.zst

# 解压（会生成 ~/bin/bin/ 和 ~/bin/lib/ 子目录）
cd ~/bin
tar --use-compress-program=unzstd -xf /tmp/ollama.tar.zst

# 将二进制移到正确位置
cp ~/bin/bin/ollama ~/bin/ollama
chmod +x ~/bin/ollama

# 加入 PATH
export PATH="$HOME/bin:$PATH"

# 验证安装
ollama --version
# 应输出: Warning: could not connect to a running Ollama instance
#         Warning: client version is 0.20.2
```

> **注意**：如果 `unzstd` 不可用，先执行 `module load zstd`。

**第二步：设置模型存储路径**

Home 目录配额有限，必须将模型存储到 ocean 目录：

```bash
export OLLAMA_MODELS=/ocean/projects/cis260081p/<your_id>/.ollama/models
mkdir -p $OLLAMA_MODELS
```

**第三步：拉取模型**

```bash
# 启动 Ollama 服务（后台）
ollama serve &
sleep 5

# 拉取两个模型
ollama pull qwen3:8b        # ~5.2GB
ollama pull qwen3:30b-a3b   # ~18GB

# 验证两个模型都在
ollama list
# 应看到：
# NAME             ID              SIZE
# qwen3:8b         500a1f067a9f    5.2 GB
# qwen3:30b-a3b    ad815644918f    18 GB

# 拉完后关掉 Ollama
kill %1
```

**第四步：清理临时文件**

```bash
rm /tmp/ollama.tar.zst
```

## 二、实验配置

配置文件位于 `agent_experiment/configs/walkforward.yaml`：

```yaml
symbols:
  - symbol_agent: "BTC-USD"          # yfinance ticker
    symbol_deep_trading: "BTC/USDT"  # deep-trading 符号
  - symbol_agent: "ETH-USD"
    symbol_deep_trading: "ETH/USDT"

test_start: "2023-01-01"
test_end: "2025-12-31"
walk_forward_retrain_days: 45

# 模型产物已打包在仓库中
deep_trading_artifacts_dir: "agent_experiment/model_artifacts"

# LLM 设置
llm_provider: "ollama"
quick_think_llm: "qwen3:8b"
deep_think_llm: "qwen3:30b-a3b"
backend_url: "http://localhost:11434/v1"

# 分析师（包含 model 即启用 Model Analyst）
selected_analysts:
  - market
  - news
  - fundamentals
  - model
```

如需只跑 Pure Agent（不含 model），去掉 `selected_analysts` 中的 `model` 即可。

## 三、创建 SLURM 提交脚本

用 `nano train_walkforward.sh` 创建文件，写入以下内容（将 `<your_id>` 替换为你的实际 ID）：

```bash
#!/bin/bash
#SBATCH --job-name=agent-model-wf
#SBATCH -p GPU-shared
#SBATCH --gres=gpu:v100-32:1
#SBATCH -t 24:00:00
#SBATCH -A cis260081p
#SBATCH --output=/ocean/projects/cis260081p/shared/logs/%x-%j.out

set -e
module load anaconda3
conda activate dl_project
mkdir -p /ocean/projects/cis260081p/shared/logs

export PATH="$HOME/bin:$PATH"
export OLLAMA_MODELS=/ocean/projects/cis260081p/<your_id>/.ollama/models

cd /ocean/projects/cis260081p/<your_id>/TradingAgents

# 启动 Ollama 后台服务
ollama serve &
sleep 10

# 检查 GPU
nvidia-smi

# ========== 先 dry-run 验证 pipeline ==========
echo "===== DRY RUN ====="
python -m agent_experiment.scripts.run_walkforward --dry-run -v

# ========== 正式运行 ==========
echo "===== FULL RUN ====="
python -m agent_experiment.scripts.run_walkforward -v

# 清理
kill %1 2>/dev/null || true
```

> **重要**：用 `nano` 编辑时，确保第一行 `#!/bin/bash` 顶格，前面没有空格或空行，否则 `sbatch` 会报错。

保存后赋权：

```bash
chmod +x train_walkforward.sh
```

**GPU 选择建议：**

| GPU | `--gres` 参数 | 适用场景 |
|-----|---------------|----------|
| V100 16GB | `gpu:v100-16:1` | dry-run 调试 |
| V100 32GB | `gpu:v100-32:1` | 正式实验（排队快） |
| L40S 48GB | `gpu:l40s-48:1` | 正式实验（性能更好，排队可能久） |
| H100 80GB | `gpu:h100-80:1` | 大型实验（使用前需协调） |

## 四、提交与监控

### 4.1 提交任务

```bash
ssh <your_id>@bridges2.psc.edu
cd /ocean/projects/cis260081p/<your_id>/TradingAgents
git pull
sbatch train_walkforward.sh
```

### 4.2 监控任务

```bash
# 查看任务状态（PD=排队中，R=运行中）
squeue -u $USER

# 实时查看日志（任务开始运行后才会生成日志文件）
tail -f /ocean/projects/cis260081p/shared/logs/agent-model-wf-<JOBID>.out

# 取消任务
scancel <JOBID>
```

### 4.3 只跑单个 symbol

如果只想跑 BTC-USD：

```bash
python -m agent_experiment.scripts.run_walkforward --symbol BTC-USD -v
```

## 五、输出结果

结果保存在 `outputs/walkforward_<run_id>/`：

```
outputs/walkforward_<run_id>/
├── BTC-USD/
│   ├── signals.csv        # 每个 45 天窗口一行
│   └── metadata.json      # 实验配置快照
├── ETH-USD/
│   ├── signals.csv
│   └── metadata.json
└── all_signals.csv         # 合并结果
```

### signals.csv 字段说明

| 字段 | 说明 |
|------|------|
| `symbol` | 标的（如 `BTC-USD`） |
| `window_idx` | Walk-forward 窗口序号 |
| `window_start` | 窗口起始日期 |
| `window_end` | 窗口结束日期 |
| `decision_raw` | Agent 原始输出（BUY / SELL / HOLD） |
| `position` | 映射仓位：1.0 / -1.0 / 0.0 |
| `latency_s` | 推理耗时（秒） |
| `attempts` | 尝试次数（>1 表示发生了重试） |
| `error` | 错误信息（如有） |

## 六、也可以跑 Pilot 实验（Pure Agent）

Pilot 是小规模验证实验（3 个 20 天窗口，共 60 天，不含 model 输入）：

```bash
# Dry run
python -m agent_experiment.scripts.run_pilot --dry-run -v

# 正式运行
python -m agent_experiment.scripts.run_pilot -v
```

配置文件：`agent_experiment/configs/pilot.yaml`

## 七、常见问题

| 问题 | 解决方案 |
|------|----------|
| `ollama: command not found` | 确认 PATH 设置：`export PATH="$HOME/bin:$PATH"` |
| `ollama --version` 输出 `Not: command not found` | 下载的文件不是二进制。删除后用 `.tar.zst` 压缩包重新安装（见 1.4 节） |
| 模型下载时磁盘满 | 设置 `OLLAMA_MODELS` 到 ocean 目录（见 1.4 第二步） |
| Ollama 模型下载失败 | 在登录节点（有网络）执行 `ollama pull`，不要在计算节点拉模型 |
| `sbatch: error: This does not look like a batch script` | `train_walkforward.sh` 第一行必须是 `#!/bin/bash`，前面不能有空格或空行 |
| 任务状态一直是 PD | 换用排队更快的 GPU（如 `v100-32`），或减少 `#SBATCH -t` 时间 |
| `ModuleNotFoundError: tradingagents` | 确认执行了 `pip install -e .` |
| LLM 推理错误 / 重试 | 已内置重试机制（默认 3 次），日志会显示重试信息 |
| 登录节点直接跑 python | 不要这样做，用 `sbatch` 提交或 `interact` 调试 |

## 八、注意事项

- 先跑 `--dry-run` 确认 pipeline 无误再提交正式任务
- 不要在登录节点跑训练/推理
- 使用唯一的 output 目录，避免覆盖他人结果
- 模型产物（`model_artifacts/`）已打包在仓库中，不需要单独从 deep-trading 生成
- 使用 H100 前与组员协调
- 每次登录 PSC 都需要重新设置环境变量：
  ```bash
  export PATH="$HOME/bin:$PATH"
  export OLLAMA_MODELS=/ocean/projects/cis260081p/<your_id>/.ollama/models
  ```
