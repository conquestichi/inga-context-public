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

## RC-4
- **Canary apply**: `ink_apply_canary.sh`（チャンク送信・レート制限・health失敗で即SAFE）
- **SLO監視**: `ink_apply_slo_check.sh`（window内 失敗率/連続失敗で自動SAFE）。`inkaritsu-apply-slo.timer` が 15分ごとに実行
- 環境変数（既定値）:  
  `INK_CANARY_MAX_CHUNK=10` `INK_CANARY_CHUNK_SLEEP_SEC=3` `INK_RATE_MIN_SEC=0`  
  `INK_SLO_WINDOW_SEC=3600` `INK_SLO_MAX_FAIL_PCT=20` `INK_SLO_MAX_STREAK=3`
