# Evidence index — Week 1

All PNG images below are **copies of screenshots supplied during the lab walkthrough**, not simulated results. The caption states exactly what each screenshot supports.

| Screenshot | What it proves |
| --- | --- |
| [w1-vmware-virtual-network.png](w1-vmware-virtual-network.png) | VMware Virtual Network Editor: VMnet1 host-only 10.10.10.0/24, DHCP disabled; VMnet8 NAT. |
| [w1-siem-vm-settings.png](w1-siem-vm-settings.png) | siem-host VMware VM settings: 16 GB RAM, six vCPU, 250 GB disk; VMnet8 plus VMnet1. |
| [w1-docker-install.png](w1-docker-install.png) | Docker service active, hello-world test, and Docker Compose v5.6.0. |
| [w1-indexer-sysctl.png](w1-indexer-sysctl.png) | Kernel vm.max_map_count=1048576 and Docker service active (after applying persistent setting). |
| [w1-wazuh-containers.png](w1-wazuh-containers.png) | Three Wazuh 4.14.8 Docker containers up just after initial deployment. |
| [w1-dashboard-overview.png](w1-dashboard-overview.png) | Wazuh Dashboard accessible over HTTPS from the Windows 11 laptop. |
| [w1-container-memory.png](w1-container-memory.png) | Point-in-time Docker memory statistics for all three Wazuh services. |
| [w1-linux-agent-active.png](w1-linux-agent-active.png) | The ubuntu-web Linux agent shown Active in Wazuh (earlier screenshot). |
| [w1-apache-web-server.png](w1-apache-web-server.png) | Ubuntu Apache default page open in browser at http://10.10.10.20. |
| [w1-ubuntu-isolation.png](w1-ubuntu-isolation.png) | ubuntu-web retains 10.10.10.20; no default IPv4 route; manager ping and services work. |
| [w1-sysmon-process.png](w1-sysmon-process.png) | Custom Wazuh rule 100101 detects notepad.exe on win-client. |
| [w1-sudo-command.png](w1-sudo-command.png) | Wazuh alert for sudo /usr/bin/whoami on ubuntu-web. |
| [w1-linux-user-created.png](w1-linux-user-created.png) | Wazuh rule 5902 records new Linux user w1labtest on ubuntu-web. |
| [w1-failed-ssh.png](w1-failed-ssh.png) | Wazuh rule 5503 records failed SSH/PAM authentication on ubuntu-web. |
| [w1-failed-windows-login.png](w1-failed-windows-login.png) | Wazuh indexes Windows Security Event ID 4625 for failed logon on win-client. |
| [w1-windows-isolation.png](w1-windows-isolation.png) | win-client host-only IP, no default IPv4 route, reachable manager, WazuhSvc/Sysmon running. |
| [w1-stack-stop.png](w1-stack-stop.png) | All Wazuh containers stop after docker compose stop. |
| [w1-stack-restart.png](w1-stack-restart.png) | Wazuh containers start again after docker compose start. |
| [w1-agents-active-after-stack-restart.png](w1-agents-active-after-stack-restart.png) | Both agents Active after Docker stop/start (NOT proof of post-reboot agent status). |
| [w1-containers-after-reboot.png](w1-containers-after-reboot.png) | Host boot time, Docker active, Wazuh containers running automatically after VM reboot. |
| [w1-notepad-alert-after-reboot.png](w1-notepad-alert-after-reboot.png) | Historical Notepad rule 100101 searchable after reboot. |
| [w1-user-alert-after-reboot.png](w1-user-alert-after-reboot.png) | Historical user-add rule 5902 searchable after reboot. |


## Still needed from your live VMware/Wazuh environment

- **VMware snapshot list** for each VM: names `w1-clean-install` and **`w1-done`**. You said you took the clean snapshots, but did not supply snapshot-manager screenshots. Take the final snapshots only after completing and verifying Week 1.
- **Both agents Active after full `siem-host` reboot** (the included two-agent screenshot was captured after `docker compose start`, before the full reboot).
- **Screenshot showing `rule.description` and `rule.level`** for the sudo and Windows failed-login alerts, if not visible in the current captures.
- **Windows evaluation expiry date**, if an evaluation copy is used, for README traceability.

**Privacy review before a public GitHub push:** these are genuine endpoint screenshots and can contain usernames, paths, timestamps, process hashes, host IDs, and IP addresses. Review and redact anything sensitive before publishing. Never post passwords, exported certificates, private keys, or agent enrollment secrets.
