# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1112 | -0.7620 | 0.4612 | 0.3308 | -2.8807 | -4.0155 | -0.2157 | -3.5330 | -0.0067 | -0.0132 | 0.1700 | 0.9125 | -0.0920 | -0.6910 | -0.0193 | 1.0493 | -0.3701 | 0.0236 | 207 | 0.4896 | 37.22 | 0.8731 |

**Diagnostics:** 
- Bars: 720 | Long: 3.3% | Short: 43.3% | Flat: 53.3% | Flips: 16

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1613 | -0.9992 | 0.6955 | -9.9099 | -13.4 | -0.2239 | -4.4632 | -0.0214 |
| low_vol | 0.0597 | 1.7422 | 0.3072 | 3.4376 | 5.6142 | -0.0600 | 29.05 | -0.0070 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1112 | -0.7620 | 0.4612 | 0.3308 | -2.8807 | -4.0155 | -0.2157 | -3.5330 | -0.0067 | -0.0132 | 0.1700 | 0.9125 | -0.0920 | -0.6910 | -0.0193 | 1.0493 | -0.3701 | 0.0236 | 207 | 0.4896 | 37.22 | 0.8731 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1613 | -0.9992 | -9.9099 | -13.4 | -0.2239 | -4.4632 | -0.0214 |
| low_vol | 0.0597 | 1.7422 | 3.4376 | 5.6142 | -0.0600 | 29.05 | -0.0070 |

*Bars: 720 | Long: 3.3% | Short: 43.3% | Flat: 53.3% | Flips: 16*

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
