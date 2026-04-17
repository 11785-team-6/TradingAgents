# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1631 | 5.2905 | 0.3448 | 0.1978 | 5.5066 | 9.5981 | -0.0444 | 119.1 | -0.0061 | -0.0084 | 0.0169 | 0.9181 | -0.2364 | -0.9625 | 0.3995 | 0.7934 | 6.3584 | 0.0208 | 182.6 | 0.5254 | 41.88 | 1.2631 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 15

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0492 | 6.0326 | 0.4090 | 4.9735 | 8.8725 | -0.0444 | 135.8 | -0.0095 |
| low_vol | 0.1085 | 4.9969 | 0.3132 | 5.8753 | 10.08 | -0.0408 | 122.5 | -0.0078 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1631 | 5.2905 | 0.3448 | 0.1978 | 5.5066 | 9.5981 | -0.0444 | 119.1 | -0.0061 | -0.0084 | 0.0169 | 0.9181 | -0.2364 | -0.9625 | 0.3995 | 0.7934 | 6.3584 | 0.0208 | 182.6 | 0.5254 | 41.88 | 1.2631 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0492 | 6.0326 | 4.9735 | 8.8725 | -0.0444 | 135.8 | -0.0095 |
| low_vol | 0.1085 | 4.9969 | 5.8753 | 10.08 | -0.0408 | 122.5 | -0.0078 |

*Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 15*

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
