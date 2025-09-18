# Inkaritsu – Trade API (minimal client)
- Base: STRATEGY_WEBHOOK_BASE（env）
- Auto prefix（優先）: "", /inkaritsu, /v1, /api
- Endpoints:
  - POST {BASE}{PFX}/signal      -> 200
  - POST {BASE}{PFX}/webhook/dev -> 200
  - POST {BASE}{PFX}/webhook     -> 401（本番は未認可想定）
- Auth: Authorization: Bearer <TOKEN|JWT>（/webhook は無認証で401を期待）

Payload（2形態）
A) {"action":"buy","symbol":"6501.T","qty":100,"source":"inga","dry":true,"cancel_id":"demo-0001"}
B) {"event":"order_signal","order":{"action":"BUY","symbol":"6501.T","qty":100,"price_type":"MKT","tif":"DAY","client_order_id":"demo-0001"},"dry_run":true,"source":"inga"}

CLI
ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_order.sh buy 6501.T 100 --source doc
ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_order.sh sell 6501.T  50 --source doc
ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_order.sh cancel 6501.T 0 --cancel-id demo-0001 --source doc

Health
ENV=/root/inkaritsu/config/inkaritsu.env /root/bin/ink_webhook_health.sh

注記: 初回RAW公開前の conquestichi/inga-context-public は 404 許容。公開後200へ遷移。
