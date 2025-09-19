# Inkaritsu Ops Handover (v1)

## 0. 概要
- 目的: 因果コアは VPS ローカルで確実保存。監視～自己修復～通知はエージェント自動化。
- 状態: GitOps / Prometheus / Alertmanager / Grafana / エージェント群(ritsu/kogane) すべて稼働。

## 1. GitOps / 監視
- Prometheus OK（/etc に正本配置、rules 読み込み成功）
- Alertmanager OK（127.0.0.1:9093、secret は /var/lib/prometheus/alertmanager/.slack_webhook）
- ルール:
  - AgentDown / AgentStuck（agents.yml）
  - InkaritsuVersionStale を **updated_seconds** 実時間判定へ刷新
- Grafana: 稼働 / ダッシュボード（Version ほか）

## 2. エージェント
- ritsu (127.0.0.1:8181) / kogane (127.0.0.1:8282) 稼働・ハードニング drop-in 済み
- Inkaritsu Agent v2.1: 2分周期
  - /ready 監視 → restart、AM 9093 listen 監視、version鮮度、**メモリ鮮度(>30m警告)**、AM自己修復(AUTO_FIX_AM=1)
  - 反映: Slack 要約、morning report 09:05

## 3. メモリ保全
- 10分毎 snapshot (tgz+sha256) / 週次ローテ / reflect-log 15分トリム / ディスクガード(>85%)
- 失敗時 Slack 通知 (OnFailure)

## 4. PR 自動化（プラン不要）
- `.github/workflows/promtool-automerge.yml` により **promtool 成功＋ラベル `automerge`** で自動マージ
- 自動PRツール:
  - `/opt/inkaritsu/agent/auto_pr.sh`（stash対応、ラベル付与つき）
  - `/opt/inkaritsu/agent/auto_pr_api.sh`（gh不要のREST版・対話入力可）
- puller: `Environment=HOME=/root` drop-in 済み

## 5. 主要タイマー（systemd）
- inkaritsu-agent.timer（2m）、memory-snapshot/rotate/trim/disk-guard、morning-report、spawner

## 6. 直近実績
- PR → promtool 成功 → 自動マージ → puller SUCCESS を複数回確認
- ritsu/kogane target health: up

## 7. 引き継ぎのコマンド（一式は /root/inkaritsu/bin/inkaritsu-handover.sh を参照）
- 状態確認、PR 自動作成、GitOps 反映のサンプルを同梱

## Handover 20250816_184129
- git_sha: 0ce647a
- services: inkaritsu=active, control=active, runner.timer=active
- /health: {"summary":[{"timestamp":"2025-08-08T08:30:28.782314","event":"order_signal"}],"latest_payload_json":null,"latest_payload_raw_tail":"]633;E;echo;2d42ed14-147c-415d-92bc-2df194231a02\u0007\u001b]633;C\u0007\n[監視・通知 進捗 | 2025-08-11 11:24:29]\n■ 状態\n  - inkaritsu(webhook) / Prometheus / Alertmanager / Grafana すべて active/ready\n  - Prometheus targets: inkaritsu_trading / inkaritsu_webhook / prometheus = health: up\n  - Alertmanager cluster: disabled(単体) 正常応答\n  - Grafana /api/health: ready（SSHトンネル経由で http://localhost:33000 で閲覧）\n■ 今日はここまでやったこと\n  - 監視スタック復旧（Prometheus/Alertmanager/Grafana）\n  - Grafana datasource(provisioning) 確認：Prometheus -> http://127.0.0.1:9090\n  - ダッシュボード『Inkaritsu モニタ』で稼働・RPM・Webhook状態の可視化\n  - Slack 通知経路確認：Prometheus -> Alertmanager -> Slack（テストアラート受信OK）\n  - UFW で 9090/3000 は 127.0.0.1 限定、外部公開せず（トンネル前提）\n  - バックアップ: /root/inkaritsu/backup/monitoring_*.tgz 作成・cron 追加（/etc/cron.d/inkaritsu-monitor-backup）\n  - Grafana 管理者PWリセット用スクリプト作成：/root/bin/grafana-reset-admin\n■ 運用メモ\n  - ローカル閲覧: PowerShell で SSH トンネル再張り\n    ssh -i $env:USERPROFILE\\.ssh\\inkaritsu_ed25519 -NT \\\n        -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes \\\n        -L 33000:127.0.0.1:3000 root@160.251.167.44\n■ 次回TODO\n  - “NoScrape5m” 等の健全性アラートを本番用に整備\n  - Trading 側メトリクス追加（必要なら）とダッシュボード微調整\n  - 週次/月次でバックアップの復元テスト\n\n【GitOps/コンテナ移行 作業記録｜2025-08-14 22:20:27 JST】\n■ 正本リポ\n  - repo: github.com/conquestichi/inga-control\n  - commit: ef37c55\n\n■ きょう実施\n  - デプロイ鍵(読取専用) 作成・登録 → リモートを SSH(Deploy Key) に切替\n  - GitOps puller 導入：/usr/local/bin/inga-pull-apply ＋ inga-puller.timer(3分毎)\n  - policy/guard.yaml 追加（±15% / for+5m / rpm+20% / 2回/h / TTL=60m）\n    hash: 8d201175a0b5f25c015c63f22b9e151b3abe9a47\n  - PR作成→マージ→自動反映確認（timerで pull→検証→反映）\n\n■ 自動反映（timer）\n  - timer: active / next: 3d 11h 27min 52.128318s\n  - last pull: 2025-08-14 22:17:49 [puller] no-change (ef37c555635a0ef36ff03e5eb4dccae0c3d1892a)\n\n■ ヘルス\n  - webhook: ready\n  - prometheus: OK\n  - grafana: ok\n\n■ 次アクション（候補）\n  - PRテンプレ導入（提案の必須項目：目的/差分/根拠/ガード判定/ロールバック）\n  - Grafanaに version 表示（commit / params hash / image tag）\n  - INKARITSU_SLACK_WEBHOOK を設定し、pull適用時に短SHAを通知\n\n[2025-08-14 22:20:50] GitOps: PRをマージし自動反映確認済み (commit ef37c55)","reflect_tail_tail":"{\"message\": \"\\u30c6\\u30b9\\u30c8\\u30b5\\u30de\\u30e9\\u30a4\\u30ba\\u30ed\\u30b0\\u9001\\u4fe1\", \"source\": \"unit-test\"}\n{\n  \"source\": \"ops\",\n  \"type\": \"snapshot\",\n  \"ts\": \"2025-08-08 12:00:54\",\n  \"backup_dir\": \"inkaritsu_backup_20250808_115805\",\n  \"archive\": \"inkaritsu_backup_20250808_115805.tar.gz\",\n  \"note\": \"安定稼働スナップショット\"\n}\n","meta":{"last_tick":1755337289.586412}}
- metrics_sign: inkaritsu_requests_total{code="init"} 0
- queue: pending=5, done=1, failed=0
### 2025-08-18T11:24:42+0900　記憶読み込み完了（ChatGPT側）
- room: 新チャットルーム_20250818-1124

