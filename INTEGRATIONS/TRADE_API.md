title: INKARITSU Trade API (DRY-RUN)
owner: ops
updated: STAMP
tags: [trading, inkaritsu, api, webhook]

## Purpose
戦略 ⇒ 律（inkaritsu）への最小契約。現状は **DRY-RUN** で検証・監査のみ。

## Endpoints (prefix auto-detected)
`{PFX}` は OpenAPI (`/openapi.json`) から自動推定：`""` / `/inkaritsu` / `/v1` / `/api`。

- **POST** `{BASE}{PFX}/signal` — シグナル受信（**Bearer 必須**）
- **POST** `{BASE}{PFX}/webhook/dev` — 開発用エコー（**Bearer 必須**）
- **POST** `{BASE}{PFX}/webhook` — 本番面（現在は 401）

Auth: `Authorization: Bearer <token>`  
Content-Type: `application/json`

## Request JSON (common)
```json
{
  "event": "order_signal",
  "order": {
    "action": "BUY | SELL | CANCEL",
    "symbol": "6501.T",
    "qty": 100,
    "price_type": "MKT | LMT",
    "tif": "DAY | FAK | FOK",
    "client_order_id": "demo-0001",
    "cancel_client_order_id": ""
  },
  "dry_run": true,
  "source": "inga-gpt",
  "ts": "任意（ISO8601）"
}

