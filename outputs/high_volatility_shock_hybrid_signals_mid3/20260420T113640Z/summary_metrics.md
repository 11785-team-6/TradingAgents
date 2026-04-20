# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.0777 | 1.4863 | 0.5133 | 0.3160 | 2.0296 | 3.2970 | -0.1498 | 9.9202 | -0.0052 | -0.0128 | 0.0456 | 0.8403 | -0.0920 | -0.6910 | 0.1696 | 1.0642 | 1.8625 | 0.0194 | 170.4 | 0.5083 | 34.29 | 1.1346 |

**Diagnostics:** 
- Bars: 720 | Long: 3.3% | Short: 30.0% | Flat: 66.7% | Flips: 13

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1313 | 148.6 | 0.8550 | 6.2831 | 11.08 | -0.1328 | 1119 | -0.0203 |
| low_vol | -0.0474 | -0.5704 | 0.2487 | -3.2729 | -4.2068 | -0.0688 | -8.2960 | -0.0069 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.0777 | 1.4863 | 0.5133 | 0.3160 | 2.0296 | 3.2970 | -0.1498 | 9.9202 | -0.0052 | -0.0128 | 0.0456 | 0.8403 | -0.0920 | -0.6910 | 0.1696 | 1.0642 | 1.8625 | 0.0194 | 170.4 | 0.5083 | 34.29 | 1.1346 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1313 | 148.6 | 6.2831 | 11.08 | -0.1328 | 1119 | -0.0203 |
| low_vol | -0.0474 | -0.5704 | -3.2729 | -4.2068 | -0.0688 | -8.2960 | -0.0069 |

*Bars: 720 | Long: 3.3% | Short: 30.0% | Flat: 66.7% | Flips: 13*

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
