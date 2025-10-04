# 因果コンテキスト サマリ（自動生成）

> このファイルは CI により生成されます。直接編集しないでください。

## KPI_CATALOG

### trading_perf
| key | name | window | unit | warn | crit |
|---|---|---|---|---:|---:|
| trading_perf.pnl_daily | Daily PnL | 1d | JPY | -100000 | -300000 |
| trading_perf.win_rate_30d | Win Rate (30d) | 30d | pct | 45 | 35 |
| trading_perf.sharpe_30d | Sharpe (30d) | 30d | ratio | 0.5 | 0.0 |
| trading_perf.max_drawdown_90d | Max Drawdown (90d) | 90d | pct | -10 | -15 |
| trading_perf.turnover_1d | Turnover (1d) | 1d | pct | 300 | 500 |
| trading_perf.slippage_bps_1d | Slippage (1d) | 1d | bps | 10 | 20 |

## EVENTS
### routes
- trading_ops: trading_ops
- risk_ops: risk_ops
- infra_ops: infra_ops

### events
| name | severity | route | template |
|---|---|---|---|
| order_filled | info | trading_ops | Filled {symbol} {qty} @ {price} |
| order_rejected | warn | trading_ops | Rejected {symbol} {qty} reason={reason} |
| connectivity_down | critical | infra_ops | Connectivity down {venue} |
| model_deployed | info | trading_ops | Model deployed {model}@{sha} |
| risk_limit_breached | critical | risk_ops | Risk breach {type}: {value} > {limit} |
| model_rollback | warn | trading_ops | Rollback to {sha} cause={cause} |

## RISK_GUARDRAILS
### limits
| key | value |
|---|---:|
| max_daily_loss_pct | 3 |
| max_drawdown_pct | 10 |
| max_position_notional_jpy | 10000000 |
| max_order_rate_per_min | 60 |
| max_open_orders | 200 |

### actions.on_breach
- halt_trading
- notify_slack
- require_manual_resume
