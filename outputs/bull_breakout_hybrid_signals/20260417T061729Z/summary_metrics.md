# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.0604 | -0.5314 | 0.2199 | 0.1633 | -3.3373 | -4.4939 | -0.0952 | -5.5802 | -0.0031 | -0.0068 | 0.0619 | 0.8569 | 0.3463 | 36.34 | -0.4066 | 0.5805 | -7.6662 | 0.0194 | 170.4 | 0.4708 | 34.29 | 0.8280 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 33.3% | Flat: 66.7% | Flips: 14

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0626 | -0.9274 | 0.2793 | -9.2458 | -11.69 | -0.0686 | -13.51 | -0.0093 |
| low_vol | 0.0024 | 0.0419 | 0.1881 | 0.3124 | 0.4509 | -0.0521 | 0.8038 | -0.0053 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.0604 | -0.5314 | 0.2199 | 0.1633 | -3.3373 | -4.4939 | -0.0952 | -5.5802 | -0.0031 | -0.0068 | 0.0619 | 0.8569 | 0.3463 | 36.34 | -0.4066 | 0.5805 | -7.6662 | 0.0194 | 170.4 | 0.4708 | 34.29 | 0.8280 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0626 | -0.9274 | -9.2458 | -11.69 | -0.0686 | -13.51 | -0.0093 |
| low_vol | 0.0024 | 0.0419 | 0.3124 | 0.4509 | -0.0521 | 0.8038 | -0.0053 |

*Bars: 720 | Long: 0.0% | Short: 33.3% | Flat: 66.7% | Flips: 14*

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
