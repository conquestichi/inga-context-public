# Inkaritsu – Trade API (minimal client, RC-1)
- Endpoints / Auth / 期待コードは従来通り（signal=200, webhook-dev=200, webhook=401）
- Auto prefix: "", /inkaritsu, /v1, /api （検出は /webhook/dev）
- Prefix キャッシュ: /tmp/inkaritsu_pfx（TTL=1800秒, env `INK_PFX_CACHE`, `INK_PFX_TTL`）

## CLI 例（DRY）
ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_order.sh buy 6501.T 100 --source doc
ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_order.sh sell 6501.T  50 --source doc
ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_order.sh cancel 6501.T 0 --cancel-id demo-0001 --source doc

## Python 関数 / 引数
--action buy|sell|cancel
--symbol 6501.T
--qty 100
--source inga
--dry true|false
--cancel-id <ID>
--env-path /root/inkaritsu/config/inkaritsu.env
--price-type MKT|LMT|...
--tif DAY|...
--client-order-id <ID>
--pfx-cache /tmp/inkaritsu_pfx
--pfx-ttl 1800

## クイックテスト
ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_trade_quicktest.sh

## RC-3.1
- 二名承認（可変）：`INK_APPLY_APPROVERS`（既定=2）。`ink_go_live.sh --who <name> [--ttl sec]` で `apply.ok.<name>` を発行。
- 監査ログ：`/var/log/inkaritsu/apply_audit.jsonl`（注文・ゲート判定・実効DRYを1行JSONで追記）。`ink_apply_audit.sh [N]` で参照。
- Slack通知（任意）：`INK_APPLY_AUDIT_SLACK=true` で ALLOW/DENY を投稿（Webhookは既存の *INKARITSU_SLACK_WEBHOOK / SLACK_WEBHOOK_URL / TBX_SLACK_WEBHOOK_URL* のいずれか）。
- ステータス：`ink_go_status.sh` で承認票と残TTL、Kill-switch を一覧。
