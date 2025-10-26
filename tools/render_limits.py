#!/usr/bin/env python3
import os, json, sys
def worst(R):
  s=0
  for v in R.values(): s=max(s, 2 if v.get('status')=='crit' else (1 if v.get('status')=='warn' else 0))
  return 'crit' if s==2 else ('warn' if s==1 else 'ok')
def main():
  src = sys.argv[1] if len(sys.argv)>1 else '/root/inga-control/data/metrics/last_eval.json'
  out = '/root/inkaritsu/config/risk_limits.env'
  R   = json.load(open(src))['results']
  sev = worst(R); pf,halt = '1.0','0'
  if sev=='warn': pf='0.7'
  if sev=='crit': pf,halt='0.5','1'
  os.makedirs(os.path.dirname(out), exist_ok=True)
  with open(out,'w',encoding='utf-8') as f:
    f.write(f'POSITION_FACTOR={pf}\nHALT_NEW_ORDERS={halt}\nSEVERITY={sev}\n')
  print(f'[limits] {out}: severity={sev}, POSITION_FACTOR={pf}, HALT_NEW_ORDERS={halt}')
if __name__=='__main__': main()
