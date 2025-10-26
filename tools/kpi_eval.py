# --- below: real implementation (part1) ---
import re, datetime, argparse, pathlib, subprocess
def parse_kpi_catalog(path:str):
    items, cur = {}, None
    for raw in open(path, encoding="utf-8"):
        line=raw.rstrip("\n"); s=line.strip()
        if not s or s.startswith("#"): continue
        if re.match(r"^\s{2}[A-Za-z0-9_]+:\s*$", line):
            cur=line.strip()[:-1]; items[cur]={}; continue
        m=re.match(r"^\s{4}([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
        if m and cur:
            k=m.group(1); v=m.group(2).split(" #",1)[0].strip()
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")): v=v[1:-1]
            if re.match(r"^-?\d+(\.\d+)?$", v): v=float(v) if "." in v else int(v)
            items[cur][k]=v
    return items
def infer_direction(warn,crit):
    try: return "lower_worse" if float(crit)<float(warn) else "higher_worse"
    except: return "lower_worse"
def eval_status(value,warn,crit,direction):
    if value is None: return "unknown"
    try:
        v=float(value); w=float(warn); c=float(crit)
        if direction=="lower_worse":   return "crit" if v<=c else ("warn" if v<=w else "ok")
        else:                          return "crit" if v>=c else ("warn" if v>=w else "ok")
    except: return "unknown"
def iso_now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
def detect_queue_root(default="/root/inga-control/agent_queue"):
    try:
        out=subprocess.run(["systemctl","show","agent-queue-drain.service","-p","ConditionPathExistsGlob","--value"],
                           capture_output=True,text=True,check=False).stdout.strip()
        if out: return out.replace("/pending/*.json","")
    except: pass
    return default
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--catalog", default="context/KPI_CATALOG.yaml")
    ap.add_argument("--metrics", required=True)
    ap.add_argument("-o","--out", default="/root/inga-control/data/metrics/last_eval.json")
    ap.add_argument("--emit-pending", action="store_true")
    ap.add_argument("--queue-root", default=None)
    a=ap.parse_args()
    if not os.path.isfile(a.catalog): sys.exit(f"[ERR] catalog not found: {a.catalog}")
    if not os.path.isfile(a.metrics): sys.exit(f"[ERR] metrics not found: {a.metrics}")
    cat=parse_kpi_catalog(a.catalog); met=json.load(open(a.metrics,encoding="utf-8"))
    res={}
    for k,meta in cat.items():
        w, c = meta.get("warn"), meta.get("crit")
        dirc = infer_direction(w,c); val = met.get(k,None)
        res[k]={ "name": meta.get("name",k), "value": val, "unit": meta.get("unit"),
                 "window": meta.get("window"), "warn": w, "crit": c,
                 "direction": dirc, "status": eval_status(val,w,c,dirc) }
    asof=iso_now(); out={"asof":asof,"results":res,"catalog_path":os.path.abspath(a.catalog),"metrics_path":os.path.abspath(a.metrics)}
    json.dump(out, open(a.out,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"== KPI evaluation @ {asof} ==")
    for k,v in res.items():
        u="" if v["unit"] is None else f" {v['unit']}"
        print(f"- {k:18s}: {str(v['value'])}{u} -> {v['status'].upper()} (warn={v['warn']}, crit={v['crit']}, dir={v['direction']})")
    if a.emit_pending:
        qroot=a.queue_root or detect_queue_root(); pen=os.path.join(qroot,"pending")
        pathlib.Path(pen).mkdir(parents=True, exist_ok=True); cnt=0
        for k,v in res.items():
            if v["status"] in ("warn","crit"):
                ev={"event":"kpi_guardrail_breach","severity":v["status"],"kpi":k,"value":v["value"],
                    "warn":v["warn"],"crit":v["crit"],"unit":v["unit"],"window":v["window"],"ts":asof}
                fn=f"{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}_{k}_{v['status']}.json"
                json.dump(ev, open(os.path.join(pen,fn),"w",encoding="utf-8"), ensure_ascii=False); cnt+=1
        print(f"[enqueue] {cnt} event(s) into {pen}")
if __name__=="__main__": main()
