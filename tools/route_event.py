#!/usr/bin/env python3
import os, sys, json, time, hashlib

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

def dedupe_crit(ev):
  kpi=str(ev.get("kpi",""))
  bucket=int(time.time()//600)  # 10min
  sig=hashlib.sha1(f"{ev.get('event','')}_{kpi}".encode()).hexdigest()[:8]
  flag=f"/tmp/inga_crit_{kpi}_{bucket}_{sig}"
  if os.path.exists(flag): return False
  open(flag,"w").close()
  return True

def main():
  if len(sys.argv)<2:
    print("[ERR] usage: route_event.py <event.json>", file=sys.stderr); sys.exit(2)
  p=sys.argv[1]
  ev=json.load(open(p,encoding="utf-8"))
  typ=ev.get("event","")
  sev=(ev.get("status") or ev.get("severity") or "").lower()

  emap=read_event_map("/root/inga-context-public/context/EVENT_MAP.yaml")
  cfg=emap.get(typ, {})
  notify=cfg.get("notify")
  risk=cfg.get("risk")

  # crit は即時Slack（デュープ抑制）
  if sev=="crit" and dedupe_crit(ev):
    os.system(f"python3 /root/inga-context-public/tools/notify_slack.py '{p}' >/dev/null 2>&1 || true")

  # 通常ルート：digest / slack
  if notify=="digest":
    os.system("python3 /root/inga-context-public/tools/notify_digest.py >/dev/null 2>&1 || true")
  elif notify=="slack":
    os.system(f"python3 /root/inga-context-public/tools/notify_slack.py '{p}' >/dev/null 2>&1 || true")

  # リスク出力（既定は default）
  if risk=="default":
    os.system("python3 /root/inga-context-public/tools/render_limits.py >/dev/null 2>&1 || true")

  print(f"[route] {typ} sev={sev or '-'} -> notify={notify} risk={risk}")

if __name__=='__main__': main()