### 2025-08-18T11:25:41+0900　記憶読み込み完了（ChatGPT側）
- room: 新チャットルーム_20250818-1125

### 2025-08-21T23:15:37+0900 Handover（to: 新チャットルーム）
- snap: /root/inkaritsu/memory/handover-2025-08-21T14:15:37Z.tgz
- timers: healthcheck / reflect-trim / memory-snapshot / disk-guard / metrics（のみ）
- masked: agent / deploy / recovery / **reflector** / **summarizer** / morning（維持）
- DRY: INKARITSU_DRY_RUN=true, DRY_RUN=true（反映済）
- keys: OPENAI/INKARITSU/X → 長さのみ検証（本文は未記録）
- control: Screener/ドラフト群/オフラインツール PR済（no-runtime）
- ritsu_core: screener/validator/paper stub（flag=OFF, NO-OP）
## 2025-08-21T23:23:45+09:00 Handover fixed
- masks kept; minimal timers; DRY; control CHECKS(B)/offline; ritsu stubs OFF; 08:40 SAFE report

[2025-08-23 JST] 新チャットルーム：Phase Plan v1.1 を採用。
- Agent v1.1（jobs.json: {path,mode,message,model,content}／タブ禁止・末尾LF）
- Phase 2 機能：Backtest 30d, Metrics偏りアラート, ReleaseNotes+ハイライト, Logrotate
- タイマー：policy 11:25 / metrics 11:30 / RN+ 11:35 / backtest 11:40 / bias 11:31(*任意)
- Slack threads key：policy/metrics/release/backtest/agent 固定
[2025-08-23 JST] Agent v1.2: .sh/.py 自動+x、pyc抑止（temp compile）、bin/.gitignore 追加。Backtest/Bias/RN+ を specs で適用、手動一発確認OK。
[2025-08-23 JST] Backtest: daily に JSON空/破損フォールバックを追加（stderr→log）。スモークscores投入で動作確認。
[2025-08-23 JST] cards: id/name mismatch 自動修整ジョブ追加（cards_fix_names.py）。ファイル名の <id> を正準に YAML(id,name) を統一。
[2025-08-23 JST] Backtest安定（fallback & file JSON）。cards: id/name 統一（found=67, changed=67）。runtime/binを正本とし、dev-agentはpost-installで配備。
[2025-08-23 JST] RN+ highlight を前方一致判定に変更（regex撤廃）し、awkの '\:' 警告を静音化。
[2025-08-23 JST] 方針固定：構築はエージェントモード最優先（jobs.json→dev-agent→post-install→dev-tests）。Bias alert はCSV直読みに置換（MDはフォールバック）。
[2025-08-23 JST] metrics: Backtest Top5(30d) をダッシュボードに自動差し込み。11:30:20 timer で毎日反映。マーカー置換で冪等。
[2025-08-23 JST] metrics_backtest_insert: awk→sed範囲削除に変更。旧エラーノイズ(awk: cmd. line)も除去して静音・冪等化。
[2025-08-23 JST] policy_counts exporter を堅牢化（Bash安全版・side集計/ダッシュボード%フォールバック）。11:24:40 timer 導入。Bias は CSV 直読みに統一。
[2025-08-23 JST] RN+ highlight: Slack要約は bullet 先頭5行のみ（マーカー除外）。11:35:20 timer を追加。
[2025-08-23 JST] metrics chain v1.2：metrics/retry＋insert待機を追加。dev-tests は shellcheck 連携（存在時のみ）。
[2025-08-23 JST] metrics_backtest_insert: JSON を引数渡し→stdinパイプに修正。JSONDecodeError解消、sed範囲削除で静音維持。
[2025-08-23 JST] metrics: Backtest Top5 SVG 自動添付（idempotent）。チェーンに svg ステップを追加。tailは `tail -n 40` を使用。
[2025-08-23 JST] scores_snapshot 自動生成を導入（memory/manual/cards の順で取り込み・無い日は0.0で生成）。11:10 JST timer、チェーンv1.5に backtest前の生成を追加。
[2025-08-23 JST] metrics_dashboard exitfix: 同パスを wrapper 化し、freshness(≤300s) を満たせば 0 で返す。タイマー/チェーンとも WARN を出さず安定運転。
