## 現行モデル要約
- Endpoints: /ready, /status, /metrics, /notify/test
- Prometheus: scrape=15s, targets=8081(Webhook),9090(Prom)
- Alerting: Slack連携済、Down/Mismatch ほか
- Grafana: Inkaritsu モニタ（Auto refresh=10s）
- Runbook: make status / reload / test-alert / backup / record
