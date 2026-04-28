# Agent vs Forecasting Models - Same-Calendar Comparison

**Evaluation period:** 30 calendar days (dense span from first to last signal date: 2025-10-27 -> 2025-11-25), aligned with  forward-fill.

Forecast strategies are sliced to the **same hourly bars** on those dates; agent aggregate metrics come from  (produced by ).

---

## Aggregate comparison (agent vs baselines on signal dates)

| strategy | selected models | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LLM Pure | - | 0.2586 | 15.4488 | 7.0681 | 12.3391 | -0.0688 | 224.4000 | 0.4950 | 6.8601 | 0.5506 | 1.3507 |
| LLM Hybrid (metrics) | - | 0.1006 | 2.2123 | 4.3832 | 7.7879 | -0.0590 | 37.4800 | 0.3370 | 6.1562 | 0.5093 | 1.2695 |
| LLM Hybrid (signals) | - | 0.1802 | 6.5159 | 5.8121 | 10.4573 | -0.0594 | 109.6310 | 0.4166 | 6.4464 | 0.5139 | 1.3225 |
| hybrid_metrics(best2) | lstm, sma_cross | 0.0208 | 0.2842 | 0.9931 | 1.5312 | -0.0693 | 4.1031 | 0.2572 | 4.6994 | 0.5156 | 1.0543 |
| hybrid_signals(best2) | lstm, sma_cross | 0.0428 | 0.6665 | 1.3938 | 2.3532 | -0.0944 | 7.0570 | 0.2793 | 4.0984 | 0.5031 | 1.0513 |
| hybrid_metrics(mid3) | arima_garch, xgboost, xgb_lstm_ensemble | 0.1999 | 8.1988 | 5.9111 | 10.4176 | -0.0795 | 103.1522 | 0.4363 | 6.3898 | 0.5061 | 1.2547 |
| hybrid_signals(mid3) | arima_garch, xgboost, xgb_lstm_ensemble | 0.1846 | 6.8662 | 6.0975 | 10.6176 | -0.0417 | 164.7713 | 0.4210 | 6.6039 | 0.5521 | 1.3187 |
| hybrid_metrics(worst2) | macd, buy_and_hold | 0.1294 | 3.4017 | 5.3908 | 9.3208 | -0.0437 | 77.8565 | 0.3659 | 6.5242 | 0.5209 | 1.3217 |
| hybrid_signals(worst2) | macd, buy_and_hold | 0.1610 | 5.1569 | 5.6869 | 9.6338 | -0.0413 | 124.9550 | 0.3974 | 6.4897 | 0.5312 | 1.2915 |
| arima_garch | - | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.2364 | 6.0169 | 0.0000 | 0.0000 |
| buy_and_hold | - | -0.2364 | -0.9625 | -6.0169 | -8.9417 | -0.2913 | -3.3047 | 0.0000 | 0.0000 | 0.4917 | 0.8388 |
| lstm | - | 0.2836 | 19.8953 | 7.0559 | 12.3209 | -0.0549 | 362.6469 | 0.5200 | 7.4088 | 0.5208 | 1.2756 |
| macd | - | -0.0677 | -0.5739 | -1.3665 | -2.3041 | -0.1302 | -4.4083 | 0.1687 | 3.0639 | 0.4861 | 0.9609 |
| sma_cross | - | 0.1087 | 2.5118 | 2.6598 | 4.7689 | -0.1221 | 20.5706 | 0.3451 | 4.6145 | 0.4972 | 1.0808 |
| xgb_lstm_ensemble | - | -0.0426 | -0.4116 | -2.2080 | -3.0219 | -0.0782 | -5.2640 | 0.1938 | 4.8985 | 0.4756 | 0.8264 |
| xgboost | - | -0.0412 | -0.4005 | -2.1895 | -3.0096 | -0.0653 | -6.1287 | 0.1953 | 5.0165 | 0.4247 | 0.8179 |

---

## Benchmark reference
- **Buy-and-hold (signal dates):** cumulative return = -0.2364

## Source files
- : 
- : 
- : 
