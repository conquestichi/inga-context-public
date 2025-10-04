#!/usr/bin/env python3
import sys, yaml, re, os
base = os.path.join(os.path.dirname(__file__), .., context)
def load(p): 
    with open(p, r, encoding=utf-8) as f: 
        return yaml.safe_load(f) or {}
def fail(msg): 
    print(f"NG: {msg}", file=sys.stderr); sys.exit(1)
# KPI
kpi = load(os.path.join(base,KPI_CATALOG.yaml))
assert isinstance(kpi, dict), "KPI_CATALOG.yaml: top must be mapping"
for g,items in kpi.items():
    if not isinstance(items, dict): fail(f"KPI group  must be mapping")
    for k,defn in items.items():
        for field in (name,window,unit,warn,crit):
            if field not in defn: fail(f"KPI  missing ")
# EVENT
evt = load(os.path.join(base,EVENT_MAP.yaml))
routes = evt.get(routes,{}) or {}
events = evt.get(events,{}) or {}
sev_ok = {info,warn,critical}
for en, e in events.items():
    if e.get(severity) not in sev_ok: fail(f"EVENT  invalid severity")
    r = e.get(route); 
    if r not in routes: fail(f"EVENT  route  not in routes")
    if template not in e: fail(f"EVENT  missing template")
# RISK
risk = load(os.path.join(base,RISK_GUARDRAILS.yaml))
limits = (risk.get(limits) or {})
if not isinstance(limits, dict): fail("RISK_GUARDRAILS.yaml limits must be mapping")
for k,v in limits.items():
    if not isinstance(v,(int,float)): fail(f"risk limit  must be number")
acts = (risk.get(actions,{}).get(on_breach) or [])
allowed = {halt_trading,notify_slack,require_manual_resume}
if any(a not in allowed for a in acts): fail("actions.on_breach contains unknown action")
print("OK: context validated (KPI/EVENT/RISK)")
