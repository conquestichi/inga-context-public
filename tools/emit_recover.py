#!/usr/bin/env python3
import json,sys,os,datetime,glob
BASE="/root/inga-control/data/metrics"
cur=os.path.join(BASE,"last_eval.json")
prev=os.path.join(BASE,"prev_eval.json")
if not os.path.isfile(cur) or not os.path.isfile(prev):
  sys.exit(0)
C=json.load(open(cur)); P=json.load(open(prev))
cres=C.get("results",{}); pres=P.get("results",{})
pend="/root/inga-control/agent_queue/pending"; os.makedirs(pend,exist_ok=True)
cnt=0; now=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
for k,cv in cres.items():
  ps=pres.get(k,{}).get("status"); cs=cv.get("status")
  if ps in ("warn","crit") and cs=="ok":
    ev={"event":"kpi_guardrail_recover","kpi":k,"prev":ps,"now":cs,"ts":now}
    fn=os.path.join(pend,f"recover_{k}_{now.replace(':','')}.json")
    json.dump(ev,open(fn,"w"),ensure_ascii=False)
    cnt+=1
print(f"[recover] enqueued={cnt}")
