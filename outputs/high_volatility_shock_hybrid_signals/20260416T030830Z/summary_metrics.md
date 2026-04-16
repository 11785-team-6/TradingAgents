# Agent Pilot — Summary Metrics

Same metric pipeline as deep-trading forecasting baselines (`summary_metrics`).

---

## 1. Aggregate (All Pilot Windows)

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent | 0.3107 | 25.94 | 0.5174 | 0.2721 | 6.6229 | 12.59 | -0.0749 | 346.4 | -0.0060 | -0.0113 | 0.0380 | 0.9319 | -0.0920 | -0.6910 | 0.4026 | 1.1276 | 3.8729 | 0.0167 | 146.1 | 0.5179 | 56 | 1.3894 |

**Diagnostics:** 
- Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 11

### 1.1 Regime Metrics (Aggregate)

| regime | cumulative_return | annualized_return | annualized_volatility | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1649 | 489.3 | 0.8039 | 8.1061 | 16.3 | -0.0626 | 7821 | -0.0170 |
| low_vol | 0.1251 | 6.7708 | 0.3238 | 6.4940 | 11.34 | -0.0646 | 104.8 | -0.0075 |

---

## 2. Per-Window Metrics

### 2.1 Window 0: 2025-02-24 → 2025-03-25

| strategy | cumulative_return | annualized_return | annualized_volatility | downside_volatility_annualized | sharpe | sortino | max_drawdown | calmar | var_95 | cvar_95 | ulcer_index | time_under_water_ratio | benchmark_cumulative_return | benchmark_annualized_return | excess_cumulative_return | tracking_error_annualized | information_ratio | turnover_mean | turnover_annualized | hit_rate | avg_holding_bars | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trading_agent (w0) | 0.3107 | 25.94 | 0.5174 | 0.2721 | 6.6229 | 12.59 | -0.0749 | 346.4 | -0.0060 | -0.0113 | 0.0380 | 0.9319 | -0.0920 | -0.6910 | 0.4026 | 1.1276 | 3.8729 | 0.0167 | 146.1 | 0.5179 | 56 | 1.3894 |

| regime | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | cvar_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_vol | 0.1649 | 489.3 | 8.1061 | 16.3 | -0.0626 | 7821 | -0.0170 |
| low_vol | 0.1251 | 6.7708 | 6.4940 | 11.34 | -0.0646 | 104.8 | -0.0075 |

*Bars: 720 | Long: 0.0% | Short: 46.7% | Flat: 53.3% | Flips: 11*

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
