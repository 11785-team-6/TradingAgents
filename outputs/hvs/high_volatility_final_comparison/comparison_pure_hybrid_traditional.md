# Agent vs Forecasting Models - Same-Calendar Comparison

**Evaluation period:** 30 calendar days (dense span from first to last signal date: 2025-02-24 -> 2025-03-25), aligned with  forward-fill.

Forecast strategies are sliced to the **same hourly bars** on those dates; agent aggregate metrics come from  (produced by ).

---

## Aggregate comparison (agent vs baselines on signal dates)

| strategy | selected models | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LLM Pure | - | -0.0024 | -0.0290 | 0.2573 | 0.4243 | -0.1525 | -0.1902 | 0.0895 | 0.8696 | 0.4712 | 1.0107 |
| LLM Hybrid (metrics) | - | 0.2184 | 10.0750 | 5.5895 | 10.3853 | -0.0674 | 149.5383 | 0.3103 | 3.3309 | 0.4925 | 1.3037 |
| LLM Hybrid (signals) | - | 0.0970 | 2.0875 | 2.4084 | 4.1437 | -0.1434 | 14.5587 | 0.1890 | 1.9386 | 0.4833 | 1.1112 |
| hybrid_metrics(best2) | macd, xgb_lstm_ensemble | 0.1561 | 4.8460 | 3.5512 | 6.4138 | -0.0996 | 48.6675 | 0.2480 | 2.4696 | 0.4708 | 1.1868 |
| hybrid_signals(best2) | macd, xgb_lstm_ensemble | 0.1111 | 2.6057 | 3.2228 | 5.7652 | -0.0727 | 35.8303 | 0.2030 | 2.3006 | 0.4599 | 1.1874 |
| hybrid_metrics(mid3) | arima_garch, lstm, xgboost | -0.1328 | -0.8235 | -3.5440 | -4.4783 | -0.2100 | -3.9209 | -0.0408 | -0.7414 | 0.4917 | 0.8141 |
| hybrid_signals(mid3) | arima_garch, lstm, xgboost | 0.0777 | 1.4863 | 2.0296 | 3.2970 | -0.1498 | 9.9202 | 0.1696 | 1.8625 | 0.5083 | 1.1346 |
| hybrid_metrics(worst2) | buy_and_hold, sma_cross | 0.1804 | 6.5294 | 3.9230 | 6.4661 | -0.2208 | 29.5664 | 0.2723 | 2.6430 | 0.5219 | 1.1756 |
| hybrid_signals(worst2) | buy_and_hold, sma_cross | 0.0417 | 0.6438 | 1.2161 | 2.0118 | -0.1090 | 5.9052 | 0.1336 | 1.3922 | 0.4657 | 1.0638 |
| arima_garch | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0920 | 1.3768 | 0.0000 | 0.0000 |
| buy_and_hold | - | -0.0920 | -0.6910 | -1.3768 | -2.0395 | -0.1939 | -3.5636 | 0.0000 | 0.0000 | 0.5153 | 0.9553 |
| lstm | - | -0.0123 | -0.1399 | -0.4364 | -0.6478 | -0.1000 | -1.3995 | 0.0796 | 1.2109 | 0.5000 | 0.9779 |
| macd | - | 0.2379 | 12.4365 | 4.1479 | 7.5550 | -0.1188 | 104.7238 | 0.3298 | 3.4904 | 0.4958 | 1.1477 |
| sma_cross | - | -0.2479 | -0.9688 | -4.7398 | -6.6084 | -0.4063 | -2.3843 | -0.1559 | -2.2388 | 0.4986 | 0.8543 |
| xgb_lstm_ensemble | - | 0.0012 | 0.0144 | 0.1788 | 0.2515 | -0.0594 | 0.2433 | 0.0931 | 1.4755 | 0.4952 | 1.0139 |
| xgboost | - | -0.0227 | -0.2437 | -1.3090 | -1.6769 | -0.0623 | -3.9098 | 0.0693 | 1.0200 | 0.4828 | 0.8956 |

---

## Benchmark reference
- **Buy-and-hold (signal dates):** cumulative return = -0.0920

## Source files
- : 
- : 
- : 
