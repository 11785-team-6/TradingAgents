# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.0866 | -0.6679 | 0.2785 | 0.1708 | -3.8199 | -6.2293 | -0.1255 | -5.3202 | -0.0046 | -0.0071 | 0.0494 | 0.9583 | 0.3463 | 36.34 | -0.4328 | 0.6452 | -7.4092 | 0.0236 | 207 | 0.4308 | 42.56 | 0.8478 |

**Diagnostics:** 
- Bars: 720 | Long: 3.3% | Short: 50.0% | Flat: 46.7% | Flips: 15

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0093 | 0.4587 | 0.3485 | 1.2562 | 2.6221 | -0.0337 | 13.6 | -0.0069 |
| low_vol | -0.0950 | -0.8239 | 0.2420 | -7.0537 | -9.9053 | -0.1057 | -7.7974 | -0.0071 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-04-09 → 2025-05-08

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.0866 | -0.6679 | 0.2785 | 0.1708 | -3.8199 | -6.2293 | -0.1255 | -5.3202 | -0.0046 | -0.0071 | 0.0494 | 0.9583 | 0.3463 | 36.34 | -0.4328 | 0.6452 | -7.4092 | 0.0236 | 207 | 0.4308 | 42.56 | 0.8478 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0093 | 0.4587 | 1.2562 | 2.6221 | -0.0337 | 13.6 | -0.0069 |
| low_vol | -0.0950 | -0.8239 | -7.0537 | -9.9053 | -0.1057 | -7.7974 | -0.0071 |

*Bars: 720 | Long: 3.3% | Short: 50.0% | Flat: 46.7% | Flips: 15*

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
