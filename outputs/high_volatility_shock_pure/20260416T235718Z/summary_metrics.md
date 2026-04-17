# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1799 | -0.9106 | 0.5197 | 0.3542 | -4.3848 | -6.4335 | -0.1905 | -4.7801 | -0.0075 | -0.0139 | 0.1156 | 0.9972 | -0.0920 | -0.6910 | -0.0879 | 1.0034 | -1.3342 | 0.0222 | 194.8 | 0.4452 | 57 | 0.8317 |

**Diagnostics:** 
- Bars: 720 | Long: 10.0% | Short: 53.3% | Flat: 36.7% | Flips: 14

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1310 | -0.9966 | 0.7625 | -7.0896 | -10.01 | -0.1565 | -6.3694 | -0.0225 |
| low_vol | -0.0562 | -0.6346 | 0.3688 | -2.5454 | -4.1323 | -0.0915 | -6.9364 | -0.0090 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1799 | -0.9106 | 0.5197 | 0.3542 | -4.3848 | -6.4335 | -0.1905 | -4.7801 | -0.0075 | -0.0139 | 0.1156 | 0.9972 | -0.0920 | -0.6910 | -0.0879 | 1.0034 | -1.3342 | 0.0222 | 194.8 | 0.4452 | 57 | 0.8317 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1310 | -0.9966 | -7.0896 | -10.01 | -0.1565 | -6.3694 | -0.0225 |
| low_vol | -0.0562 | -0.6346 | -2.5454 | -4.1323 | -0.0915 | -6.9364 | -0.0090 |

*Bars: 720 | Long: 10.0% | Short: 53.3% | Flat: 36.7% | Flips: 14*

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
