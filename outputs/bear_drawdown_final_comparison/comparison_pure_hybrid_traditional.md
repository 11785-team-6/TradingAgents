# Pure vs Hybrid vs Traditional — Combined Comparison

**Evaluation window:** 30 calendar days (dense span 2025-10-27 → 2025-11-25), from reference `signals.csv` in `/ocean/projects/cis260081p/chsu11/hybrid/TradingAgents/outputs/bear_drawdown_pure/20260417T111728Z`.

LLM rows use `agent_metrics.json` (post–`run_eval`). Traditional rows are non-agent forecast baselines sliced to the **same** hourly bars on those dates.

---

## LLM agents vs traditional forecasts

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **LLM Pure** (bear_drawdown_pure) | 0.2196 | 10.21 | 6.7693 | 12.43 | -0.0688 | 148.3 | 0.4560 | 6.8428 | 0.5366 | 1.3704 |
| **LLM Hybrid (metrics)** (bear_drawdown_hybrid) | 0.0972 | 2.0936 | 3.5453 | 5.9156 | -0.0604 | 34.66 | 0.3336 | 5.5542 | 0.5177 | 1.1709 |
| **LLM Hybrid (signals)** (bear_drawdown_hybrid_signals) | 0.1631 | 5.2905 | 5.5066 | 9.5981 | -0.0444 | 119.1 | 0.3995 | 6.3584 | 0.5254 | 1.2631 |

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
