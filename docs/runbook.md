# 因果HUB v0.1 — 運用Runbook（要約）

■ 平常運用
- 日次: journalctl(kpi-report) → ファイル更新確認 → 必要なら publish
- 週次: journalctl(kpi-weekly) → weekly/latest 確認
- SSH push 検証: ops.sh push-dry

■ 定期ヘルス
- タイマー: ops.sh timers
- ガード: systemctl start ink_git_guard.service; journalctl -u ink_git_guard.service
  - ExecMainStatus=0|2 を期待（1は失敗）

■ 障害対応
- Git https 回帰: 復旧ワンライナー（docs参照）→ 再実行
- publish失敗: journalctl→原因切分→再実行
- KPI未生成: status/env/権限/依存を確認

■ 変更管理
- env変更→ink_env_apply.sh→影響サービス再起動
- commit→SSH push→publish確認

## 通知（最終仕様）
- 成功：`ink_kpi_notify.sh {daily|weekly} --rich` を ExecStartPost で実行（sink=slack または /tmp/slack.out）
- 失敗：OnFailure により直近ログを Slack 通知（publish/kpi 共通）
- メッセージ例：
[HUB/KPI Daily ✅] as_of=2025-09-22 12:34:56 JST
files=hub_metrics_daily.json
sink=slack
summary=parsed=24 bad_json=0 total=24

bash
コードをコピーする
