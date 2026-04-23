# Pure vs Hybrid vs Traditional — Combined Comparison

**Evaluation window:** 30 calendar days (dense span 2025-10-27 → 2025-11-25), from reference `signals.csv` in `/ocean/projects/cis260081p/chsu11/hybrid/TradingAgents/outputs/bear_drawdown_pure/20260418T121803Z`.

LLM rows use `agent_metrics.json` (post–`run_eval`). Traditional rows are non-agent forecast baselines sliced to the **same** hourly bars on those dates.

---

## LLM agents vs traditional forecasts

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **LLM Pure** (bear_drawdown_pure) | 0.2586 | 15.45 | 7.0681 | 12.34 | -0.0688 | 224.4 | 0.4950 | 6.8601 | 0.5506 | 1.3507 |
| **LLM Hybrid (metrics)** (bear_drawdown_hybrid_metrics_best2) | 0.0208 | 0.2842 | 0.9931 | 1.5312 | -0.0693 | 4.1031 | 0.2572 | 4.6994 | 0.5156 | 1.0543 |
| **LLM Hybrid (signals)** (bear_drawdown_hybrid_signals_best2) | 0.0428 | 0.6665 | 1.3938 | 2.3532 | -0.0944 | 7.0570 | 0.2793 | 4.0984 | 0.5031 | 1.0513 |

## Traditional forecasting baselines (same dates)

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima_garch | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.2364 | 6.0169 | 0.0000 | 0.0000 |
| buy_and_hold | -0.2364 | -0.9625 | -6.0169 | -8.9417 | -0.2913 | -3.3047 | 0.0000 | 0.0000 | 0.4917 | 0.8388 |
| lstm | 0.2836 | 19.9 | 7.0559 | 12.32 | -0.0549 | 362.6 | 0.5200 | 7.4088 | 0.5208 | 1.2756 |
| macd | -0.0677 | -0.5739 | -1.3665 | -2.3041 | -0.1302 | -4.4083 | 0.1687 | 3.0639 | 0.4861 | 0.9609 |
| sma_cross | 0.1087 | 2.5118 | 2.6598 | 4.7689 | -0.1221 | 20.57 | 0.3451 | 4.6145 | 0.4972 | 1.0808 |
| xgb_lstm_ensemble | -0.0426 | -0.4116 | -2.2080 | -3.0219 | -0.0782 | -5.2640 | 0.1938 | 4.8985 | 0.4756 | 0.8264 |
| xgboost | -0.0412 | -0.4005 | -2.1895 | -3.0096 | -0.0653 | -6.1287 | 0.1953 | 5.0165 | 0.4247 | 0.8179 |
