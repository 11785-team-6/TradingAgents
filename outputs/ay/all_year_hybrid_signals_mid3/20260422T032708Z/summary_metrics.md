# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1539 | -0.1544 | 0.2781 | 0.1888 | -0.4636 | -0.6831 | -0.3884 | -0.3975 | -0.0041 | -0.0075 | 0.2765 | 0.9961 | -0.0544 | -0.0546 | -0.0995 | 0.6596 | -0.2661 | 0.0199 | 174.6 | 0.4989 | 41.38 | 0.9769 |

**Diagnostics:** 
- Bars: 8737 | Long: 0.5% | Short: 40.7% | Flat: 58.8% | Flips: 172

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1892 | -0.5042 | 0.3914 | -1.5963 | -2.3017 | -0.3629 | -1.3894 | -0.0108 |
| low_vol | 0.0436 | 0.0630 | 0.2117 | 0.3945 | 0.6058 | -0.2258 | 0.2791 | -0.0057 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-12-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1539 | -0.1544 | 0.2781 | 0.1888 | -0.4636 | -0.6831 | -0.3884 | -0.3975 | -0.0041 | -0.0075 | 0.2765 | 0.9961 | -0.0544 | -0.0546 | -0.0995 | 0.6596 | -0.2661 | 0.0199 | 174.6 | 0.4989 | 41.38 | 0.9769 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1892 | -0.5042 | -1.5963 | -2.3017 | -0.3629 | -1.3894 | -0.0108 |
| low_vol | 0.0436 | 0.0630 | 0.3945 | 0.6058 | -0.2258 | 0.2791 | -0.0057 |

*Bars: 8737 | Long: 0.5% | Short: 40.7% | Flat: 58.8% | Flips: 172*

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
