# Agent vs Forecasting Models — Same-Calendar Comparison

**Evaluation period:** 30 calendar days (dense span from first to last signal date: 2025-02-24 → 2025-03-25), aligned with ``run_eval`` forward-fill.

Forecast strategies are sliced to the **same hourly bars** on those dates; agent aggregate metrics come from `agent_metrics.json` (produced by `run_eval`).

---

## Aggregate comparison (agent vs baselines on signal dates)

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **trading_agent** | -0.1112 | -0.7620 | -2.8807 | -4.0155 | -0.2157 | -3.5330 | -0.0193 | -0.3701 | 0.4896 | 0.8731 |
| arima_garch | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0920 | 1.3768 | 0.0000 | 0.0000 |
| buy_and_hold | -0.0920 | -0.6910 | -1.3768 | -2.0395 | -0.1939 | -3.5636 | 0.0000 | 0.0000 | 0.5153 | 0.9553 |
| lstm | -0.0123 | -0.1399 | -0.4364 | -0.6478 | -0.1000 | -1.3995 | 0.0796 | 1.2109 | 0.5000 | 0.9779 |
| macd | 0.2379 | 12.44 | 4.1479 | 7.5550 | -0.1188 | 104.7 | 0.3298 | 3.4904 | 0.4958 | 1.1477 |
| sma_cross | -0.2479 | -0.9688 | -4.7398 | -6.6084 | -0.4063 | -2.3843 | -0.1559 | -2.2388 | 0.4986 | 0.8543 |
| xgb_lstm_ensemble | 0.0012 | 0.0144 | 0.1788 | 0.2515 | -0.0594 | 0.2433 | 0.0931 | 1.4755 | 0.4952 | 1.0139 |
| xgboost | -0.0227 | -0.2437 | -1.3090 | -1.6769 | -0.0623 | -3.9098 | 0.0693 | 1.0200 | 0.4828 | 0.8956 |

---

## Benchmark reference

- **Buy-and-hold (signal dates):** cumulative return = -0.0920
