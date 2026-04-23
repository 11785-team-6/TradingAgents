# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1586 | 0.1591 | 0.3221 | 0.2086 | 0.6194 | 0.9561 | -0.1999 | 0.7961 | -0.0048 | -0.0084 | 0.0942 | 0.9888 | -0.0544 | -0.0546 | 0.2129 | 0.7073 | 0.2162 | 0.0212 | 185.6 | 0.4993 | 48.26 | 1.0284 |

**Diagnostics:** 
- Bars: 8737 | Long: 2.2% | Short: 49.2% | Flat: 48.6% | Flips: 178

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0298 | 0.1033 | 0.4666 | 0.4437 | 0.6842 | -0.2187 | 0.4723 | -0.0123 |
| low_vol | 0.1250 | 0.1839 | 0.2343 | 0.8376 | 1.3169 | -0.1160 | 1.5850 | -0.0062 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-12-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1586 | 0.1591 | 0.3221 | 0.2086 | 0.6194 | 0.9561 | -0.1999 | 0.7961 | -0.0048 | -0.0084 | 0.0942 | 0.9888 | -0.0544 | -0.0546 | 0.2129 | 0.7073 | 0.2162 | 0.0212 | 185.6 | 0.4993 | 48.26 | 1.0284 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0298 | 0.1033 | 0.4437 | 0.6842 | -0.2187 | 0.4723 | -0.0123 |
| low_vol | 0.1250 | 0.1839 | 0.8376 | 1.3169 | -0.1160 | 1.5850 | -0.0062 |

*Bars: 8737 | Long: 2.2% | Short: 49.2% | Flat: 48.6% | Flips: 178*

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
