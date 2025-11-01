#!/usr/bin/env python3
import os, json, datetime, subprocess, sys, hashlib
EVAL="/root/inga-control/data/metrics/last_eval.json"
if len(sys.argv)>1: EVAL=sys.argv[1]
data=json.load(open(EVAL,encoding='utf-8'))
R=data.get('results',{})
sev_map={'ok':0,'warn':1,'crit':2}; sev=0
for v in R.values(): sev=max(sev, sev_map.get(str(v.get('status','ok')).lower(),0))
sev_txt={0:'OK',1:'WARN',2:'CRITICAL'}[sev]
def fmt(k,lab):
  v=R.get(k,{}); val=v.get('value'); unit=v.get('unit') or ''
  return f"{lab}: {val}{(' '+unit) if unit else ''}  → {str(v.get('status','?')).upper()}"
order=[('pnl_daily','pnl_daily'),('win_rate_30d','win_rate_30d'),('sharpe_30d','sharpe_30d'),
       ('max_drawdown_90d','max_drawdown_90d'),('turnover_1d','turnover_1d'),('slippage_bps_1d','slippage_bps_1d')]
lines=['- '+fmt(k,lab) for k,lab in order if k in R]
msg=f"[{sev_txt}] KPI digest\n" + "\n".join(lines)

# 5分バケット + 内容ハッシュで重複抑止
now=datetime.datetime.utcnow()
bucket=now.replace(minute=(now.minute//5)*5, second=0, microsecond=0)
sig=hashlib.sha1(msg.encode('utf-8')).hexdigest()[:10]
flag=f"/tmp/inga_digest_{bucket.strftime('%Y%m%d%H%M')}_{sig}"
if os.path.exists(flag): sys.exit(0)
open(flag,'w').close()

env=os.environ.copy(); env['ENV_SRC']='/root/inkaritsu/config/ink_notify.env'
subprocess.run(['/root/bin/ink_post_to_slack.sh', msg], check=False, env=env)
