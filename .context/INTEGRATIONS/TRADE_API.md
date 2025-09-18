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

## RC-4.1
- カナリア適応制御：成功で段階的に拡大（`INK_CANARY_SUCC_GROWTH_PCT`）、失敗で縮小（`INK_CANARY_FAIL_SHRINK_PCT`）＋指数バックオフ（`INK_CANARY_BACKOFF_BASE_SEC`～`_MAX_SEC`）＋ジッター（`INK_CANARY_JITTER_PCT`）。
- 時間当たりBudget（任意）：`INK_BUDGET_PER_HOUR_QTY`（成功分のみ消費。0=無効）。ファイル `/var/cache/inkaritsu/budget/<symbol>-YYYYMMDDHH.qty`。
- 既存：銘柄別レート制限 `INK_RATE_MIN_SEC`、失敗時 SAFE 化は従来通り。
