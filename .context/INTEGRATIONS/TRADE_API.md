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

## RC-2
- CLIラッパに `--price-type` / `--tif` / `--client-order-id` を追加（Pythonへ引き渡し）
- 定期ヘルス（5分）とクイックテストをsystemd timer化（06–23のみ実行）
- 失敗時のみSlack通知（`INKARITSU_SLACK_WEBHOOK` / `SLACK_WEBHOOK_URL` / `TBX_SLACK_WEBHOOK_URL` のいずれか）
- Prefix検出は /tmp キャッシュ（TTL=1800秒、`INK_PFX_CACHE`/`INK_PFX_TTL`で調整）
- 期待値は従来通り：signal=200 / webhook-dev=200 / webhook=401（/webhookは無認証で401が正）

### 追加CLI例
ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_order.sh buy 6501.T 100 --price-type LMT --tif DAY --client-order-id rc2-$(date +%s)
ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_health_report.sh
