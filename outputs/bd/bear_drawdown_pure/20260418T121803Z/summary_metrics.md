# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.2586 | 15.45 | 0.4080 | 0.2337 | 7.0681 | 12.34 | -0.0688 | 224.4 | -0.0072 | -0.0098 | 0.0232 | 0.8472 | -0.2364 | -0.9625 | 0.4950 | 0.8790 | 6.8601 | 0.0222 | 194.8 | 0.5506 | 42 | 1.3507 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 16

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1343 | 165.5 | 0.6263 | 8.4812 | 16.19 | -0.0574 | 2883 | -0.0124 |
| low_vol | 0.1096 | 5.0997 | 0.2632 | 7.0029 | 11.32 | -0.0370 | 138 | -0.0073 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.2586 | 15.45 | 0.4080 | 0.2337 | 7.0681 | 12.34 | -0.0688 | 224.4 | -0.0072 | -0.0098 | 0.0232 | 0.8472 | -0.2364 | -0.9625 | 0.4950 | 0.8790 | 6.8601 | 0.0222 | 194.8 | 0.5506 | 42 | 1.3507 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1343 | 165.5 | 8.4812 | 16.19 | -0.0574 | 2883 | -0.0124 |
| low_vol | 0.1096 | 5.0997 | 7.0029 | 11.32 | -0.0370 | 138 | -0.0073 |

*Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 16*

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
