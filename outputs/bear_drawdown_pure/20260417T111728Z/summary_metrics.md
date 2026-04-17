# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.2196 | 10.21 | 0.3669 | 0.1999 | 6.7693 | 12.43 | -0.0688 | 148.3 | -0.0055 | -0.0085 | 0.0246 | 0.9069 | -0.2364 | -0.9625 | 0.4560 | 0.8228 | 6.8428 | 0.0208 | 182.6 | 0.5366 | 35.88 | 1.3704 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 40.0% | Flat: 60.0% | Flips: 15

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1697 | 578.6 | 0.4987 | 13.01 | 26.47 | -0.0387 | 1.497e+04 | -0.0101 |
| low_vol | 0.0426 | 1.0656 | 0.2909 | 2.6388 | 4.3470 | -0.0498 | 21.42 | -0.0075 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-10-27 → 2025-11-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.2196 | 10.21 | 0.3669 | 0.1999 | 6.7693 | 12.43 | -0.0688 | 148.3 | -0.0055 | -0.0085 | 0.0246 | 0.9069 | -0.2364 | -0.9625 | 0.4560 | 0.8228 | 6.8428 | 0.0208 | 182.6 | 0.5366 | 35.88 | 1.3704 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1697 | 578.6 | 13.01 | 26.47 | -0.0387 | 1.497e+04 | -0.0101 |
| low_vol | 0.0426 | 1.0656 | 2.6388 | 4.3470 | -0.0498 | 21.42 | -0.0075 |

*Bars: 720 | Long: 0.0% | Short: 40.0% | Flat: 60.0% | Flips: 15*

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
