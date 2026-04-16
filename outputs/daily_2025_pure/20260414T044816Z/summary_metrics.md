# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1040 | -0.7259 | 0.3837 | 0.2554 | -3.1808 | -4.7797 | -0.1464 | -4.9596 | -0.0057 | -0.0104 | 0.0891 | 0.9261 | 0.0954 | 1.9273 | -0.1995 | 0.8515 | -2.8610 | 0.0228 | 200.3 | 0.4703 | 50.56 | 0.8817 |

**Diagnostics:** 
- Bars: 744 | Long: 0.0% | Short: 61.3% | Flat: 38.7% | Flips: 17

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0717 | -0.9464 | 0.5207 | -5.3569 | -8.2255 | -0.0992 | -9.5378 | -0.0139 |
| low_vol | -0.0348 | -0.4490 | 0.3067 | -1.7903 | -2.6775 | -0.0761 | -5.9024 | -0.0084 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-01-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1040 | -0.7259 | 0.3837 | 0.2554 | -3.1808 | -4.7797 | -0.1464 | -4.9596 | -0.0057 | -0.0104 | 0.0891 | 0.9261 | 0.0954 | 1.9273 | -0.1995 | 0.8515 | -2.8610 | 0.0228 | 200.3 | 0.4703 | 50.56 | 0.8817 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0717 | -0.9464 | -5.3569 | -8.2255 | -0.0992 | -9.5378 | -0.0139 |
| low_vol | -0.0348 | -0.4490 | -1.7903 | -2.6775 | -0.0761 | -5.9024 | -0.0084 |

*Bars: 744 | Long: 0.0% | Short: 61.3% | Flat: 38.7% | Flips: 17*

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
