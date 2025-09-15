# deploy key rotate (ed25519)
- create: ssh-keygen -t ed25519 -N "" -f /root/.ssh/id_ed25519_ingacontrol -C "$(hostname)-ed25519"
- repo settings -> Deploy keys (Allow write)

