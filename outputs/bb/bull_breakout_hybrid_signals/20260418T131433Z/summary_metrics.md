# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.2197 | -0.9512 | 0.2815 | 0.2059 | -10.59 | -14.47 | -0.2197 | -4.3294 | -0.0049 | -0.0084 | 0.1228 | 0.9319 | 0.3463 | 36.34 | -0.5660 | 0.6555 | -10.22 | 0.0236 | 207 | 0.4345 | 39.89 | 0.6332 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 50.0% | Flat: 50.0% | Flips: 17

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0941 | -0.9819 | 0.3506 | -11.26 | -16.34 | -0.0941 | -10.44 | -0.0100 |
| low_vol | -0.1387 | -0.9255 | 0.2459 | -10.44 | -13.69 | -0.1369 | -6.7586 | -0.0075 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.2197 | -0.9512 | 0.2815 | 0.2059 | -10.59 | -14.47 | -0.2197 | -4.3294 | -0.0049 | -0.0084 | 0.1228 | 0.9319 | 0.3463 | 36.34 | -0.5660 | 0.6555 | -10.22 | 0.0236 | 207 | 0.4345 | 39.89 | 0.6332 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0941 | -0.9819 | -11.26 | -16.34 | -0.0941 | -10.44 | -0.0100 |
| low_vol | -0.1387 | -0.9255 | -10.44 | -13.69 | -0.1369 | -6.7586 | -0.0075 |

*Bars: 720 | Long: 0.0% | Short: 50.0% | Flat: 50.0% | Flips: 17*

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
