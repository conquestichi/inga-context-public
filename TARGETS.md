---
title: Targets / SLO
owner: ops
updated: 2025-09-14T13:00:23Z
---
Expected
- full auto from HUB .content to Runner; no manual steps
- failures observable with runbooks to self-heal

SLO
- content->pending latency p95 < 1m
- pending->done/failed p95 < 2m
- autopull/push success: daily > 99%

