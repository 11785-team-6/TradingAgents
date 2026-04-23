# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.0276 | 0.0277 | 0.3590 | 0.2274 | 0.2553 | 0.4030 | -0.2488 | 0.1113 | -0.0053 | -0.0091 | 0.1511 | 0.9971 | -0.0544 | -0.0546 | 0.0820 | 0.7540 | 0.0598 | 0.0228 | 199.7 | 0.4948 | 52.32 | 1.0110 |

**Diagnostics:** 
- Bars: 8737 | Long: 1.9% | Short: 58.0% | Flat: 40.1% | Flips: 190

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0041 | 0.0136 | 0.5296 | 0.2899 | 0.4693 | -0.2771 | 0.0492 | -0.0130 |
| low_vol | 0.0234 | 0.0338 | 0.2527 | 0.2577 | 0.3978 | -0.1492 | 0.2262 | -0.0068 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-12-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.0276 | 0.0277 | 0.3590 | 0.2274 | 0.2553 | 0.4030 | -0.2488 | 0.1113 | -0.0053 | -0.0091 | 0.1511 | 0.9971 | -0.0544 | -0.0546 | 0.0820 | 0.7540 | 0.0598 | 0.0228 | 199.7 | 0.4948 | 52.32 | 1.0110 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0041 | 0.0136 | 0.2899 | 0.4693 | -0.2771 | 0.0492 | -0.0130 |
| low_vol | 0.0234 | 0.0338 | 0.2577 | 0.3978 | -0.1492 | 0.2262 | -0.0068 |

*Bars: 8737 | Long: 1.9% | Short: 58.0% | Flat: 40.1% | Flips: 190*

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
