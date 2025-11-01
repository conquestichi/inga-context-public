#!/usr/bin/env bash
set -Eeuo pipefail
BASE="/root/inga-control"
Q="$BASE/agent_queue"; P="$Q/pending"; D="$Q/done"; E="$Q/error"
mkdir -p "$P" "$D" "$E"
shopt -s nullglob
cnt=0
for f in "$P"/*.json; do
  if python3 /root/inga-context-public/tools/route_event.py "$f"; then
    mv -f "$f" "$D/"
  else
    mv -f "$f" "$E/"
  fi
  cnt=$((cnt+1))
done
echo "[route] processed=$cnt"
