# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.0024 | -0.0290 | 0.6132 | 0.3719 | 0.2573 | 0.4243 | -0.1525 | -0.1902 | -0.0080 | -0.0155 | 0.0868 | 0.9653 | -0.0920 | -0.6910 | 0.0895 | 1.2626 | 0.8696 | 0.0208 | 182.6 | 0.4712 | 62.88 | 1.0107 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 70.0% | Flat: 30.0% | Flips: 14

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0600 | 9.6509 | 0.9760 | 2.9095 | 5.1576 | -0.1328 | 72.69 | -0.0224 |
| low_vol | -0.0589 | -0.6521 | 0.3582 | -2.7680 | -4.1444 | -0.1482 | -4.3999 | -0.0091 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.0024 | -0.0290 | 0.6132 | 0.3719 | 0.2573 | 0.4243 | -0.1525 | -0.1902 | -0.0080 | -0.0155 | 0.0868 | 0.9653 | -0.0920 | -0.6910 | 0.0895 | 1.2626 | 0.8696 | 0.0208 | 182.6 | 0.4712 | 62.88 | 1.0107 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0600 | 9.6509 | 2.9095 | 5.1576 | -0.1328 | 72.69 | -0.0224 |
| low_vol | -0.0589 | -0.6521 | -2.7680 | -4.1444 | -0.1482 | -4.3999 | -0.0091 |

*Bars: 720 | Long: 0.0% | Short: 70.0% | Flat: 30.0% | Flips: 14*

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
