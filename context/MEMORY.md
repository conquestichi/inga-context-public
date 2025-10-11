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
<!-- BEGIN 因果GPT-BOARD @ 2025-10-11 23:03:52 JST -->
## 因果GPT: Task Board Snapshot (2025-10-11 23:03:52 JST)

**現況**: Guardrail=OK / Runner=OK(`flock -w 5`) / Queue=pending0

### Workstreams
- WS-A 運用基盤（Ops/Runbook）
- WS-B 観測とSLO（Observability/KPI）
- WS-C エージェント契約（Agents/Contract）
- WS-D 同期/ガードレール（Sync/Guardrail）
- WS-E セキュリティ/鍵（Secrets/Keys）
- WS-F ドキュメント/記憶（Docs/HUB）

### タスク（ID / 概要 / 優先）
- INK-A01: Runner OnFailure Slack 通報（高）
- INK-A02: Queue ヘルス時系列 JSONL（中）
- INK-A03: guardrail クリーン冪等化（中）
- INK-A04: Ops コマンド固定化（中）
- INK-B01: p95 指標（pending→result / content→pending）（高）
- INK-B02: SLO 逸脱アラート（高）
- INK-B03: 日次 digest 拡張（中）
- INK-C01: payload schema v1 固定（高）
- INK-C02: NG/OK スモーク標準化（中）
- INK-C03: archived 階層規約（中）
- INK-D01: gr-guardrail no-op & ログ整形（高）
- INK-D02: behind 検出→update-branch リトライ（中）
- INK-E01: DeployKey/PAT 満了監視（高）
- INK-E02: 権限縮退検出（中）
- INK-F01: HUB RAW優先ルールの明文化（高）
- INK-F02: Runbook刷新（中）
- INK-F03: インシデント記録テンプレ（中）

**進行ステータス**
- Doing: INK-A01 / INK-B01 / INK-D01 / INK-F01
- Ready: INK-A03 / INK-B02 / INK-C01 / INK-F02
- Icebox: INK-E02 / INK-C03
<!-- END 因果GPT-BOARD @ 2025-10-11 23:03:52 JST -->
