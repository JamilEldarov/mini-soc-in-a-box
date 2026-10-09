# Mini-SOC in a Box — Week 1

> **LabShop SOC capstone — Week 1:** Build an isolated virtual network and deploy Wazuh to collect, detect, and investigate events from a Linux web server and a Windows workstation. Work performed on private, user-owned VMware virtual machines.

**Platform:** Windows 11 host laptop · VMware Workstation Pro · Ubuntu Server 24.04.5 LTS · Windows 10 Pro · **Wazuh 4.14.8** single-node Docker deployment · Docker Compose **v5.6.0** (as observed during installation).

## What is built

![Week 1 architecture](architecture/network-diagram.png)

The lab contains **three VMs** on a **VMnet1 host-only** network (`10.10.10.0/24`). Only `siem-host` retains **VMnet8 NAT** for updates. The endpoints' temporary NAT adapters were removed after setup. See [address table and isolation notes](architecture/ip-addresses.md).

| VM | Role | IP (VMnet1) | RAM / vCPU / disk | Main components |
| --- | --- | --- | --- | --- |
| `siem-host` | Central SOC monitoring | `10.10.10.10` | 16 GB / 6 / 250 GB | Wazuh Manager + Indexer + Dashboard (4.14.8) in Docker |
| `ubuntu-web` | Web server / Linux endpoint | `10.10.10.20` | 2 GB / 2 / 40 GB | Apache2 + Wazuh agent 4.14.8 |
| `win-client` | Windows endpoint | `10.10.10.30` | 4 GB / 2 / 80 GB | Windows 10 Pro + Wazuh agent 4.14.8 + Sysmon |

Dashboard: `https://10.10.10.10` (self-signed certificate in this isolated lab). Web server: `http://10.10.10.20`.

**Security warning:** This is a lab, not a hardened internet-facing production deployment. Windows 10 is past normal support; it remains host-only. Do not direct attacks or scans at any non-lab machine.

## SIEM / EDR / XDR and the role of Wazuh

