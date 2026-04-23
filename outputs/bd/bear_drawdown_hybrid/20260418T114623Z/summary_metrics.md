# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1006 | 2.2123 | 0.2748 | 0.1547 | 4.3832 | 7.7879 | -0.0590 | 37.48 | -0.0042 | -0.0068 | 0.0214 | 0.9042 | -0.2364 | -0.9625 | 0.3370 | 0.7068 | 6.1562 | 0.0222 | 194.8 | 0.5093 | 27 | 1.2695 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 30.0% | Flat: 70.0% | Flips: 15

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0695 | 14.29 | 0.3731 | 7.4964 | 14.49 | -0.0509 | 280.6 | -0.0081 |
| low_vol | 0.0291 | 0.6458 | 0.2192 | 2.3819 | 3.8987 | -0.0279 | 23.17 | -0.0057 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1006 | 2.2123 | 0.2748 | 0.1547 | 4.3832 | 7.7879 | -0.0590 | 37.48 | -0.0042 | -0.0068 | 0.0214 | 0.9042 | -0.2364 | -0.9625 | 0.3370 | 0.7068 | 6.1562 | 0.0222 | 194.8 | 0.5093 | 27 | 1.2695 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0695 | 14.29 | 7.4964 | 14.49 | -0.0509 | 280.6 | -0.0081 |
| low_vol | 0.0291 | 0.6458 | 2.3819 | 3.8987 | -0.0279 | 23.17 | -0.0057 |

*Bars: 720 | Long: 0.0% | Short: 30.0% | Flat: 70.0% | Flips: 15*

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
