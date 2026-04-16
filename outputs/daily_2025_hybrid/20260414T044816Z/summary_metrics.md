# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.0373 | 0.5397 | 0.2869 | 0.1938 | 1.6478 | 2.4400 | -0.0635 | 8.5059 | -0.0038 | -0.0073 | 0.0362 | 0.9758 | 0.0954 | 1.9273 | -0.0581 | 0.7283 | -1.0197 | 0.0188 | 165 | 0.4936 | 44.57 | 1.0864 |

**Diagnostics:** 
- Bars: 744 | Long: 0.0% | Short: 41.9% | Flat: 58.1% | Flips: 13

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0510 | -0.8722 | 0.3382 | -5.9132 | -7.4993 | -0.0635 | -13.74 | -0.0099 |
| low_vol | 0.0931 | 3.4684 | 0.2612 | 5.8633 | 10.08 | -0.0382 | 90.72 | -0.0060 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-01-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.0373 | 0.5397 | 0.2869 | 0.1938 | 1.6478 | 2.4400 | -0.0635 | 8.5059 | -0.0038 | -0.0073 | 0.0362 | 0.9758 | 0.0954 | 1.9273 | -0.0581 | 0.7283 | -1.0197 | 0.0188 | 165 | 0.4936 | 44.57 | 1.0864 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0510 | -0.8722 | -5.9132 | -7.4993 | -0.0635 | -13.74 | -0.0099 |
| low_vol | 0.0931 | 3.4684 | 5.8633 | 10.08 | -0.0382 | 90.72 | -0.0060 |

*Bars: 744 | Long: 0.0% | Short: 41.9% | Flat: 58.1% | Flips: 13*

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
