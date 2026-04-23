# Agent vs Forecasting Models - Same-Calendar Comparison

**Evaluation period:** 30 calendar days (dense span from first to last signal date: 2025-04-09 -> 2025-05-08), aligned with  forward-fill.

Forecast strategies are sliced to the **same hourly bars** on those dates; agent aggregate metrics come from  (produced by ).

---

## Aggregate comparison (agent vs baselines on signal dates)

| strategy | selected models | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LLM Pure | - | -0.0866 | -0.6679 | -3.8199 | -6.2293 | -0.1255 | -5.3202 | -0.4328 | -7.4092 | 0.4308 | 0.8478 |
| LLM Hybrid (metrics) | - | 0.0775 | 1.4807 | 4.4690 | 8.2895 | -0.0275 | 53.7763 | -0.2688 | -4.8997 | 0.5152 | 1.2707 |
| LLM Hybrid (signals) | - | -0.2197 | -0.9512 | -10.5882 | -14.4745 | -0.2197 | -4.3294 | -0.5660 | -10.2166 | 0.4345 | 0.6332 |
| hybrid_metrics(best2) | buy_and_hold, lstm | -0.1771 | -0.9068 | -6.7126 | -8.5417 | -0.1911 | -4.7452 | -0.5234 | -8.1457 | 0.4687 | 0.7045 |
| hybrid_signals(best2) | buy_and_hold, lstm | -0.1035 | -0.7354 | -5.2891 | -7.4851 | -0.1411 | -5.2122 | -0.4497 | -8.2149 | 0.4599 | 0.7582 |
| hybrid_metrics(mid3) | sma_cross, macd, arima_garch | -0.1627 | -0.8849 | -7.9454 | -11.0763 | -0.1715 | -5.1592 | -0.5090 | -9.1637 | 0.4484 | 0.7416 |
| hybrid_signals(mid3) | sma_cross, macd, arima_garch | -0.0642 | -0.5540 | -2.3823 | -3.1511 | -0.1004 | -5.5167 | -0.4104 | -6.3605 | 0.4792 | 0.8595 |
| hybrid_metrics(worst2) | xgb_lstm_ensemble, xgboost | -0.1943 | -0.9280 | -7.2237 | -9.3069 | -0.2081 | -4.4604 | -0.5406 | -8.3181 | 0.4763 | 0.6904 |
| hybrid_signals(worst2) | xgb_lstm_ensemble, xgboost | -0.0737 | -0.6065 | -3.3092 | -5.0917 | -0.1182 | -5.1316 | -0.4200 | -7.1876 | 0.4615 | 0.8499 |
| arima_garch | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.3463 | -8.4711 | 0.0000 | 0.0000 |
| buy_and_hold | - | 0.3463 | 36.3418 | 8.4711 | 15.4995 | -0.0544 | 668.3160 | 0.0000 | 0.0000 | 0.5375 | 1.3297 |
| lstm | - | 0.2960 | 22.4866 | 7.8850 | 14.5039 | -0.0441 | 509.4107 | -0.0503 | -3.0770 | 0.5350 | 1.3395 |
| macd | - | 0.0862 | 1.7367 | 2.5051 | 4.7205 | -0.0862 | 20.1554 | -0.2601 | -4.9620 | 0.4833 | 1.0877 |
| sma_cross | - | 0.1075 | 2.4680 | 3.0462 | 4.3522 | -0.1212 | 20.3618 | -0.2387 | -4.8758 | 0.5514 | 1.1076 |
| xgb_lstm_ensemble | - | -0.0242 | -0.2583 | -2.1655 | -2.9973 | -0.0626 | -4.1278 | -0.3705 | -9.0061 | 0.4776 | 0.7971 |
| xgboost | - | -0.0349 | -0.3512 | -2.9302 | -3.5995 | -0.0583 | -6.0213 | -0.3812 | -8.5212 | 0.5114 | 0.7546 |

---

## Benchmark reference
- **Buy-and-hold (signal dates):** cumulative return = 0.3463

## Source files
- : 
- : 
- : 
