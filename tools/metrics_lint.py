#!/usr/bin/env python3
import json,sys,os
SCHEMA=json.load(open('/root/inga-context-public/context/METRICS_SCHEMA.json'))
REQ=SCHEMA['required']; PROPS=SCHEMA['properties']
def fail(msg): print(f"[LINT][ERR] {msg}", file=sys.stderr); sys.exit(1)
def main():
  if len(sys.argv)<2: fail("usage: metrics_lint.py <metrics.json>")
  p=sys.argv[1]
  try: data=json.load(open(p,encoding='utf-8'))
  except Exception as e: fail(f"json load failed: {e}")
  if not isinstance(data,dict): fail("top-level not object")
  for k in REQ:
    if k not in data: fail(f"missing key: {k}")
    if not isinstance(data[k],(int,float)): fail(f"not number: {k}")
  for k in data.keys():
    if k not in PROPS: fail(f"unexpected key: {k}")
  print("[LINT] ok:", p)
if __name__=='__main__': main()
