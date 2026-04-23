# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1035 | -0.7354 | 0.2457 | 0.1736 | -5.2891 | -7.4851 | -0.1411 | -5.2122 | -0.0036 | -0.0071 | 0.0710 | 0.9597 | 0.3463 | 36.34 | -0.4497 | 0.6106 | -8.2149 | 0.0236 | 207 | 0.4599 | 31.89 | 0.7582 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 40.0% | Flat: 60.0% | Flips: 17

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0111 | -0.3631 | 0.3167 | -1.2671 | -2.0446 | -0.0591 | -6.1472 | -0.0080 |
| low_vol | -0.0934 | -0.8184 | 0.2078 | -8.1055 | -10.34 | -0.0985 | -8.3118 | -0.0065 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1035 | -0.7354 | 0.2457 | 0.1736 | -5.2891 | -7.4851 | -0.1411 | -5.2122 | -0.0036 | -0.0071 | 0.0710 | 0.9597 | 0.3463 | 36.34 | -0.4497 | 0.6106 | -8.2149 | 0.0236 | 207 | 0.4599 | 31.89 | 0.7582 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0111 | -0.3631 | -1.2671 | -2.0446 | -0.0591 | -6.1472 | -0.0080 |
| low_vol | -0.0934 | -0.8184 | -8.1055 | -10.34 | -0.0985 | -8.3118 | -0.0065 |

*Bars: 720 | Long: 0.0% | Short: 40.0% | Flat: 60.0% | Flips: 17*

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
