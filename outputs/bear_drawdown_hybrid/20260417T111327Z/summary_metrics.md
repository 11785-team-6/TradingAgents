# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.0972 | 2.0936 | 0.3343 | 0.2003 | 3.5453 | 5.9156 | -0.0604 | 34.66 | -0.0056 | -0.0087 | 0.0207 | 0.7931 | -0.2364 | -0.9625 | 0.3336 | 0.7799 | 5.5542 | 0.0208 | 182.6 | 0.5177 | 38.88 | 1.1709 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 43.3% | Flat: 56.7% | Flips: 15

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0959 | 40.14 | 0.3850 | 9.8472 | 18.3 | -0.0495 | 810.8 | -0.0091 |
| low_vol | 0.0012 | 0.0206 | 0.3092 | 0.2204 | 0.3458 | -0.0604 | 0.3407 | -0.0083 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.0972 | 2.0936 | 0.3343 | 0.2003 | 3.5453 | 5.9156 | -0.0604 | 34.66 | -0.0056 | -0.0087 | 0.0207 | 0.7931 | -0.2364 | -0.9625 | 0.3336 | 0.7799 | 5.5542 | 0.0208 | 182.6 | 0.5177 | 38.88 | 1.1709 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0959 | 40.14 | 9.8472 | 18.3 | -0.0495 | 810.8 | -0.0091 |
| low_vol | 0.0012 | 0.0206 | 0.2204 | 0.3458 | -0.0604 | 0.3407 | -0.0083 |

*Bars: 720 | Long: 0.0% | Short: 43.3% | Flat: 56.7% | Flips: 15*

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
