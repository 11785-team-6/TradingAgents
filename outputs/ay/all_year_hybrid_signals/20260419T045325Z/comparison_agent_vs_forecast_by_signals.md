# Agent vs Forecasting Models — Same-Calendar Comparison

**Evaluation period:** 365 calendar days (dense span from first to last signal date: 2025-01-01 → 2025-12-31), aligned with ``run_eval`` forward-fill.

Forecast strategies are sliced to the **same hourly bars** on those dates; agent aggregate metrics come from `agent_metrics.json` (produced by `run_eval`).

---

## Aggregate comparison (agent vs baselines on signal dates)

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **trading_agent** | 0.1474 | 0.1479 | 0.6011 | 0.9451 | -0.2403 | 0.6155 | 0.2018 | 0.2033 | 0.5048 | 1.0291 |
| arima_garch | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0544 | -0.1028 | 0.0000 | 0.0000 |
| buy_and_hold | -0.0544 | -0.0546 | 0.1028 | 0.1604 | -0.3475 | -0.1570 | 0.0000 | 0.0000 | 0.5064 | 1.0033 |
| lstm | 0.9257 | 0.9299 | 2.2430 | 3.5727 | -0.1870 | 4.9733 | 0.9801 | 1.3016 | 0.5053 | 1.0981 |
| macd | -0.3741 | -0.3750 | -0.8116 | -1.3338 | -0.4529 | -0.8281 | -0.3197 | -0.6304 | 0.4883 | 0.9739 |
| sma_cross | -0.4401 | -0.4412 | -1.0579 | -1.6294 | -0.5038 | -0.8757 | -0.3857 | -0.7784 | 0.4993 | 0.9662 |
| xgb_lstm_ensemble | 0.0493 | 0.0494 | 0.3700 | 0.5368 | -0.1297 | 0.3812 | 0.1036 | 0.0349 | 0.4996 | 1.0327 |
| xgboost | 0.0493 | 0.0494 | 0.3916 | 0.5617 | -0.0926 | 0.5336 | 0.1036 | 0.0290 | 0.5016 | 1.0375 |

---

## Benchmark reference

- **Buy-and-hold (signal dates):** cumulative return = -0.0544
