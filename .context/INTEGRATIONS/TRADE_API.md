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

## RC-3
- APPLYゲート: `ink_apply_gate.sh`（ENV/承認ファイル/時間帯/数量/銘柄/Kill-switch）
- 安全ラッパ: `ink_order_apply.sh`（`--apply true`時のみゲート照会。DENY=DRY、ALLOWでも既定は simulate=DRY）
- 承認/停止: `ink_go_live.sh`（TTL付き承認） / `ink_go_safe.sh`（即停止）
- ENV（既定安全）: `INK_APPLY=false`, `INK_APPLY_SIM_ONLY=true`, `INK_APPLY_HOURS=09-15`, `INK_APPLY_MAX_QTY=100`, `INK_APPLY_SYMBOLS="6501.T,7203.T,6758.T"`, `INK_APPLY_GO_TTL_SEC=1800`
### 例（安全な流れ）
1) 既定はDENY:  
   `ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_order_apply.sh buy 6501.T 1 --apply true --price-type MKT --tif DAY`
2) （本番化時）ENVで `INK_APPLY=true`/`INK_APPLY_SIM_ONLY=false` を明示＋ `ink_go_live.sh` 実行 → 少量で検証。  
3) 即停止は `ink_go_safe.sh`。
