# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.0642 | -0.5540 | 0.3176 | 0.2401 | -2.3823 | -3.1511 | -0.1004 | -5.5167 | -0.0038 | -0.0085 | 0.0636 | 0.9944 | 0.3463 | 36.34 | -0.4104 | 0.7033 | -6.3605 | 0.0250 | 219.2 | 0.4792 | 26.67 | 0.8595 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 33.3% | Flat: 66.7% | Flips: 17

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0351 | -0.7650 | 0.5224 | -2.5086 | -3.3014 | -0.1004 | -7.6175 | -0.0148 |
| low_vol | -0.0302 | -0.4131 | 0.1648 | -3.1520 | -4.4554 | -0.0566 | -7.2982 | -0.0050 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.0642 | -0.5540 | 0.3176 | 0.2401 | -2.3823 | -3.1511 | -0.1004 | -5.5167 | -0.0038 | -0.0085 | 0.0636 | 0.9944 | 0.3463 | 36.34 | -0.4104 | 0.7033 | -6.3605 | 0.0250 | 219.2 | 0.4792 | 26.67 | 0.8595 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0351 | -0.7650 | -2.5086 | -3.3014 | -0.1004 | -7.6175 | -0.0148 |
| low_vol | -0.0302 | -0.4131 | -3.1520 | -4.4554 | -0.0566 | -7.2982 | -0.0050 |

*Bars: 720 | Long: 0.0% | Short: 33.3% | Flat: 66.7% | Flips: 17*

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
