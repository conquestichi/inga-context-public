#!/usr/bin/env python3
import os, sys, json
def read_event_map(path):
  ks={}; cur=None
  for raw in open(path, encoding="utf-8"):
    s=raw.rstrip("\n")
    if not s.strip() or s.strip().startswith("#"): continue
    if s.strip()=="routes:": continue
    if s.strip().endswith(":") and not s.startswith("  "):
      cur=None; continue
    if s.strip().endswith(":") and s.startswith("  "):
      cur=s.strip().split(":")[0]; ks[cur]={}; continue
    if cur and s.strip().startswith("notify:"): ks[cur]["notify"]=s.split(":",1)[1].strip()
    if cur and s.strip().startswith("risk:"):   ks[cur]["risk"]=s.split(":",1)[1].strip()
  return ks
def route(typ,emap,ev_path):
  cfg=emap.get(typ,{})
  n=cfg.get("notify"); r=cfg.get("risk")
  if n=="digest": os.system("python3 /root/inga-context-public/tools/notify_digest.py >/dev/null 2>&1 || true")
  elif n=="slack": os.system(f"python3 /root/inga-context-public/tools/notify_slack.py '{ev_path}' >/dev/null 2>&1 || true")
  if r=="default": os.system("python3 /root/inga-context-public/tools/render_limits.py >/dev/null 2>&1 || true")
  print(f"[route] {typ} -> notify={n} risk={r}")
def main():
  if len(sys.argv)<2: print("[ERR] usage: route_event.py <event.json>", file=sys.stderr); sys.exit(2)
  p=sys.argv[1]; ev=json.load(open(p,encoding="utf-8")); typ=ev.get("event","")
  emap=read_event_map("/root/inga-context-public/context/EVENT_MAP.yaml")
  if typ in emap: route(typ,emap,p)
  else: print(f"[route] skip unknown event: {typ}")
if __name__=='__main__': main()
