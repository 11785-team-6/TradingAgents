# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1294 | 3.4017 | 0.2823 | 0.1633 | 5.3908 | 9.3208 | -0.0437 | 77.86 | -0.0044 | -0.0072 | 0.0164 | 0.7222 | -0.2364 | -0.9625 | 0.3659 | 0.7155 | 6.5242 | 0.0181 | 158.3 | 0.5209 | 30.71 | 1.3217 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 30.0% | Flat: 70.0% | Flips: 13

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0986 | 44.37 | 0.3018 | 12.79 | 25.07 | -0.0223 | 1990 | -0.0067 |
| low_vol | 0.0281 | 0.6196 | 0.2728 | 1.9036 | 3.1134 | -0.0437 | 14.18 | -0.0073 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1294 | 3.4017 | 0.2823 | 0.1633 | 5.3908 | 9.3208 | -0.0437 | 77.86 | -0.0044 | -0.0072 | 0.0164 | 0.7222 | -0.2364 | -0.9625 | 0.3659 | 0.7155 | 6.5242 | 0.0181 | 158.3 | 0.5209 | 30.71 | 1.3217 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0986 | 44.37 | 12.79 | 25.07 | -0.0223 | 1990 | -0.0067 |
| low_vol | 0.0281 | 0.6196 | 1.9036 | 3.1134 | -0.0437 | 14.18 | -0.0073 |

*Bars: 720 | Long: 0.0% | Short: 30.0% | Flat: 70.0% | Flips: 13*

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
