# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.0775 | 1.4807 | 0.2081 | 0.1122 | 4.4690 | 8.2895 | -0.0275 | 53.78 | -0.0026 | -0.0047 | 0.0119 | 0.8903 | 0.3463 | 36.34 | -0.2688 | 0.5687 | -4.8997 | 0.0222 | 194.8 | 0.5152 | 33 | 1.2707 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 36.7% | Flat: 63.3% | Flips: 16

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0122 | 0.6327 | 0.2934 | 1.8164 | 3.6737 | -0.0340 | 18.59 | -0.0062 |
| low_vol | 0.0645 | 1.9678 | 0.1581 | 6.9614 | 11.66 | -0.0150 | 131.5 | -0.0039 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.0775 | 1.4807 | 0.2081 | 0.1122 | 4.4690 | 8.2895 | -0.0275 | 53.78 | -0.0026 | -0.0047 | 0.0119 | 0.8903 | 0.3463 | 36.34 | -0.2688 | 0.5687 | -4.8997 | 0.0222 | 194.8 | 0.5152 | 33 | 1.2707 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0122 | 0.6327 | 1.8164 | 3.6737 | -0.0340 | 18.59 | -0.0062 |
| low_vol | 0.0645 | 1.9678 | 6.9614 | 11.66 | -0.0150 | 131.5 | -0.0039 |

*Bars: 720 | Long: 0.0% | Short: 36.7% | Flat: 63.3% | Flips: 16*

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
