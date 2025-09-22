#!/usr/bin/env bash
set -euo pipefail
cmd="${1:-help}"; shift || true
case "$cmd" in
  daily)   systemctl restart inkaritsu-kpi-report.service;;
  weekly)  systemctl restart inkaritsu-kpi-weekly.service;;
  publish) systemctl restart inkaritsu-hub-publish.service;;
  guard)   systemctl start   ink_git_guard.service;;
  timers)  systemctl list-timers | grep -E 'inkaritsu-(kpi-(report|weekly)|hub-publish|report)\.timer' || true;;
  push-dry) GIT_TRACE=1 git -C /root/work/inga-context-public push --dry-run -v origin HEAD:main | tail -n 30;;
  health)
    echo '--- KPI daily';  journalctl -u inkaritsu-kpi-report.service   -n 30 --no-pager || true
    echo '--- KPI weekly'; journalctl -u inkaritsu-kpi-weekly.service  -n 30 --no-pager || true
    echo '--- publish';    journalctl -u inkaritsu-hub-publish.service -n 50 --no-pager || true
    echo '--- guard';      journalctl -u ink_git_guard.service         -n 50 --no-pager || true;;
  *) echo "usage: $0 {daily|weekly|publish|guard|timers|push-dry|health}"; exit 2;;
esac
