# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.2154 | -0.9479 | 0.4033 | 0.2953 | -7.1208 | -9.7226 | -0.2288 | -4.1432 | -0.0064 | -0.0115 | 0.1657 | 0.9944 | 0.3463 | 36.34 | -0.5617 | 0.8245 | -7.9906 | 0.0153 | 133.9 | 0.4574 | 91.83 | 0.7548 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 76.7% | Flat: 23.3% | Flips: 10

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1553 | -0.9989 | 0.6202 | -10.73 | -14.63 | -0.1697 | -5.8862 | -0.0173 |
| low_vol | -0.0711 | -0.7229 | 0.2578 | -4.8488 | -7.1094 | -0.0821 | -8.8101 | -0.0072 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.2154 | -0.9479 | 0.4033 | 0.2953 | -7.1208 | -9.7226 | -0.2288 | -4.1432 | -0.0064 | -0.0115 | 0.1657 | 0.9944 | 0.3463 | 36.34 | -0.5617 | 0.8245 | -7.9906 | 0.0153 | 133.9 | 0.4574 | 91.83 | 0.7548 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1553 | -0.9989 | -10.73 | -14.63 | -0.1697 | -5.8862 | -0.0173 |
| low_vol | -0.0711 | -0.7229 | -4.8488 | -7.1094 | -0.0821 | -8.8101 | -0.0072 |

*Bars: 720 | Long: 0.0% | Short: 76.7% | Flat: 23.3% | Flips: 10*

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
