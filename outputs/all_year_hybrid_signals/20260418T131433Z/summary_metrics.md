# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.0026 | -0.0309 | 0.2850 | 0.1807 | 0.0320 | 0.0505 | -0.0833 | -0.3709 | -0.0050 | -0.0079 | 0.0439 | 0.9458 | -0.2364 | -0.9625 | 0.2338 | 0.7042 | 4.4808 | 0.0222 | 194.8 | 0.5000 | 30 | 1.0016 |

**Diagnostics:** 
- Bars: 720 | Long: 3.3% | Short: 30.0% | Flat: 66.7% | Flips: 14

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0753 | 18 | 0.3670 | 8.2081 | 15.71 | -0.0538 | 334.7 | -0.0083 |
| low_vol | -0.0724 | -0.7293 | 0.2401 | -5.3216 | -7.2743 | -0.0972 | -7.5049 | -0.0076 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.0026 | -0.0309 | 0.2850 | 0.1807 | 0.0320 | 0.0505 | -0.0833 | -0.3709 | -0.0050 | -0.0079 | 0.0439 | 0.9458 | -0.2364 | -0.9625 | 0.2338 | 0.7042 | 4.4808 | 0.0222 | 194.8 | 0.5000 | 30 | 1.0016 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0753 | 18 | 8.2081 | 15.71 | -0.0538 | 334.7 | -0.0083 |
| low_vol | -0.0724 | -0.7293 | -5.3216 | -7.2743 | -0.0972 | -7.5049 | -0.0076 |

*Bars: 720 | Long: 3.3% | Short: 30.0% | Flat: 66.7% | Flips: 14*

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
