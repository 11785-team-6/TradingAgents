# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1795 | -0.1801 | 0.3115 | 0.2060 | -0.4817 | -0.7282 | -0.4004 | -0.4498 | -0.0048 | -0.0083 | 0.2785 | 0.9961 | -0.0544 | -0.0546 | -0.1252 | 0.6988 | -0.2813 | 0.0205 | 179.6 | 0.4959 | 51.51 | 0.9791 |

**Diagnostics:** 
- Bars: 8737 | Long: 2.2% | Short: 50.3% | Flat: 47.5% | Flips: 171

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.2240 | -0.5718 | 0.4337 | -1.7383 | -2.6054 | -0.4061 | -1.4080 | -0.0117 |
| low_vol | 0.0573 | 0.0831 | 0.2407 | 0.4519 | 0.6988 | -0.2260 | 0.3677 | -0.0065 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-12-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1795 | -0.1801 | 0.3115 | 0.2060 | -0.4817 | -0.7282 | -0.4004 | -0.4498 | -0.0048 | -0.0083 | 0.2785 | 0.9961 | -0.0544 | -0.0546 | -0.1252 | 0.6988 | -0.2813 | 0.0205 | 179.6 | 0.4959 | 51.51 | 0.9791 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.2240 | -0.5718 | -1.7383 | -2.6054 | -0.4061 | -1.4080 | -0.0117 |
| low_vol | 0.0573 | 0.0831 | 0.4519 | 0.6988 | -0.2260 | 0.3677 | -0.0065 |

*Bars: 8737 | Long: 2.2% | Short: 50.3% | Flat: 47.5% | Flips: 171*

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
