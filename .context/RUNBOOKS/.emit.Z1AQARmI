# git-autopush: recover
- status: systemctl status inkaritsu-autopush.service
- drop-in: /etc/systemd/system/inkaritsu-autopush.service.d/10-ssh.conf
- ssh test:
  env -i /usr/bin/ssh -F /root/.ssh/config -o BatchMode=yes -o IdentitiesOnly=yes -T git@github.com-ingacontrol || true
- recent log:
  journalctl -u inkaritsu-autopush.service -n 120 --no-pager

