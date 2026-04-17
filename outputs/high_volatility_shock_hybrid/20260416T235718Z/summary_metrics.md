# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1053 | 2.3851 | 0.3425 | 0.1793 | 3.7299 | 7.1270 | -0.0561 | 42.53 | -0.0040 | -0.0074 | 0.0317 | 0.8667 | -0.0920 | -0.6910 | 0.1973 | 0.8785 | 2.5246 | 0.0194 | 170.4 | 0.4875 | 34.29 | 1.2509 |

**Diagnostics:** 
- Bars: 720 | Long: 3.3% | Short: 30.0% | Flat: 66.7% | Flips: 14

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0700 | 14.59 | 0.4597 | 6.2016 | 14.36 | -0.0235 | 620.9 | -0.0081 |
| low_vol | 0.0330 | 0.7592 | 0.2772 | 2.1761 | 3.5484 | -0.0561 | 13.54 | -0.0069 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1053 | 2.3851 | 0.3425 | 0.1793 | 3.7299 | 7.1270 | -0.0561 | 42.53 | -0.0040 | -0.0074 | 0.0317 | 0.8667 | -0.0920 | -0.6910 | 0.1973 | 0.8785 | 2.5246 | 0.0194 | 170.4 | 0.4875 | 34.29 | 1.2509 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0700 | 14.59 | 6.2016 | 14.36 | -0.0235 | 620.9 | -0.0081 |
| low_vol | 0.0330 | 0.7592 | 2.1761 | 3.5484 | -0.0561 | 13.54 | -0.0069 |

*Bars: 720 | Long: 3.3% | Short: 30.0% | Flat: 66.7% | Flips: 14*

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
