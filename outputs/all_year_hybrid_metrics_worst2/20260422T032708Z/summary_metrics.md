# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | -0.2690 | -0.2697 | 0.3406 | 0.2228 | -0.7526 | -1.1507 | -0.3306 | -0.8158 | -0.0051 | -0.0090 | 0.2053 | 0.9962 | -0.0544 | -0.0546 | -0.2146 | 0.7386 | -0.4101 | 0.0211 | 184.6 | 0.4920 | 52.7 | 0.9674 |

**Diagnostics:** 
- Bars: 8737 | Long: 1.6% | Short: 53.8% | Flat: 44.5% | Flips: 175

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.2881 | -0.6791 | 0.4964 | -2.0413 | -3.1388 | -0.3303 | -2.0561 | -0.0131 |
| low_vol | 0.0269 | 0.0388 | 0.2451 | 0.2776 | 0.4303 | -0.1831 | 0.2117 | -0.0066 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-12-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | -0.2690 | -0.2697 | 0.3406 | 0.2228 | -0.7526 | -1.1507 | -0.3306 | -0.8158 | -0.0051 | -0.0090 | 0.2053 | 0.9962 | -0.0544 | -0.0546 | -0.2146 | 0.7386 | -0.4101 | 0.0211 | 184.6 | 0.4920 | 52.7 | 0.9674 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | -0.2881 | -0.6791 | -2.0413 | -3.1388 | -0.3303 | -2.0561 | -0.0131 |
| low_vol | 0.0269 | 0.0388 | 0.2776 | 0.4303 | -0.1831 | 0.2117 | -0.0066 |

*Bars: 8737 | Long: 1.6% | Short: 53.8% | Flat: 44.5% | Flips: 175*

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
