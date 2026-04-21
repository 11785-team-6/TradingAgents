# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1627 | -0.8849 | 0.2676 | 0.1919 | -7.9454 | -11.08 | -0.1715 | -5.1592 | -0.0047 | -0.0077 | 0.0740 | 0.8597 | 0.3463 | 36.34 | -0.5090 | 0.6376 | -9.1637 | 0.0208 | 182.6 | 0.4484 | 56.88 | 0.7416 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 63.3% | Flat: 36.7% | Flips: 15

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0970 | -0.9841 | 0.2658 | -15.44 | -19.04 | -0.1020 | -9.6470 | -0.0086 |
| low_vol | -0.0728 | -0.7315 | 0.2678 | -4.7749 | -7.0687 | -0.1104 | -6.6275 | -0.0072 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1627 | -0.8849 | 0.2676 | 0.1919 | -7.9454 | -11.08 | -0.1715 | -5.1592 | -0.0047 | -0.0077 | 0.0740 | 0.8597 | 0.3463 | 36.34 | -0.5090 | 0.6376 | -9.1637 | 0.0208 | 182.6 | 0.4484 | 56.88 | 0.7416 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0970 | -0.9841 | -15.44 | -19.04 | -0.1020 | -9.6470 | -0.0086 |
| low_vol | -0.0728 | -0.7315 | -4.7749 | -7.0687 | -0.1104 | -6.6275 | -0.0072 |

*Bars: 720 | Long: 0.0% | Short: 63.3% | Flat: 36.7% | Flips: 15*

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
