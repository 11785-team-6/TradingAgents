# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1515 | 0.1520 | 0.3464 | 0.2204 | 0.5815 | 0.9139 | -0.3142 | 0.4838 | -0.0052 | -0.0090 | 0.1957 | 0.9896 | -0.0544 | -0.0546 | 0.2058 | 0.7453 | 0.2078 | 0.0227 | 198.7 | 0.4953 | 51.15 | 1.0252 |

**Diagnostics:** 
- Bars: 8737 | Long: 1.9% | Short: 56.0% | Flat: 42.0% | Flips: 188

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0062 | -0.0206 | 0.5000 | 0.2081 | 0.3298 | -0.2509 | -0.0820 | -0.0129 |
| low_vol | 0.1586 | 0.2350 | 0.2534 | 0.9594 | 1.5196 | -0.1664 | 1.4120 | -0.0066 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-12-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1515 | 0.1520 | 0.3464 | 0.2204 | 0.5815 | 0.9139 | -0.3142 | 0.4838 | -0.0052 | -0.0090 | 0.1957 | 0.9896 | -0.0544 | -0.0546 | 0.2058 | 0.7453 | 0.2078 | 0.0227 | 198.7 | 0.4953 | 51.15 | 1.0252 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0062 | -0.0206 | 0.2081 | 0.3298 | -0.2509 | -0.0820 | -0.0129 |
| low_vol | 0.1586 | 0.2350 | 0.9594 | 1.5196 | -0.1664 | 1.4120 | -0.0066 |

*Bars: 8737 | Long: 1.9% | Short: 56.0% | Flat: 42.0% | Flips: 188*

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
