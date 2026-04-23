# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.3077 | 0.3089 | 0.3230 | 0.2054 | 0.9948 | 1.5644 | -0.2627 | 1.1758 | -0.0046 | -0.0082 | 0.1318 | 0.9935 | -0.0544 | -0.0546 | 0.3621 | 0.7151 | 0.3842 | 0.0228 | 199.7 | 0.4998 | 46.55 | 1.0455 |

**Diagnostics:** 
- Bars: 8737 | Long: 0.8% | Short: 51.9% | Flat: 47.2% | Flips: 194

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1480 | 0.5864 | 0.4672 | 1.2211 | 1.9283 | -0.1779 | 3.2964 | -0.0121 |
| low_vol | 0.1392 | 0.2054 | 0.2356 | 0.9107 | 1.4401 | -0.1321 | 1.5548 | -0.0062 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-01-01 → 2025-12-31

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.3077 | 0.3089 | 0.3230 | 0.2054 | 0.9948 | 1.5644 | -0.2627 | 1.1758 | -0.0046 | -0.0082 | 0.1318 | 0.9935 | -0.0544 | -0.0546 | 0.3621 | 0.7151 | 0.3842 | 0.0228 | 199.7 | 0.4998 | 46.55 | 1.0455 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1480 | 0.5864 | 1.2211 | 1.9283 | -0.1779 | 3.2964 | -0.0121 |
| low_vol | 0.1392 | 0.2054 | 0.9107 | 1.4401 | -0.1321 | 1.5548 | -0.0062 |

*Bars: 8737 | Long: 0.8% | Short: 51.9% | Flat: 47.2% | Flips: 194*

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
