# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1771 | -0.9068 | 0.3446 | 0.2708 | -6.7126 | -8.5417 | -0.1911 | -4.7452 | -0.0047 | -0.0103 | 0.1051 | 0.9944 | 0.3463 | 36.34 | -0.5234 | 0.7402 | -8.1457 | 0.0208 | 182.6 | 0.4687 | 41.88 | 0.7045 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 14

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1004 | -0.9863 | 0.5299 | -7.8326 | -9.8853 | -0.1217 | -8.1065 | -0.0161 |
| low_vol | -0.0853 | -0.7877 | 0.2214 | -6.8897 | -9.1483 | -0.1178 | -6.6878 | -0.0068 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1771 | -0.9068 | 0.3446 | 0.2708 | -6.7126 | -8.5417 | -0.1911 | -4.7452 | -0.0047 | -0.0103 | 0.1051 | 0.9944 | 0.3463 | 36.34 | -0.5234 | 0.7402 | -8.1457 | 0.0208 | 182.6 | 0.4687 | 41.88 | 0.7045 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1004 | -0.9863 | -7.8326 | -9.8853 | -0.1217 | -8.1065 | -0.0161 |
| low_vol | -0.0853 | -0.7877 | -6.8897 | -9.1483 | -0.1178 | -6.6878 | -0.0068 |

*Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 14*

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
