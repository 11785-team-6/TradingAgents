# Agent vs Forecasting Models — Same-Calendar Comparison

**Evaluation period:** 31 calendar days (dense span from first to last signal date: 2025-01-01 → 2025-01-31), aligned with ``run_eval`` forward-fill.

Forecast strategies are sliced to the **same hourly bars** on those dates; agent aggregate metrics come from `agent_metrics.json` (produced by `run_eval`).

---

## Aggregate comparison (agent vs baselines on signal dates)

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **trading_agent** | -0.1040 | -0.7259 | -3.1808 | -4.7797 | -0.1464 | -4.9596 | -0.1995 | -2.8610 | 0.4703 | 0.8817 |
| arima_garch | -0.1348 | -0.8184 | -2.9393 | -4.5328 | -0.1689 | -4.8451 | -0.2302 | -2.6584 | 0.4677 | 0.9076 |
| buy_and_hold | 0.0954 | 1.9273 | 2.2839 | 3.7239 | -0.1101 | 17.51 | 0.0000 | 0.0000 | 0.5255 | 1.0783 |
| lstm | 0.0124 | 0.1557 | 0.5377 | 0.8579 | -0.1185 | 1.3142 | -0.0831 | -1.8041 | 0.4987 | 1.0179 |
| macd | -0.1371 | -0.8241 | -2.9983 | -4.3215 | -0.2326 | -3.5428 | -0.2326 | -3.5573 | 0.4919 | 0.9058 |
| sma_cross | -0.1551 | -0.8628 | -3.4675 | -5.3249 | -0.2023 | -4.2656 | -0.2506 | -4.8804 | 0.4825 | 0.8919 |
| xgb_lstm_ensemble | 0.1793 | 5.9774 | 3.9181 | 6.5907 | -0.1320 | 45.27 | 0.0838 | 2.5744 | 0.5228 | 1.1380 |
| xgboost | 0.1900 | 6.7675 | 4.1202 | 6.9480 | -0.1373 | 49.29 | 0.0946 | 2.8814 | 0.5242 | 1.1456 |

---

## Benchmark reference

- **Buy-and-hold (signal dates):** cumulative return = 0.0954
