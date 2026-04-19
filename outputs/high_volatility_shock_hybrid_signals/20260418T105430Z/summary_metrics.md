# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.0970 | 2.0875 | 0.5251 | 0.3052 | 2.4084 | 4.1437 | -0.1434 | 14.56 | -0.0075 | -0.0129 | 0.0761 | 0.9486 | -0.0920 | -0.6910 | 0.1890 | 1.1373 | 1.9386 | 0.0167 | 146.1 | 0.4833 | 60 | 1.1112 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 50.0% | Flat: 50.0% | Flips: 11

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0795 | 21.27 | 0.8090 | 4.2385 | 7.7354 | -0.0828 | 256.8 | -0.0184 |
| low_vol | 0.0163 | 0.3239 | 0.3362 | 1.0024 | 1.6223 | -0.1108 | 2.9238 | -0.0083 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.0970 | 2.0875 | 0.5251 | 0.3052 | 2.4084 | 4.1437 | -0.1434 | 14.56 | -0.0075 | -0.0129 | 0.0761 | 0.9486 | -0.0920 | -0.6910 | 0.1890 | 1.1373 | 1.9386 | 0.0167 | 146.1 | 0.4833 | 60 | 1.1112 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.0795 | 21.27 | 4.2385 | 7.7354 | -0.0828 | 256.8 | -0.0184 |
| low_vol | 0.0163 | 0.3239 | 1.0024 | 1.6223 | -0.1108 | 2.9238 | -0.0083 |

*Bars: 720 | Long: 0.0% | Short: 50.0% | Flat: 50.0% | Flips: 11*

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
