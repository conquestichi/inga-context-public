# queue healthcheck
- counts:
  ls -1 /root/inga-control/agent_queue/{pending,processing,done,failed}/*.json 2>/dev/null | wc -l
- runner log:
  journalctl -u inkaritsu-agent-runner.service -n 120 --no-pager

