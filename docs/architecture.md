# 因果HUB v0.1 — 設計図（要約）

- 目的：KPI（日次/週次）生成→GitHub公開（SSH鍵）→Slack通知（未設定時は /tmp/slack.out）。
- データ：/root/inkaritsu/reports/
- リポジトリ：/root/work/inga-context-public（origin=git@github.com:conquestichi/inga-context-public.git）

【構成】
ingest → rule → decider → kpi → publish(oneshot) → GitHub
                                   └→ notify(Slack|/tmp)

【systemd】
- inkaritsu-kpi-report.service（10:40 JST）
- inkaritsu-kpi-weekly.service（Sun 11:10 JST）
- inkaritsu-hub-publish.service（oneshot）
  - drop-in: 10-auth/10-bash-wrapper/20-onfailure
  - 連携: 50-post-publish（任意）, 60-notify + 55-notify-env

【ガード】
- ink_git_guard.service/timer（30m）
- 退出コード: 0=健全 / 2=是正（Success） / 1=失敗
- 失敗時のみ OnFailure 通知。専用envを使用（巨大envは直読しない）

【通知】
- /root/bin/ink_notify_lib.sh（sink判定）
- /root/bin/ink_kpi_notify.sh（daily/weekly）
- /root/inkaritsu/config/ink_notify.env（INK_SLACK_WEBHOOK ほか）

## 12. ヘルス監視 / メトリクス
- エクスポータ: `/root/bin/ink_metrics_export.sh` → `/root/inkaritsu/reports/hub_metrics_status.json`
  - last_success / last_failure / 24h 成否 / 経過秒
- 監視: `ink_health_watch.service/timer`（30m）
  - しきい値: `/root/inkaritsu/config/ink_health.env`
  - 通知: Slack（未設定は `/tmp/slack.out`）

## 12. ヘルス監視 / メトリクス
- エクスポータ: `/root/bin/ink_metrics_export.sh` → `/root/inkaritsu/reports/hub_metrics_status.json`
  - last_success / last_failure / 24h 成否 / 経過秒
- 監視: `ink_health_watch.service/timer`（30m）
  - しきい値: `/root/inkaritsu/config/ink_health.env`
  - 通知: Slack（未設定は `/tmp/slack.out`）
