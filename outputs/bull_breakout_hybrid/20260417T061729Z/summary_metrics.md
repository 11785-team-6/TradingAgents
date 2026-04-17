# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1471 | -0.8559 | 0.3143 | 0.2583 | -6.0034 | -7.3051 | -0.1925 | -4.4452 | -0.0043 | -0.0096 | 0.1673 | 0.9944 | 0.3463 | 36.34 | -0.4934 | 0.6986 | -8.0208 | 0.0194 | 170.4 | 0.4508 | 37.71 | 0.7007 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 36.7% | Flat: 63.3% | Flips: 13

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1314 | -0.9967 | 0.5204 | -10.72 | -13.07 | -0.1623 | -6.1393 | -0.0162 |
| low_vol | -0.0181 | -0.2722 | 0.1553 | -1.9685 | -2.6332 | -0.0509 | -5.3463 | -0.0047 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1471 | -0.8559 | 0.3143 | 0.2583 | -6.0034 | -7.3051 | -0.1925 | -4.4452 | -0.0043 | -0.0096 | 0.1673 | 0.9944 | 0.3463 | 36.34 | -0.4934 | 0.6986 | -8.0208 | 0.0194 | 170.4 | 0.4508 | 37.71 | 0.7007 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1314 | -0.9967 | -10.72 | -13.07 | -0.1623 | -6.1393 | -0.0162 |
| low_vol | -0.0181 | -0.2722 | -1.9685 | -2.6332 | -0.0509 | -5.3463 | -0.0047 |

*Bars: 720 | Long: 0.0% | Short: 36.7% | Flat: 63.3% | Flips: 13*

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
