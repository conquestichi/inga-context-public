#!/usr/bin/env python3
import os, json, sys, datetime, hashlib, re

SCHEMA_EVAL="/root/inga-control/data/metrics/last_eval.json"
GUARDS_YAML="/root/inga-context-public/context/RISK_GUARDRAILS.yaml"
OUT="/root/inkaritsu/config/risk_limits.env"

def load_eval(path):
  return json.load(open(path,encoding='utf-8')).get("results",{})

def load_guards(path):
  lines=open(path,encoding="utf-8").read().splitlines()
  defaults={}; rules=[]; mode=None; i=0
  while i<len(lines):
    s=lines[i].strip()
    if not s or s.startswith("#"): i+=1; continue
    if s=="defaults:": mode="def"; i+=1; continue
    if s=="rules:":    mode="rules"; i+=1; continue
    if mode=="def" and ":" in s:
      k,v=[t.strip() for t in s.split(":",1)]; defaults[k]=v; i+=1; continue
    if mode=="rules" and s.startswith("- match:"):
      m=re.search(r"\{(.*)\}", s); match={}
      if m:
        for p in [x.strip() for x in m.group(1).split(",") if x.strip()]:
          k,v=[t.strip() for t in p.split(":",1)]; match[k]=v
      i+=1
      setmap={}
      if i<len(lines):
        t=lines[i].strip(); m2=re.search(r"\{(.*)\}", t)
        if m2:
          for p in [x.strip() for x in m2.group(1).split(",") if x.strip()]:
            k,v=[tt.strip() for tt in p.split(":",1)]; setmap[k]=v
      rules.append({"match":match,"set":setmap}); i+=1; continue
    i+=1
  return defaults, rules

def worst_overall(R):
  order={"ok":0,"warn":1,"crit":2}
  s=0
  for v in R.values(): s=max(s, order.get(str(v.get("status","ok")).lower(),0))
  return ["ok","warn","crit"][s]

def baseline_env(sev):
  pf="1.0"; halt="0"
  if sev=="warn": pf="0.7"
  if sev=="crit": pf="0.5"
  return {"POSITION_FACTOR":pf, "HALT_NEW_ORDERS":halt, "SEVERITY":sev}

def apply_rules(env, R, defaults, rules):
  env.update(defaults or {})
  for k,v in R.items():
    ctx={"kpi":k, "status":str(v.get("status","ok")).lower()}
    for r in rules:
      mt=r.get("match",{})
      if all(str(ctx.get(kk))==str(vv) for kk,vv in mt.items()):
        env.update(r.get("set",{}))
  return env

def main():
  R=load_eval(SCHEMA_EVAL)
  sev=worst_overall(R)
  env=baseline_env(sev)
  defaults, rules=load_guards(GUARDS_YAML)
  env=apply_rules(env, R, defaults, rules)

  os.makedirs(os.path.dirname(OUT), exist_ok=True)
  with open(OUT,"w",encoding="utf-8") as f:
    for k in sorted(env.keys()):
      f.write(f"{k}={env[k]}\n")
  print(f"[limits] {OUT}: " + " ".join([f"{k}={env[k]}" for k in sorted(env.keys())]))
if __name__=="__main__": main()
