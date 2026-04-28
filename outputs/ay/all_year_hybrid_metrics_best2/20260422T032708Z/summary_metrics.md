# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.1887 | -0.1892 | 0.3161 | 0.2140 | -0.5053 | -0.7464 | -0.3523 | -0.5372 | -0.0047 | -0.0085 | 0.2111 | 0.9992 | -0.0544 | -0.0546 | -0.1343 | 0.7076 | -0.2915 | 0.0216 | 189.6 | 0.4966 | 46.72 | 0.9771 |

**Diagnostics:** 
- Bars: 8737 | Long: 0.5% | Short: 49.7% | Flat: 49.7% | Flips: 186

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1732 | -0.4707 | 0.4564 | -1.1654 | -1.6972 | -0.2738 | -1.7195 | -0.0126 |
| low_vol | -0.0187 | -0.0266 | 0.2313 | -0.0011 | -0.0017 | -0.2142 | -0.1244 | -0.0063 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-12-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.1887 | -0.1892 | 0.3161 | 0.2140 | -0.5053 | -0.7464 | -0.3523 | -0.5372 | -0.0047 | -0.0085 | 0.2111 | 0.9992 | -0.0544 | -0.0546 | -0.1343 | 0.7076 | -0.2915 | 0.0216 | 189.6 | 0.4966 | 46.72 | 0.9771 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.1732 | -0.4707 | -1.1654 | -1.6972 | -0.2738 | -1.7195 | -0.0126 |
| low_vol | -0.0187 | -0.0266 | -0.0011 | -0.0017 | -0.2142 | -0.1244 | -0.0063 |

*Bars: 8737 | Long: 0.5% | Short: 49.7% | Flat: 49.7% | Flips: 186*

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
