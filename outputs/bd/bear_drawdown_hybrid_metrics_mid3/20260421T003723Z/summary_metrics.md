# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1999 | 8.1988 | 0.3882 | 0.2203 | 5.9111 | 10.42 | -0.0795 | 103.2 | -0.0069 | -0.0091 | 0.0248 | 0.8028 | -0.2364 | -0.9625 | 0.4363 | 0.8515 | 6.3898 | 0.0264 | 231.3 | 0.5061 | 40.7 | 1.2547 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 56.7% | Flat: 43.3% | Flips: 18

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1509 | 299.4 | 0.5209 | 11.22 | 21.32 | -0.0574 | 5216 | -0.0109 |
| low_vol | 0.0426 | 1.0648 | 0.3132 | 2.4717 | 4.0460 | -0.0795 | 13.4 | -0.0081 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1999 | 8.1988 | 0.3882 | 0.2203 | 5.9111 | 10.42 | -0.0795 | 103.2 | -0.0069 | -0.0091 | 0.0248 | 0.8028 | -0.2364 | -0.9625 | 0.4363 | 0.8515 | 6.3898 | 0.0264 | 231.3 | 0.5061 | 40.7 | 1.2547 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1509 | 299.4 | 11.22 | 21.32 | -0.0574 | 5216 | -0.0109 |
| low_vol | 0.0426 | 1.0648 | 2.4717 | 4.0460 | -0.0795 | 13.4 | -0.0081 |

*Bars: 720 | Long: 0.0% | Short: 56.7% | Flat: 43.3% | Flips: 18*

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
