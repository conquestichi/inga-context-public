#!/usr/bin/env python3
import sys, json, os, datetime, pathlib
TPL = """# Inga Daily Report ({date})
## KPI Digest (window=SSOT)
- pnl_daily: {pnl_daily} JPY → {pnl_status}
- win_rate_30d: {win_rate_30d} % → {win_status}
- sharpe_30d: {sharpe_30d} → {sharpe_status}
- max_drawdown_90d: {mdd_90d} % → {mdd_status}
- turnover_1d: {turnover_1d} % → {turn_status}
- slippage_bps_1d: {slip_bps_1d} bps → {slip_status}

## Actions Today
- (auto) see guardrails / ops playbook

## Ops Notes
- generated_from: {eval_path}
"""
def main():
    if len(sys.argv)<3: sys.exit("usage: report_head_from_eval.py <eval.json> <report.md>")
    ev, rpt = sys.argv[1], sys.argv[2]
    R=json.load(open(ev,encoding="utf-8"))["results"]
    gv=lambda k: "-" if R.get(k,{}).get("value") is None else R[k]["value"]
    gs=lambda k: R.get(k,{}).get("status","unknown").upper()
    today=datetime.date.today().isoformat()
    head=TPL.format(date=today, eval_path=os.path.abspath(ev),
        pnl_daily=gv("pnl_daily"), pnl_status=gs("pnl_daily"),
        win_rate_30d=gv("win_rate_30d"), win_status=gs("win_rate_30d"),
        sharpe_30d=gv("sharpe_30d"), sharpe_status=gs("sharpe_30d"),
        mdd_90d=gv("max_drawdown_90d"), mdd_status=gs("max_drawdown_90d"),
        turnover_1d=gv("turnover_1d"), turn_status=gs("turnover_1d"),
        slip_bps_1d=gv("slippage_bps_1d"), slip_status=gs("slippage_bps_1d"))
    p=pathlib.Path(rpt); p.parent.mkdir(parents=True, exist_ok=True)
    old=p.read_text(encoding="utf-8") if p.exists() else ""
    p.write_text(head+"\n---\n"+old, encoding="utf-8"); print(f"[report] written: {p}")
if __name__=="__main__": main()
