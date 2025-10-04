#!/usr/bin/env python3
import sys, os
import yaml
BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "context"))
def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
def fail(msg):
    print(f"NG: {msg}", file=sys.stderr); sys.exit(1)

# KPI
kpi = load(os.path.join(BASE, "KPI_CATALOG.yaml"))
if not isinstance(kpi, dict): fail("KPI_CATALOG.yaml: top must be mapping")
for g, items in kpi.items():
    if not isinstance(items, dict): fail(f"KPI group `{g}` must be mapping")
    for k, d in items.items():
        for field in ("name","window","unit","warn","crit"):
            if field not in d: fail(f"KPI `{g}.{k}` missing `{field}`")

# EVENT
evt = load(os.path.join(BASE, "EVENT_MAP.yaml"))
routes = evt.get("routes", {}) or {}
events = evt.get("events", {}) or {}
sev_ok = {"info","warn","critical"}
for en, e in events.items():
    if e.get("severity") not in sev_ok: fail(f"EVENT `{en}` invalid severity")
    r = e.get("route")
    if r not in routes: fail(f"EVENT `{en}` route `{r}` not in routes")
    if "template" not in e: fail(f"EVENT `{en}` missing template")

# RISK
risk = load(os.path.join(BASE, "RISK_GUARDRAILS.yaml"))
limits = risk.get("limits") or {}
if not isinstance(limits, dict): fail("RISK_GUARDRAILS.yaml: `limits` must be mapping")
for k,v in limits.items():
    if not isinstance(v,(int,float)): fail(f"risk limit `{k}` must be number")
acts = (risk.get("actions",{}).get("on_breach") or [])
allowed = {"halt_trading","notify_slack","require_manual_resume"}
for a in acts:
    if a not in allowed: fail(f"actions.on_breach contains unknown `{a}`")
print("OK: context validated (KPI/EVENT/RISK)")
