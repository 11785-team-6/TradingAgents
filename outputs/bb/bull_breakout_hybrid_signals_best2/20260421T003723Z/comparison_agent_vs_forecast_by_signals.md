# Agent vs Forecasting Models — Same-Calendar Comparison

**Evaluation period:** 30 calendar days (dense span from first to last signal date: 2025-04-09 → 2025-05-08), aligned with ``run_eval`` forward-fill.

Forecast strategies are sliced to the **same hourly bars** on those dates; agent aggregate metrics come from `agent_metrics.json` (produced by `run_eval`).

---

## Aggregate comparison (agent vs baselines on signal dates)

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **trading_agent** | -0.1035 | -0.7354 | -5.2891 | -7.4851 | -0.1411 | -5.2122 | -0.4497 | -8.2149 | 0.4599 | 0.7582 |
| arima_garch | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.3463 | -8.4711 | 0.0000 | 0.0000 |
| buy_and_hold | 0.3463 | 36.34 | 8.4711 | 15.5 | -0.0544 | 668.3 | 0.0000 | 0.0000 | 0.5375 | 1.3297 |
| lstm | 0.2960 | 22.49 | 7.8850 | 14.5 | -0.0441 | 509.4 | -0.0503 | -3.0770 | 0.5350 | 1.3395 |
| macd | 0.0862 | 1.7367 | 2.5051 | 4.7205 | -0.0862 | 20.16 | -0.2601 | -4.9620 | 0.4833 | 1.0877 |
| sma_cross | 0.1075 | 2.4680 | 3.0462 | 4.3522 | -0.1212 | 20.36 | -0.2387 | -4.8758 | 0.5514 | 1.1076 |
| xgb_lstm_ensemble | -0.0242 | -0.2583 | -2.1655 | -2.9973 | -0.0626 | -4.1278 | -0.3705 | -9.0061 | 0.4776 | 0.7971 |
| xgboost | -0.0349 | -0.3512 | -2.9302 | -3.5995 | -0.0583 | -6.0213 | -0.3812 | -8.5212 | 0.5114 | 0.7546 |

---

## Benchmark reference

- **Buy-and-hold (signal dates):** cumulative return = 0.3463
