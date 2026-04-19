# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1526 | 4.6379 | 0.3765 | 0.2217 | 4.7825 | 8.1209 | -0.0559 | 82.95 | -0.0068 | -0.0094 | 0.0182 | 0.7917 | -0.2364 | -0.9625 | 0.3891 | 0.8224 | 6.0148 | 0.0306 | 267.8 | 0.5268 | 30.55 | 1.2297 |

**Diagnostics:** 
- Bars: 720 | Long: 3.3% | Short: 43.3% | Flat: 53.3% | Flips: 20

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0751 | 17.9 | 0.5328 | 5.7827 | 10.15 | -0.0513 | 348.7 | -0.0121 |
| low_vol | 0.0721 | 2.3573 | 0.2840 | 4.4063 | 7.2707 | -0.0364 | 64.77 | -0.0073 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1526 | 4.6379 | 0.3765 | 0.2217 | 4.7825 | 8.1209 | -0.0559 | 82.95 | -0.0068 | -0.0094 | 0.0182 | 0.7917 | -0.2364 | -0.9625 | 0.3891 | 0.8224 | 6.0148 | 0.0306 | 267.8 | 0.5268 | 30.55 | 1.2297 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0751 | 17.9 | 5.7827 | 10.15 | -0.0513 | 348.7 | -0.0121 |
| low_vol | 0.0721 | 2.3573 | 4.4063 | 7.2707 | -0.0364 | 64.77 | -0.0073 |

*Bars: 720 | Long: 3.3% | Short: 43.3% | Flat: 53.3% | Flips: 20*

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
