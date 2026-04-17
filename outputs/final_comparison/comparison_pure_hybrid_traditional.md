# Pure vs Hybrid vs Traditional — Combined Comparison

**Evaluation window:** 30 calendar days (dense span 2025-02-24 → 2025-03-25), from reference `signals.csv` in `/ocean/projects/cis260081p/chsu11/hybrid/TradingAgents/outputs/high_volatility_shock_pure/20260416T235718Z`.

LLM rows use `agent_metrics.json` (post–`run_eval`). Traditional rows are non-agent forecast baselines sliced to the **same** hourly bars on those dates.

---

## LLM agents vs traditional forecasts

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **LLM Pure** (high_volatility_shock_pure) | -0.1799 | -0.9106 | -4.3848 | -6.4335 | -0.1905 | -4.7801 | -0.0879 | -1.3342 | 0.4452 | 0.8317 |
| **LLM Hybrid (metrics)** (high_volatility_shock_hybrid) | 0.1053 | 2.3851 | 3.7299 | 7.1270 | -0.0561 | 42.53 | 0.1973 | 2.5246 | 0.4875 | 1.2509 |
| **LLM Hybrid (signals)** (high_volatility_shock_hybrid_signals) | 0.0129 | 0.1689 | 0.6231 | 0.9793 | -0.1330 | 1.2702 | 0.1049 | 1.3795 | 0.4917 | 1.0354 |

## Traditional forecasting baselines (same dates)

| strategy | cumulative_return | annualized_return | sharpe | sortino | max_drawdown | calmar | excess_cumulative_return | information_ratio | hit_rate | profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima_garch | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0920 | 1.3768 | 0.0000 | 0.0000 |
| buy_and_hold | -0.0920 | -0.6910 | -1.3768 | -2.0395 | -0.1939 | -3.5636 | 0.0000 | 0.0000 | 0.5153 | 0.9553 |
| lstm | -0.0123 | -0.1399 | -0.4364 | -0.6478 | -0.1000 | -1.3995 | 0.0796 | 1.2109 | 0.5000 | 0.9779 |
| macd | 0.2379 | 12.44 | 4.1479 | 7.5550 | -0.1188 | 104.7 | 0.3298 | 3.4904 | 0.4958 | 1.1477 |
| sma_cross | -0.2479 | -0.9688 | -4.7398 | -6.6084 | -0.4063 | -2.3843 | -0.1559 | -2.2388 | 0.4986 | 0.8543 |
| xgb_lstm_ensemble | 0.0012 | 0.0144 | 0.1788 | 0.2515 | -0.0594 | 0.2433 | 0.0931 | 1.4755 | 0.4952 | 1.0139 |
| xgboost | -0.0227 | -0.2437 | -1.3090 | -1.6769 | -0.0623 | -3.9098 | 0.0693 | 1.0200 | 0.4828 | 0.8956 |
