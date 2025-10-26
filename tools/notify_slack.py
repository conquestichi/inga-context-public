#!/usr/bin/env python3
import os, sys, json, subprocess
def main():
  ev=json.load(open(sys.argv[1])) if len(sys.argv)>1 else json.load(sys.stdin)
  sev=ev.get("severity","?").upper(); ttl=f"[{sev}] {ev.get(\"event\",\"event\")}"
  kpi=ev.get("kpi"); val=ev.get("value"); unit=ev.get("unit") or "";
  line=f"{kpi}: {val}{(\" \"+unit) if unit else \"\"} (warn={ev.get(\"warn\")}, crit={ev.get(\"crit\")})"
  text=ttl+"\\n"+line+"\\n"+str(ev.get("ts",""))
  env=os.environ.copy(); env["ENV_SRC"]="/root/inkaritsu/config/ink_notify.env"
  subprocess.run(["/root/bin/ink_post_to_slack.sh", text], check=False, env=env)
if __name__=="__main__": main()
