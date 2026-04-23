# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1802 | 6.5159 | 0.3581 | 0.1990 | 5.8121 | 10.46 | -0.0594 | 109.6 | -0.0053 | -0.0086 | 0.0240 | 0.8139 | -0.2364 | -0.9625 | 0.4166 | 0.8109 | 6.4464 | 0.0167 | 146.1 | 0.5139 | 48 | 1.3225 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 40.0% | Flat: 60.0% | Flips: 11

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1284 | 133.9 | 0.5194 | 9.7037 | 18.56 | -0.0497 | 2695 | -0.0109 |
| low_vol | 0.0458 | 1.1807 | 0.2587 | 3.1426 | 5.2293 | -0.0674 | 17.53 | -0.0066 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1802 | 6.5159 | 0.3581 | 0.1990 | 5.8121 | 10.46 | -0.0594 | 109.6 | -0.0053 | -0.0086 | 0.0240 | 0.8139 | -0.2364 | -0.9625 | 0.4166 | 0.8109 | 6.4464 | 0.0167 | 146.1 | 0.5139 | 48 | 1.3225 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1284 | 133.9 | 9.7037 | 18.56 | -0.0497 | 2695 | -0.0109 |
| low_vol | 0.0458 | 1.1807 | 3.1426 | 5.2293 | -0.0674 | 17.53 | -0.0066 |

*Bars: 720 | Long: 0.0% | Short: 40.0% | Flat: 60.0% | Flips: 11*

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
