# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1561 | 4.8460 | 0.5377 | 0.2977 | 3.5512 | 6.4138 | -0.0996 | 48.67 | -0.0074 | -0.0126 | 0.0536 | 0.9528 | -0.0920 | -0.6910 | 0.2480 | 1.1538 | 2.4696 | 0.0264 | 231.3 | 0.4708 | 35.9 | 1.1868 |

**Diagnostics:** 
- Bars: 720 | Long: 3.3% | Short: 46.7% | Flat: 50.0% | Flips: 17

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1123 | 74.12 | 0.8448 | 5.5319 | 10.49 | -0.0700 | 1059 | -0.0189 |
| low_vol | 0.0394 | 0.9571 | 0.3264 | 2.2202 | 3.7537 | -0.0588 | 16.29 | -0.0081 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1561 | 4.8460 | 0.5377 | 0.2977 | 3.5512 | 6.4138 | -0.0996 | 48.67 | -0.0074 | -0.0126 | 0.0536 | 0.9528 | -0.0920 | -0.6910 | 0.2480 | 1.1538 | 2.4696 | 0.0264 | 231.3 | 0.4708 | 35.9 | 1.1868 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1123 | 74.12 | 5.5319 | 10.49 | -0.0700 | 1059 | -0.0189 |
| low_vol | 0.0394 | 0.9571 | 2.2202 | 3.7537 | -0.0588 | 16.29 | -0.0081 |

*Bars: 720 | Long: 3.3% | Short: 46.7% | Flat: 50.0% | Flips: 17*

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
