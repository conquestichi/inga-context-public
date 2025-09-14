---
title: POINTERS (public <-> local)
owner: ops
updated: 2025-09-14T13:03:50Z
tags: [pointers, inventory]
---

## Public (GitHub Pages)
- Base: https://conquestichi.github.io/inga-context-public
- Raw : https://raw.githubusercontent.com/conquestichi/inga-context-public/main
- Pages:
  - <https://conquestichi.github.io/inga-context-public/index.md>
  - <https://conquestichi.github.io/inga-context-public/AGENTS.md>
  - <https://conquestichi.github.io/inga-context-public/ARCHITECTURE.md>
  - <https://conquestichi.github.io/inga-context-public/TARGETS.md>
  - <https://conquestichi.github.io/inga-context-public/POINTERS.md>
  - <https://conquestichi.github.io/inga-context-public/HUB.md>

## Local (VM)
- Context dir : /root/inga-control/.context
- Publish work: /root/inga-control/.ctx-public
- Hub inbox   : /root/inkaritsu/memory/hub_jobs/incoming/   (\*.content)
- Queue (json): /root/inga-control/agent_queue/{pending,processing,done,failed}/

## Operations
- Rebuild & push (context) : `/usr/local/bin/ctxctl rebuild`
- Publish (safe repeatable) : `/usr/local/bin/ctxctl publish`
- Status: `/usr/local/bin/ctxctl status`
