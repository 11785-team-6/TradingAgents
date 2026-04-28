# Agent vs Forecasting Models — Same-Calendar Comparison

**Evaluation period:** 30 calendar days (dense span from first to last signal date: 2025-10-27 → 2025-11-25), aligned with ``run_eval`` forward-fill.

Forecast strategies are sliced to the **same hourly bars** on those dates; agent aggregate metrics come from `agent_metrics.json` (produced by `run_eval`).

---

## Aggregate comparison (agent vs baselines on signal dates)

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **trading_agent** | 0.1802 | 6.5159 | 5.8121 | 10.46 | -0.0594 | 109.6 | 0.4166 | 6.4464 | 0.5139 | 1.3225 |
| arima_garch | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.2364 | 6.0169 | 0.0000 | 0.0000 |
| buy_and_hold | -0.2364 | -0.9625 | -6.0169 | -8.9417 | -0.2913 | -3.3047 | 0.0000 | 0.0000 | 0.4917 | 0.8388 |
| lstm | 0.2836 | 19.9 | 7.0559 | 12.32 | -0.0549 | 362.6 | 0.5200 | 7.4088 | 0.5208 | 1.2756 |
| macd | -0.0677 | -0.5739 | -1.3665 | -2.3041 | -0.1302 | -4.4083 | 0.1687 | 3.0639 | 0.4861 | 0.9609 |
| sma_cross | 0.1087 | 2.5118 | 2.6598 | 4.7689 | -0.1221 | 20.57 | 0.3451 | 4.6145 | 0.4972 | 1.0808 |
| xgb_lstm_ensemble | -0.0426 | -0.4116 | -2.2080 | -3.0219 | -0.0782 | -5.2640 | 0.1938 | 4.8985 | 0.4756 | 0.8264 |
| xgboost | -0.0412 | -0.4005 | -2.1895 | -3.0096 | -0.0653 | -6.1287 | 0.1953 | 5.0165 | 0.4247 | 0.8179 |

---

## Benchmark reference

- **Buy-and-hold (signal dates):** cumulative return = -0.2364
