# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.0129 | 0.1689 | 0.3466 | 0.2206 | 0.6231 | 0.9793 | -0.1330 | 1.2702 | -0.0047 | -0.0093 | 0.0841 | 0.9403 | -0.0920 | -0.6910 | 0.1049 | 0.8381 | 1.3795 | 0.0194 | 170.4 | 0.4917 | 34.29 | 1.0354 |

**Diagnostics:** 
- Bars: 720 | Long: 3.3% | Short: 30.0% | Flat: 66.7% | Flips: 13

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0263 | 1.8629 | 0.4901 | 2.3904 | 3.8854 | -0.0683 | 27.28 | -0.0126 |
| low_vol | -0.0130 | -0.2037 | 0.2620 | -0.7386 | -1.1208 | -0.1077 | -1.8909 | -0.0068 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.0129 | 0.1689 | 0.3466 | 0.2206 | 0.6231 | 0.9793 | -0.1330 | 1.2702 | -0.0047 | -0.0093 | 0.0841 | 0.9403 | -0.0920 | -0.6910 | 0.1049 | 0.8381 | 1.3795 | 0.0194 | 170.4 | 0.4917 | 34.29 | 1.0354 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0263 | 1.8629 | 2.3904 | 3.8854 | -0.0683 | 27.28 | -0.0126 |
| low_vol | -0.0130 | -0.2037 | -0.7386 | -1.1208 | -0.1077 | -1.8909 | -0.0068 |

*Bars: 720 | Long: 3.3% | Short: 30.0% | Flat: 66.7% | Flips: 13*

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
