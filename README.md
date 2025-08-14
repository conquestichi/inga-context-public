# Inga Control (GitOps 正本)
- 目的: 因果＝ハブ（Runbook/可視化/記録）を Git 正本で管理し、VPS は実行専用（pull）で反映
- 階層: infra/monitoring, grafana/, runbook/, params/, policy/
- 変更手順: PR → CI検証 → マージ → VPS pull → Runbookで反映
