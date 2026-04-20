# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1804 | 6.5294 | 0.5536 | 0.3359 | 3.9230 | 6.4661 | -0.2208 | 29.57 | -0.0074 | -0.0134 | 0.0909 | 0.9597 | -0.0920 | -0.6910 | 0.2723 | 1.1775 | 2.6430 | 0.0194 | 170.4 | 0.5219 | 65.14 | 1.1756 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 63.3% | Flat: 36.7% | Flips: 13

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0023 | -0.0882 | 0.8113 | 0.2904 | 0.4727 | -0.1643 | -0.5370 | -0.0204 |
| low_vol | 0.1830 | 17.61 | 0.3943 | 7.6125 | 13.46 | -0.0816 | 215.8 | -0.0085 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1804 | 6.5294 | 0.5536 | 0.3359 | 3.9230 | 6.4661 | -0.2208 | 29.57 | -0.0074 | -0.0134 | 0.0909 | 0.9597 | -0.0920 | -0.6910 | 0.2723 | 1.1775 | 2.6430 | 0.0194 | 170.4 | 0.5219 | 65.14 | 1.1756 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0023 | -0.0882 | 0.2904 | 0.4727 | -0.1643 | -0.5370 | -0.0204 |
| low_vol | 0.1830 | 17.61 | 7.6125 | 13.46 | -0.0816 | 215.8 | -0.0085 |

*Bars: 720 | Long: 0.0% | Short: 63.3% | Flat: 36.7% | Flips: 13*

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
