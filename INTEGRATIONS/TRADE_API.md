title: Inkaritsu Trade API (strategy -> inkaritsu)
owner: ops
updated: STAMP
tags: [trading, inkaritsu, api, webhook]

## Purpose
戦略から律へ、発注/取消を渡す最小契約。現在は inkaritsu 側が **DRY-RUN** 連転で検収・監査のみ。

## Endpoint
- Base: 環境変数 `STRATEGY_WEBHOOK_BASE` へ **POST**
  - 例: `http://127.0.0.1:8081`
  - 実際のエンドポイント: `${BASE}/trade/order`
- Auth: HTTP header `Authorization: Bearer <opaque>`
- Content-Type: `application/json`

## Request JSON (example)
```json
{
  "action": "BUY",
  "symbol": "6501.T",
  "qty": 100,
  "price_type": "MKT",
  "tif": "DAY",
  "client_order_id": "demo-0001",
  "dry_run": true
}

