#!/usr/bin/env python3
import os, sys, json
def read_event_map(path):
  route = {"notify": None, "risk": None}; key=None
  for raw in open(path, encoding="utf-8"):
    s=raw.rstrip("\n")
    if s.strip().startswith("#") or not s.strip(): continue
    if s.strip()=="routes:": continue
    if "kpi_guardrail_breach:" in s: key="kpi_guardrail_breach"; continue
    if key=="kpi_guardrail_breach":
      t=s.strip()
      if t.startswith("notify:"): route["notify"]=t.split(":",1)[1].strip()
      if t.startswith("risk:"):   route["risk"]=t.split(":",1)[1].strip()
  return route
def main():
  if len(sys.argv)<2: print("[ERR] usage: route_event.py <event.json>", file=sys.stderr); sys.exit(2)
  ev_path=sys.argv[1]; ev=json.load(open(ev_path,encoding="utf-8")); typ=ev.get("event","")
  if typ!="kpi_guardrail_breach": print(f"[route] skip unknown event: {typ}"); return
  emap=read_event_map("/root/inga-context-public/context/EVENT_MAP.yaml")
  # notify
  if emap.get("notify")=="digest":
    os.system("python3 /root/inga-context-public/tools/notify_digest.py >/dev/null 2>&1 || true")
  elif emap.get("notify")=="slack":
    os.system(f"python3 /root/inga-context-public/tools/notify_slack.py '{ev_path}' >/dev/null 2>&1 || true")
  # risk limits
  if emap.get("risk")=="default":
    os.system("python3 /root/inga-context-public/tools/render_limits.py >/dev/null 2>&1 || true")
  print(f"[route] {typ} -> notify={emap.get('notify')} risk={emap.get('risk')}")
if __name__=='__main__': main()
