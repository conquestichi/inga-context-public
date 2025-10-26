# Inga Agent Mode (HUB主導)
- 本体ロジックは **HUB(=このリポ)** に置く。実行ノードは `inga-control` が担当。
- 規約:
  - KPI評価: `python3 tools/kpi_eval.py --catalog context/KPI_CATALOG.yaml --metrics <metrics.json> -o /root/inga-control/data/metrics/last_eval.json [--emit-pending]`
  - レポート生成: `python3 tools/report_head_from_eval.py /root/inga-control/data/metrics/last_eval.json /root/inga-control/docs/agent-reports/$(date +%F).md`
  - イベントは `agent_queue/pending/*.json`（drainが拾う）
- 変更は **必ずPR**。HUBの `context/*` と `tools/*` を唯一のSSOTとする。
