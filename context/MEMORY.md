# 因果記憶（要約）
- 目的: 因果律システムの設計・運用に必要な「前提・決定・既知の制約」を集約
- ローカルHUB記憶の鏡: /root/inkaritsu/docs/hub/INGA_MEMORY.md
- 変更手順: PR（レビュー後にマージ）

## Local import (2025-10-04_10:52:34+0900)

---
## Handoff @ 2025-10-03T13:33:30+09:00

- Author / Host : root@vm-db0e111f-06.tail848448.ts.net
- Scope         : 因果HUB v0.1（KPI 日次/週次 + Slack 通知ラッパ）
- What we did   :
  - Slack Webhook を **SSoT** 化（`INKARITSU_SLACK_WEBHOOK_URL` + systemd Drop-in で注入）
  - ラッパ `/root/bin/ink_post_to_slack.sh` を整備（JSON 化 / HTTP/2 200 ヘッダ検証）
  - ドキュメント作成  
    - `docs/hub/INKARITSU_HUB_v0.1_Design.md`  
    - `docs/hub/Runbook.md`  
    - `docs/hub/adr/0001-unify-slack-webhook.md`
  - 直近ログ採取（kpi-report / kpi-weekly）と Slack スモーク送信
- How to resume :
  1) Runbook の **日常チェック** を実行  
  2) 必要に応じて `systemctl start inkaritsu-kpi-report.service` / `inkaritsu-kpi-weekly.service`  
  3) Slack 200 確認:  
     `ENV_SRC=/root/inkaritsu/config/ink_notify.env /root/bin/ink_post_to_slack.sh "resume 2025-10-03 13:33:30+0900"`
- Notes         :
  - 直接 `hooks.slack.com` を叩くコードは禁止。検査レシピは Runbook の `直叩き検出` を使用。
  - Webhook 値はリポジトリに含めない（env/600）。ローテ時は SSoT を差し替え → `daemon-reload` → スモーク。
## v0.1 完了サマリ
- SSoT: /root/inkaritsu/config/ink_notify.env（600、umask 077）
- ラッパ: /root/bin/ink_post_to_slack.sh（HTTP/2 200 判定）
- KPI services: inkaritsu-kpi-report / inkaritsu-kpi-weekly（Drop-in で SSoT 注入）
- OnFailure: inkaritsu-failure-notify@.service を適用
- 監査: inkaritsu-slack-audit.timer（Sun 11:20 JST）
- ヘルスチェック: /root/bin/ink_healthcheck.sh
- 直接 curl の排除: 定期 grep 監査導入
