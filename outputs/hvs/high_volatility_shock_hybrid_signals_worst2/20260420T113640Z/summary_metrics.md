# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.0417 | 0.6438 | 0.5187 | 0.3135 | 1.2161 | 2.0118 | -0.1090 | 5.9052 | -0.0065 | -0.0124 | 0.0486 | 0.9681 | -0.0920 | -0.6910 | 0.1336 | 1.1284 | 1.3922 | 0.0181 | 158.3 | 0.4657 | 47.86 | 1.0638 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 12

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0366 | 3.3067 | 0.7786 | 2.2616 | 3.9031 | -0.0878 | 37.67 | -0.0188 |
| low_vol | 0.0049 | 0.0879 | 0.3527 | 0.4152 | 0.6429 | -0.0889 | 0.9887 | -0.0088 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.0417 | 0.6438 | 0.5187 | 0.3135 | 1.2161 | 2.0118 | -0.1090 | 5.9052 | -0.0065 | -0.0124 | 0.0486 | 0.9681 | -0.0920 | -0.6910 | 0.1336 | 1.1284 | 1.3922 | 0.0181 | 158.3 | 0.4657 | 47.86 | 1.0638 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0366 | 3.3067 | 2.2616 | 3.9031 | -0.0878 | 37.67 | -0.0188 |
| low_vol | 0.0049 | 0.0879 | 0.4152 | 0.6429 | -0.0889 | 0.9887 | -0.0088 |

*Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 12*

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
