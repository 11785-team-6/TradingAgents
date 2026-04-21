# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.0428 | 0.6665 | 0.4338 | 0.2569 | 1.3938 | 2.3532 | -0.0944 | 7.0570 | -0.0076 | -0.0103 | 0.0440 | 0.8792 | -0.2364 | -0.9625 | 0.2793 | 0.9152 | 4.0984 | 0.0153 | 133.9 | 0.5031 | 79.83 | 1.0513 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 66.7% | Flat: 33.3% | Flips: 11

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0257 | 1.8002 | 0.5959 | 2.0252 | 3.6959 | -0.0933 | 19.3 | -0.0125 |
| low_vol | 0.0167 | 0.3341 | 0.3415 | 1.0148 | 1.6084 | -0.0559 | 5.9815 | -0.0088 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.0428 | 0.6665 | 0.4338 | 0.2569 | 1.3938 | 2.3532 | -0.0944 | 7.0570 | -0.0076 | -0.0103 | 0.0440 | 0.8792 | -0.2364 | -0.9625 | 0.2793 | 0.9152 | 4.0984 | 0.0153 | 133.9 | 0.5031 | 79.83 | 1.0513 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0257 | 1.8002 | 2.0252 | 3.6959 | -0.0933 | 19.3 | -0.0125 |
| low_vol | 0.0167 | 0.3341 | 1.0148 | 1.6084 | -0.0559 | 5.9815 | -0.0088 |

*Bars: 720 | Long: 0.0% | Short: 66.7% | Flat: 33.3% | Flips: 11*

---

## 3. Metric Definitions (from deep-trading)

| Metric | Description |
| --- | --- |
| cumulative_return | Total strategy return |
| annualized_return | Annualized return |
| sharpe | Sharpe ratio |
| max_drawdown | Maximum drawdown |
| sortino | Sortino ratio |
| calmar | Calmar ratio (return / max drawdown) |
| excess_cumulative_return | Strategy − benchmark |
| information_ratio | Excess return / tracking error |
| hit_rate | Fraction of bars with correct direction |
| turnover_annualized | Annualized turnover |
| profit_factor | Gains / losses |
