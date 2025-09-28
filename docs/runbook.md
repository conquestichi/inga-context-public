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

## 運用コマンド（ops.sh）
/root/bin/ops.sh health # まとめ見
/root/bin/ops.sh timers # タイマー
/root/bin/ops.sh push-dry # SSH push の検証
/root/bin/ops.sh notify-daily # KPI通知（rich）
/root/bin/ops.sh notify-weekly # KPI通知（rich）
/root/bin/ops.sh metrics # メトリクスJSONを再生成して表示
/root/bin/ops.sh health-watch # しきい値監視を即時実行
/root/bin/ops.sh profile prod|stg# 通知プロファイル切替

markdown
コードをコピーする

## 監視しきい値（例）
- `/root/inkaritsu/config/ink_health.env` を編集。単位は秒。
- 既定: 日次6h / 週次36h / publish6h / guard2h、失敗回数は24hで {2,1,3,3}。

---

## 障害シナリオ別チェックリスト（v0.1）

### A. Git push 拒否 / start-limit-hit
**一次対応**
systemctl start ink_git_guard.service
journalctl -u ink_git_guard.service -n 50 --no-pager

markdown
コードをコピーする

**復旧ワンライナー（SSH固定化）**
REPO=/root/work/inga-context-public
SSH_CMD='ssh -i /root/.ssh/inkhub -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new'
git -C "$REPO" config --unset-all http.https://github.com/.extraheader 2>/dev/null || true
git -C "$REPO" config credential.helper "" || true
git config --global --unset-all http.https://github.com/.extraheader 2>/dev/null || true
git config --global --unset-all credential.helper 2>/dev/null || true
git -C "$REPO" remote set-url origin git@github.com:conquestichi/inga-context-public.git
install -d -m 700 /root/.ssh && ssh-keyscan -t rsa,ecdsa,ed25519 github.com >> /root/.ssh/known_hosts 2>/dev/null || true
export GIT_SSH_COMMAND="$SSH_CMD"

nginx
コードをコピーする

### B. publish に CSV が無い/古い
- Gate: `/root/bin/ink_hub_publish_gate.sh`
- Policy: `/root/inkaritsu/config/publish_policy.env`
  - `PUBLISH_FRESH_MAX_MIN`（分）
  - `PUBLISH_IF_EMPTY=skip|warn|fail`

### C. KPI 未生成
**確認**
journalctl -u inkaritsu-kpi-report.service -n 120 --no-pager
journalctl -u inkaritsu-kpi-weekly.service -n 120 --no-pager

markdown
コードをコピーする
**通知**
- 失敗時は OnFailure で Slack（未設定なら `/tmp/slack.out`）

### D. Slack 来ない / DRY 出力
tail -n 20 /tmp/slack.out
ls -l /root/inkaritsu/config/ink_notify.env
/root/bin/ink_profile.sh prod # or stg

nginx
コードをコピーする

### E. しきい値アラート（未成功経過/24h失敗回数）
- env: `/root/inkaritsu/config/ink_health.env`
- 即時チェック: `/root/bin/ops.sh health-watch`
- メトリクス: `/root/bin/ops.sh metrics`

### G. 診断パッケージ
/root/bin/ops.sh diag

例: /root/inkaritsu/reports/YYYYmmdd_HHMMSS_inga_diag.tar.gz
nginx
コードをコピーする

### Publish プロファイル運用
/root/bin/ops.sh profile-hub stg # publish を stg ブランチへ
/root/bin/ops.sh push-dry # 反映先ブランチを dry-run で確認
/root/bin/ops.sh profile-hub prod # 戻す

nginx
コードをコピーする

### 失敗通知（OnFailure → Slack）
- 仕組み: `inkaritsu-failure-notify@.service` + `OnFailure=...@%n.service`
- 通知先: `INKARITSU_SLACK_WEBHOOK_ERR`（未設定時は通常Webhook、無ければ `/tmp/slack.out`）
- 直近ログ: `journalctl -u <unit> -n 120` を添付
- 連投抑止: 既定 600 秒（`COOLDOWN_SEC`）

#### 手動テスト
MAX_LINES=30 COOLDOWN_SEC=0 /root/bin/ink_failure_notify.sh inkaritsu-hub-publish.service
tail -n 60 /tmp/slack.out

nginx
コードをコピーする
