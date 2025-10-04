#!/usr/bin/env python3
import os, yaml
BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "context"))
def load_yaml(name):
    p = os.path.join(BASE, name)
    if not os.path.exists(p): return {}
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
kpi  = load_yaml("KPI_CATALOG.yaml")
evt  = load_yaml("EVENT_MAP.yaml")
risk = load_yaml("RISK_GUARDRAILS.yaml")
lines=[]
lines.append("# 因果コンテキスト サマリ（自動生成）\n")
lines.append("> このファイルは CI により生成されます。直接編集しないでください。\n")
# KPI
lines.append("## KPI_CATALOG\n")
if isinstance(kpi, dict):
    for g, items in kpi.items():
        lines.append(f"### {g}")
        lines.append("| key | name | window | unit | warn | crit |")
        lines.append("|---|---|---|---|---:|---:|")
        if isinstance(items, dict):
            for k, d in items.items():
                name   = (d or {}).get("name","")
                window = (d or {}).get("window","")
                unit   = (d or {}).get("unit","")
                warn   = (d or {}).get("warn","")
                crit   = (d or {}).get("crit","")
                lines.append(f"| {g}.{k} | {name} | {window} | {unit} | {warn} | {crit} |")
# EVENTS
lines.append("\n## EVENTS")
routes = (evt or {}).get("routes", {}) or {}
events = (evt or {}).get("events", {}) or {}
lines.append("### routes")
for r,v in routes.items(): lines.append(f"- {r}: {v}")
lines.append("\n### events")
lines.append("| name | severity | route | template |")
lines.append("|---|---|---|---|")
for en,e in events.items():
    tmpl = str((e or {}).get("template","")).replace("|","\\|")
    lines.append(f"| {en} | {(e or {}).get(severity,)} | {(e or {}).get(route,)} | {tmpl} |")
# RISK
lines.append("\n## RISK_GUARDRAILS")
limits = (risk or {}).get("limits", {}) or {}
if limits:
    lines.append("### limits")
    lines.append("| key | value |")
    lines.append("|---|---:|")
    for k,v in limits.items(): lines.append(f"| {k} | {v} |")
acts = (risk or {}).get("actions", {}).get("on_breach", []) or []
if acts:
    lines.append("\n### actions.on_breach")
    for a in acts: lines.append(f"- {a}")
out = os.path.join(BASE, "README.md")
with open(out,"w",encoding="utf-8") as f: f.write("\n".join(lines)+"\n")
print(f"wrote {out}")
