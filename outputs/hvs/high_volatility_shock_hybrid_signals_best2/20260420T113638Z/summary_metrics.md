# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1111 | 2.6057 | 0.4259 | 0.2381 | 3.2228 | 5.7652 | -0.0727 | 35.83 | -0.0051 | -0.0097 | 0.0340 | 0.9361 | -0.0920 | -0.6910 | 0.2030 | 1.0053 | 2.3006 | 0.0181 | 158.3 | 0.4599 | 41 | 1.1874 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 40.0% | Flat: 60.0% | Flips: 13

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0892 | 31.04 | 0.6278 | 5.8338 | 11 | -0.0578 | 537 | -0.0139 |
| low_vol | 0.0201 | 0.4139 | 0.2997 | 1.3051 | 2.1657 | -0.0828 | 4.9999 | -0.0072 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1111 | 2.6057 | 0.4259 | 0.2381 | 3.2228 | 5.7652 | -0.0727 | 35.83 | -0.0051 | -0.0097 | 0.0340 | 0.9361 | -0.0920 | -0.6910 | 0.2030 | 1.0053 | 2.3006 | 0.0181 | 158.3 | 0.4599 | 41 | 1.1874 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0892 | 31.04 | 5.8338 | 11 | -0.0578 | 537 | -0.0139 |
| low_vol | 0.0201 | 0.4139 | 1.3051 | 2.1657 | -0.0828 | 4.9999 | -0.0072 |

*Bars: 720 | Long: 0.0% | Short: 40.0% | Flat: 60.0% | Flips: 13*

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
