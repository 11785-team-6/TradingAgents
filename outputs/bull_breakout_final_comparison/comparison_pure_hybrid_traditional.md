# Pure vs Hybrid vs Traditional — Combined Comparison

**Evaluation window:** 30 calendar days (dense span 2025-04-09 → 2025-05-08), from reference `signals.csv` in `/ocean/projects/cis260081p/chsu11/hybrid/TradingAgents/outputs/bull_breakout_pure/20260417T061729Z`.

LLM rows use `agent_metrics.json` (post–`run_eval`). Traditional rows are non-agent forecast baselines sliced to the **same** hourly bars on those dates.

---

## LLM agents vs traditional forecasts

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **LLM Pure** (bull_breakout_pure) | -0.2154 | -0.9479 | -7.1208 | -9.7226 | -0.2288 | -4.1432 | -0.5617 | -7.9906 | 0.4574 | 0.7548 |
| **LLM Hybrid (metrics)** (bull_breakout_hybrid) | -0.1471 | -0.8559 | -6.0034 | -7.3051 | -0.1925 | -4.4452 | -0.4934 | -8.0208 | 0.4508 | 0.7007 |
| **LLM Hybrid (signals)** (bull_breakout_hybrid_signals) | -0.0604 | -0.5314 | -3.3373 | -4.4939 | -0.0952 | -5.5802 | -0.4066 | -7.6662 | 0.4708 | 0.8280 |

## Traditional forecasting baselines (same dates)

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima_garch | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.3463 | -8.4711 | 0.0000 | 0.0000 |
| buy_and_hold | 0.3463 | 36.34 | 8.4711 | 15.5 | -0.0544 | 668.3 | 0.0000 | 0.0000 | 0.5375 | 1.3297 |
| lstm | 0.2960 | 22.49 | 7.8850 | 14.5 | -0.0441 | 509.4 | -0.0503 | -3.0770 | 0.5350 | 1.3395 |
| macd | 0.0862 | 1.7367 | 2.5051 | 4.7205 | -0.0862 | 20.16 | -0.2601 | -4.9620 | 0.4833 | 1.0877 |
| sma_cross | 0.1075 | 2.4680 | 3.0462 | 4.3522 | -0.1212 | 20.36 | -0.2387 | -4.8758 | 0.5514 | 1.1076 |
| xgb_lstm_ensemble | -0.0242 | -0.2583 | -2.1655 | -2.9973 | -0.0626 | -4.1278 | -0.3705 | -9.0061 | 0.4776 | 0.7971 |
| xgboost | -0.0349 | -0.3512 | -2.9302 | -3.5995 | -0.0583 | -6.0213 | -0.3812 | -8.5212 | 0.5114 | 0.7546 |
