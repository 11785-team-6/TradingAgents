# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.2184 | 10.07 | 0.4481 | 0.2412 | 5.5895 | 10.39 | -0.0674 | 149.5 | -0.0054 | -0.0097 | 0.0189 | 0.9556 | -0.0920 | -0.6910 | 0.3103 | 1.0343 | 3.3309 | 0.0264 | 231.3 | 0.4925 | 33.5 | 1.3037 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 18

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1231 | 110.3 | 0.6823 | 7.2465 | 13.62 | -0.0674 | 1637 | -0.0153 |
| low_vol | 0.0848 | 3.1202 | 0.2949 | 4.9489 | 9.2067 | -0.0400 | 77.97 | -0.0064 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.2184 | 10.07 | 0.4481 | 0.2412 | 5.5895 | 10.39 | -0.0674 | 149.5 | -0.0054 | -0.0097 | 0.0189 | 0.9556 | -0.0920 | -0.6910 | 0.3103 | 1.0343 | 3.3309 | 0.0264 | 231.3 | 0.4925 | 33.5 | 1.3037 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1231 | 110.3 | 7.2465 | 13.62 | -0.0674 | 1637 | -0.0153 |
| low_vol | 0.0848 | 3.1202 | 4.9489 | 9.2067 | -0.0400 | 77.97 | -0.0064 |

*Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 18*

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