- **SIEM:** centralizes security event collection, correlation, search, and alerts.
- **EDR:** collects endpoint activity and supports endpoint-focused detection and response.
- **XDR:** correlates detections across endpoint and other security domains.
- **Wazuh in this lab:** agents collect endpoint telemetry; Manager decodes and applies rules; Indexer stores alerts; Dashboard provides investigation and visual search. Wazuh provides SIEM and XDR capabilities. See [an event's path](architecture/event-flow.md).

## Build summary and reproducibility

1. VMware Workstation Pro: created `siem-host`, `ubuntu-web`, and `win-client` with resource allocations shown above; snapshots called `w1-clean-install` taken on all three before Wazuh work (user-confirmed; **VMware snapshot-list screenshots are not yet provided**).
2. VMnet1 configured as a host-only `10.10.10.0/24` network, VMware DHCP off. Assigned static addresses: `.10`, `.20`, `.30`. Verified endpoint-to-SIEM connectivity. VMnet8 NAT provided temporary package downloads, then removed from both endpoints.
3. On Ubuntu `siem-host`, installed Docker Engine and the Compose plugin from Docker's official Ubuntu package repository; verified service active, `hello-world`, and Compose version.
4. Set persistent kernel requirement `vm.max_map_count=1048576`, which exceeds the required `262144`, in `/etc/sysctl.d/99-wazuh.conf`. Verified the value and Docker's active status after a reboot during setup.
5. Checked out official `wazuh/wazuh-docker` tag `v4.14.8`, entered its `single-node/` directory, generated TLS certificates, and started Manager, Indexer, and Dashboard containers. The indexer, Manager, and Dashboard all ran successfully.
6. Changed the Wazuh default admin credentials. Filebeat initially failed authentication after this with `401 Unauthorized`; corrected the Manager-side Indexer password configuration and recreated the Manager; `filebeat test output` subsequently returned `talk to server... OK`. **Do not store actual admin credentials or generated certificate material in this repository.**
7. Installed **Wazuh agent 4.14.8** on `ubuntu-web` (apt package version `4.14.8-1`), started/enabled it, and held its package version. Installed Apache2 and validated HTTP 200 and browser access.
8. Installed **Wazuh agent 4.14.8** on Windows 10 and Sysmon with the SwiftOnSecurity community XML configuration. Enabled the Wazuh `Microsoft-Windows-Sysmon/Operational` event channel collection. The Windows MSI installer initially needed a wait-for-completion retry.
9. Verified events in Discover and built a **lab-only custom rule `100101`**, level 5, to alert on `notepad.exe` process creation. The other event tests used built-in Wazuh rules.
10. Safely tested Docker stack stop/start, VM reboot, agent reconnection after stop/start, and **historical alert persistence after reboot**. All three Wazuh services restarted automatically after reboot.

**Reproducibility note:** The Wazuh Docker deployment configuration and its certificates were intentionally **not** copied into this public repository because the actual Compose file contains secrets. Use the official deployment from tag `v4.14.8`, then supply **your own secrets**. See [official Wazuh Docker deployment documentation](https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html) and [Docker installation guide](https://docs.docker.com/engine/install/ubuntu/).

## Lab start/stop runbook (in the correct order)

### Start

1. Start `siem-host` in VMware Workstation Pro.
2. Verify Wazuh containers in the `siem-host` Ubuntu shell:

   ```bash
   cd ~/wazuh-docker/single-node
   sudo systemctl is-active docker
   sudo docker compose ps
   ```

3. The three services auto-restarted after the observed host reboot. **If any are down**, start the existing stack (no volume deletion):

   ```bash
   sudo docker compose up -d
   ```

4. Wait for Wazuh Indexer and Dashboard readiness; open `https://10.10.10.10` on the Windows 11 host. A certificate warning is expected from the self-signed lab certificate; confirm the private IP before proceeding.
5. Start `ubuntu-web` and then `win-client` in VMware. The agents should start as services. Check **Endpoints → Agents** for both to become Active; verify Apache via `http://10.10.10.20`.
6. To confirm healthy forwarding if alerts disappear, run on `siem-host`:

   ```bash
   sudo docker exec single-node-wazuh.manager-1 filebeat test output
   ```

   Expected: `talk to server... OK`. Never post passwords or Compose config in issue screenshots.

### Stop

1. Power down endpoint VMs first, using their normal OS shutdown procedures.
2. On `siem-host`, stop the stack *without deleting its volumes*:

   ```bash
   cd ~/wazuh-docker/single-node
   sudo docker compose stop
   sudo docker compose ps -a
   ```

3. Shut down `siem-host` normally with `sudo poweroff` or through VMware.
4. To resume later, boot `siem-host`, then use `docker compose start` if existing containers are stopped, or `docker compose up -d` if necessary. **Never use `docker compose down -v`** unless intentionally destroying stored data.

### Recovery / useful commands

```bash
sudo docker compose ps                 # All services + their status
sudo docker compose logs --tail=100    # Recent container logs
sudo docker stats --no-stream          # Memory usage
sysctl vm.max_map_count                # Confirm indexer host requirement
```

## Week 1 acceptance evidence

The next table records the **five required, deliberately generated events**; rule descriptions and levels come from screenshots when visible. A custom lab-only rule was used for Notepad, and the remaining visible detections were native Wazuh rules.

| Required event | Agent | Observed Wazuh rule | Rule level | Evidence screenshot |
| --- | --- | --- | --- | --- |
| Failed SSH login | `ubuntu-web` | **5503** — PAM: User login failed. | **5** | [`w1-failed-ssh.png`](evidence/w1-failed-ssh.png) |
| `sudo whoami` | `ubuntu-web` | **Successful sudo to ROOT executed.**; rule ID **TBD** | **TBD: inspect the alert's `rule.level`** | [`w1-sudo-command.png`](evidence/w1-sudo-command.png) |
| Linux user `w1labtest` created | `ubuntu-web` | **5902** — New user added to the system. | **8** | [`w1-linux-user-created.png`](evidence/w1-linux-user-created.png) |
| Started `notepad.exe` (Sysmon Event ID 1) | `win-client` | **100101** — Lab test: Notepad process started on Windows (custom rule) | **5** (defined by custom rule) | [`w1-sysmon-process.png`](evidence/w1-sysmon-process.png) |
| Failed Windows login (`4625`) | `win-client` | **TBD: copy `rule.description` and `rule.id` from expanded alert** | **TBD: copy `rule.level`** | [`w1-failed-windows-login.png`](evidence/w1-failed-windows-login.png) |

**Do not substitute Windows Event ID `4625` for the Wazuh `rule.id` — they are different fields.** For the final submitted table, fill in the remaining `TBD` values from the actual alert records, without guessing.

### Other evidence

- [Three Wazuh containers](evidence/w1-wazuh-containers.png) and [Docker install](evidence/w1-docker-install.png)
- [Two agents Active after stop/start](evidence/w1-agents-active-after-stack-restart.png) (this screenshot **does not prove** post-reboot agent status)
- [Apache page](evidence/w1-apache-web-server.png)
- [Ubuntu IPv4 isolation](evidence/w1-ubuntu-isolation.png) and [Windows IPv4 isolation](evidence/w1-windows-isolation.png)
- [Docker stop/start](evidence/w1-stack-restart.png), [containers after reboot](evidence/w1-containers-after-reboot.png)
- [Notepad alert after reboot](evidence/w1-notepad-alert-after-reboot.png) and [Linux user alert after reboot](evidence/w1-user-alert-after-reboot.png)
- [All evidence and its status](evidence/README.md)

## Idle container memory (W5)

Captured via `sudo docker stats --no-stream` on `siem-host`, as a **single point-in-time measurement** (not a controlled average; repeat after idle period for a more representative benchmark):

| Wazuh 4.14.8 container | Observed memory |
| --- | ---: |
| `single-node-wazuh.dashboard-1` | **191.6 MiB** |
| `single-node-wazuh.manager-1` | **445.5 MiB** |
| `single-node-wazuh.indexer-1` | **1.41 GiB** |

Screenshot: [`evidence/w1-container-memory.png`](evidence/w1-container-memory.png).

## Persistence test (W4)

- `docker compose stop` stopped the three containers. `docker compose start` restarted them; both agents were subsequently seen as **Active**.
- `sudo reboot` restarted `siem-host`; observed boot time: **2026-10-09 15:57:06 UTC**. Docker service was active and Manager, Indexer, Dashboard were automatically Up, with **no manual compose start**.
- Previous Notepad rule `100101` and Linux user rule `5902` remained searchable in `wazuh-alerts-*` after reboot.
- **Pending final screenshot:** both agents showing Active **after the full host reboot**. A pre-reboot screenshot showing both Active is included, but should not be mislabeled as post-reboot proof.

See [journal.md](journal.md) for what worked, what failed, and what fixed it.

## Data security, Git hygiene and missing items

- `.gitignore` excludes private keys, certificates, credential-bearing Compose config, VM disks, and local secrets. Check the **actual Git index** before every push: `git diff --cached --name-only` and `git status --short`.
- Do not commit your real Wazuh `docker-compose.yml`, live `config/`, passwords, certificates, agent keys, or any token. Keep secrets outside the GitHub project.
- Screenshots were taken from the supplied lab walkthrough. **Review screenshots for personal details before publishing.** No credentials should be present in them.
- **Outstanding evidence:** VMware snapshot-list screenshots for **each** VM showing `w1-clean-install` and `w1-done`; final `w1-done` snapshots; post-reboot two-agent screenshot; verify old default Wazuh admin password no longer authenticates; fill remaining rule descriptions and levels.
- Windows evaluation expiry: **not supplied / record if using an evaluation image**.

## Safely publish

```bash
cd mini-soc-in-a-box
# Inspect BEFORE committing. Run from the project root.
git init
git add .
git status --short
git diff --cached --name-only
python3 scripts/check_repo.py
# If the checker succeeds and you have inspected screenshots:
git commit -m "Document Mini-SOC Week 1 lab"
# Create a private or public repository yourself, attach remote, and push after review.
```

The scripts checker provides a basic automated audit of the staged files, **not a guarantee** that no secret exists. Do a manual review.

## References

- [Week 1 course brief](#mini-soc-in-a-box--week-1) (source file provided with assignment; not republished in the repository)
- [Wazuh Docker deployment](https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html)
- [Wazuh agent installation for Linux](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-linux.html)
- [Docker Engine for Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [SwiftOnSecurity Sysmon configuration](https://github.com/SwiftOnSecurity/sysmon-config)
