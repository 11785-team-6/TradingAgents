# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.1474 | 0.1479 | 0.3085 | 0.1962 | 0.6011 | 0.9451 | -0.2403 | 0.6155 | -0.0044 | -0.0078 | 0.1481 | 0.9895 | -0.0544 | -0.0546 | 0.2018 | 0.6833 | 0.2033 | 0.0227 | 198.7 | 0.5048 | 42.18 | 1.0291 |

**Diagnostics:** 
- Bars: 8737 | Long: 3.6% | Short: 44.2% | Flat: 52.2% | Flips: 187

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0486 | -0.1534 | 0.4502 | -0.1453 | -0.2310 | -0.2454 | -0.6251 | -0.0115 |
| low_vol | 0.2060 | 0.3079 | 0.2215 | 1.3224 | 2.0697 | -0.1144 | 2.6921 | -0.0058 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-12-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.1474 | 0.1479 | 0.3085 | 0.1962 | 0.6011 | 0.9451 | -0.2403 | 0.6155 | -0.0044 | -0.0078 | 0.1481 | 0.9895 | -0.0544 | -0.0546 | 0.2018 | 0.6833 | 0.2033 | 0.0227 | 198.7 | 0.5048 | 42.18 | 1.0291 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.0486 | -0.1534 | -0.1453 | -0.2310 | -0.2454 | -0.6251 | -0.0115 |
| low_vol | 0.2060 | 0.3079 | 1.3224 | 2.0697 | -0.1144 | 2.6921 | -0.0058 |

*Bars: 8737 | Long: 3.6% | Short: 44.2% | Flat: 52.2% | Flips: 187*

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
