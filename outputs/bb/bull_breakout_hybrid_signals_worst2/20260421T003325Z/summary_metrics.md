# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.0737 | -0.6065 | 0.2708 | 0.1760 | -3.3092 | -5.0917 | -0.1182 | -5.1316 | -0.0041 | -0.0075 | 0.0854 | 0.9597 | 0.3463 | 36.34 | -0.4200 | 0.6418 | -7.1876 | 0.0250 | 219.2 | 0.4615 | 34.67 | 0.8499 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 43.3% | Flat: 56.7% | Flips: 18

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0240 | -0.6263 | 0.3945 | -2.2986 | -3.7299 | -0.0754 | -8.3027 | -0.0105 |
| low_vol | -0.0510 | -0.5976 | 0.1950 | -4.5709 | -6.5647 | -0.0569 | -10.5 | -0.0056 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.0737 | -0.6065 | 0.2708 | 0.1760 | -3.3092 | -5.0917 | -0.1182 | -5.1316 | -0.0041 | -0.0075 | 0.0854 | 0.9597 | 0.3463 | 36.34 | -0.4200 | 0.6418 | -7.1876 | 0.0250 | 219.2 | 0.4615 | 34.67 | 0.8499 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0240 | -0.6263 | -2.2986 | -3.7299 | -0.0754 | -8.3027 | -0.0105 |
| low_vol | -0.0510 | -0.5976 | -4.5709 | -6.5647 | -0.0569 | -10.5 | -0.0056 |

*Bars: 720 | Long: 0.0% | Short: 43.3% | Flat: 56.7% | Flips: 18*

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
