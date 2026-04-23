# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1328 | -0.8235 | 0.4592 | 0.3634 | -3.5440 | -4.4783 | -0.2100 | -3.9209 | -0.0055 | -0.0138 | 0.1251 | 0.7917 | -0.0920 | -0.6910 | -0.0408 | 0.9271 | -0.7414 | 0.0194 | 170.4 | 0.4917 | 34.29 | 0.8141 |

**Diagnostics:** 
- Bars: 720 | Long: 3.3% | Short: 30.0% | Flat: 66.7% | Flips: 13

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1058 | -0.9893 | 0.7586 | -5.5969 | -7.1487 | -0.1870 | -5.2895 | -0.0252 |
| low_vol | -0.0302 | -0.4129 | 0.2327 | -2.1715 | -2.9088 | -0.0504 | -8.1917 | -0.0065 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1328 | -0.8235 | 0.4592 | 0.3634 | -3.5440 | -4.4783 | -0.2100 | -3.9209 | -0.0055 | -0.0138 | 0.1251 | 0.7917 | -0.0920 | -0.6910 | -0.0408 | 0.9271 | -0.7414 | 0.0194 | 170.4 | 0.4917 | 34.29 | 0.8141 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1058 | -0.9893 | -5.5969 | -7.1487 | -0.1870 | -5.2895 | -0.0252 |
| low_vol | -0.0302 | -0.4129 | -2.1715 | -2.9088 | -0.0504 | -8.1917 | -0.0065 |

*Bars: 720 | Long: 3.3% | Short: 30.0% | Flat: 66.7% | Flips: 13*

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
