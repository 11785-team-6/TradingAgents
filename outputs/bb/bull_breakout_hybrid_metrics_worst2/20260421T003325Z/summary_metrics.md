# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1943 | -0.9280 | 0.3553 | 0.2758 | -7.2237 | -9.3069 | -0.2081 | -4.4604 | -0.0049 | -0.0104 | 0.1243 | 0.9944 | 0.3463 | 36.34 | -0.5406 | 0.7554 | -8.3181 | 0.0208 | 182.6 | 0.4763 | 44.88 | 0.6904 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 50.0% | Flat: 50.0% | Flips: 14

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0781 | -0.9631 | 0.5364 | -5.8765 | -7.5880 | -0.1108 | -8.6950 | -0.0159 |
| low_vol | -0.1261 | -0.9041 | 0.2388 | -9.6975 | -12.55 | -0.1261 | -7.1685 | -0.0074 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1943 | -0.9280 | 0.3553 | 0.2758 | -7.2237 | -9.3069 | -0.2081 | -4.4604 | -0.0049 | -0.0104 | 0.1243 | 0.9944 | 0.3463 | 36.34 | -0.5406 | 0.7554 | -8.3181 | 0.0208 | 182.6 | 0.4763 | 44.88 | 0.6904 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0781 | -0.9631 | -5.8765 | -7.5880 | -0.1108 | -8.6950 | -0.0159 |
| low_vol | -0.1261 | -0.9041 | -9.6975 | -12.55 | -0.1261 | -7.1685 | -0.0074 |

*Bars: 720 | Long: 0.0% | Short: 50.0% | Flat: 50.0% | Flips: 14*

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
