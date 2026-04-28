# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1610 | 5.1569 | 0.3291 | 0.1943 | 5.6869 | 9.6338 | -0.0413 | 125 | -0.0056 | -0.0085 | 0.0233 | 0.8764 | -0.2364 | -0.9625 | 0.3974 | 0.7733 | 6.4897 | 0.0222 | 194.8 | 0.5312 | 36 | 1.2915 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 40.0% | Flat: 60.0% | Flips: 15

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1029 | 52.28 | 0.4696 | 8.7012 | 16.19 | -0.0431 | 1211 | -0.0101 |
| low_vol | 0.0527 | 1.4419 | 0.2448 | 3.7701 | 5.8039 | -0.0225 | 64.19 | -0.0070 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1610 | 5.1569 | 0.3291 | 0.1943 | 5.6869 | 9.6338 | -0.0413 | 125 | -0.0056 | -0.0085 | 0.0233 | 0.8764 | -0.2364 | -0.9625 | 0.3974 | 0.7733 | 6.4897 | 0.0222 | 194.8 | 0.5312 | 36 | 1.2915 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1029 | 52.28 | 8.7012 | 16.19 | -0.0431 | 1211 | -0.0101 |
| low_vol | 0.0527 | 1.4419 | 3.7701 | 5.8039 | -0.0225 | 64.19 | -0.0070 |

*Bars: 720 | Long: 0.0% | Short: 40.0% | Flat: 60.0% | Flips: 15*

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
