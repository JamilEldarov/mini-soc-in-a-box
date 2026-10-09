# Week 1 lab journal — LabShop Mini-SOC

> Journal entries reflect actions and outcomes shown in the lab walkthrough. Where a result was not documented, the entry does not claim it succeeded.

## 2026-10-09 — Entry 1: Installing and isolating the virtual machines

**Tried:** Installed Ubuntu Server 24.04.5 LTS in two VMware VMs, Windows 10 Pro in a third, created a VMnet1 host-only lab at `10.10.10.0/24`, and configured `.10`, `.20`, `.30` static addresses.

**Challenge:** The first Ubuntu host-only interface initially showed DOWN and host-laptop ping to `10.10.10.1` failed. We determined the server's VMnet1 interface needed explicit Netplan configuration. Host-laptop ping may also be blocked by its firewall or a different adapter IP; we did not treat this as conclusive network failure.

**Fix/test:** Added host-only Netplan configuration to `ens34`; tested endpoint-to-server connectivity. Windows `win-client` reached both Ubuntu VMs with 0% ping loss. Created `w1-clean-install` snapshots on all three VMs (snapshot-list evidence still needed).

**Lesson:** Build and verify network layers before deploying the SIEM.

## 2026-10-09 — Entry 2: Docker from the official Ubuntu repository

**Tried:** Installed packages needed for Docker and configured its official signing key and apt repository.

**Challenge:** First package command used an incorrect package name (`ca-certification`) and apt could not locate it.

**Fix/test:** Used the correct `ca-certificates` package, installed Docker Engine and Docker Compose, confirmed the service was active, ran the `hello-world` test successfully, and verified Compose v5.6.0. Confirmed and persistently set `vm.max_map_count=1048576` (minimum required 262144).

**Lesson:** Copy package names exactly and test foundational dependencies before adding applications.

## 2026-10-09 — Entry 3: Wazuh 4.14.8 Docker deployment and credentials

**Tried:** Cloned tag `v4.14.8` of the official Wazuh Docker repository, generated certificates, and started the single-node Manager/Indexer/Dashboard stack.

**Challenge:** After changing the admin password, Windows/Sysmon alerts were present in the Manager's `alerts.json` but not searchable in Discover. `filebeat test output` returned `401 Unauthorized`. NTP checks indicated clocks were sufficiently aligned.

**Fix/test:** Corrected Indexer credentials used by the Manager/Filebeat and recreated the Manager container; the command returned `talk to server... OK`. Alerts began appearing in `wazuh-alerts-*` Discover searches.

**Lesson:** A functioning dashboard and running containers don't prove alert forwarding. Test Filebeat authentication end to end.

## 2026-10-09 — Entry 4: Registering Linux and Windows agents

**Tried:** Installed Wazuh agent 4.14.8 on `ubuntu-web` and `win-client`; installed Apache2 on Linux and Sysmon on Windows.

**Challenge:** Running Windows MSI via `msiexec.exe /qn` followed immediately by `Start-Service WazuhSvc` initially returned service not found.

**Fix/test:** Waited for the installer via PowerShell `Start-Process ... -Wait -PassThru`; exit code `0`; WazuhSvc then showed Running. Linux agent appeared Active. Apache served the default web page at `http://10.10.10.20`. Windows agent subsequently registered and appeared in Wazuh.

**Lesson:** Silent installers may take time; use exit codes and service checks rather than guessing.

## 2026-10-09 — Entry 5: Sysmon process telemetry and custom detection

**Tried:** Started Notepad on Windows 10 and searched Discover for a process creation event.

**Challenge:** Notepad did not initially appear as an alert, even though Sysmon had recorded Event ID 1 locally. The standard Sysmon base process rule can be below the configured Wazuh alert threshold.

**Fix/test:** Added a **lab-only** custom Wazuh rule `100101` with level 5, matching `notepad.exe`; validated the rules and restarted the Manager. Discover showed a matching Notepad alert on `win-client`.

**Lesson:** Sysmon collection, Wazuh decoding, and alert thresholds are separate stages; missing dashboard alerts do not automatically indicate endpoint collection failure.

## 2026-10-09 — Entry 6: The five detection tests

**Tried/tested:**

1. Linux sudo: `sudo whoami` produced a Wazuh alert described as **Successful sudo to ROOT executed.**
2. Linux user: `sudo useradd -m -s /bin/bash w1labtest` produced built-in rule `5902`, level 8, **New user added to the system.**
3. Linux SSH failure: an intentionally incorrect SSH password from `siem-host` was logged by `ubuntu-web`, with Wazuh rule `5503`, level 5, **PAM: User login failed.**
4. Windows program execution: a deliberate `notepad.exe` start produced lab rule `100101`, level 5.
5. Windows failed logon: intentionally incorrect local `runas` password generated Windows Security Event ID `4625`, visible in Wazuh Discover.

**Lesson:** Use the event's actual Wazuh `rule.description` and `rule.level` for the final report; the Windows native Event ID is different from the Wazuh rule ID. Remaining TBD rule fields are identified in the README.

## 2026-10-09 — Entry 7: Final endpoint network isolation

**Tried:** Removed the temporary VMnet8 NAT adapters from both monitored endpoint VMs.

**Verified:** `ubuntu-web` kept `10.10.10.20`, had no default IPv4 route, reached `10.10.10.10`, and Apache and Wazuh agent remained active. `win-client` kept `10.10.10.30`, had no default IPv4 route, reached Wazuh port 1514, and its WazuhSvc and Sysmon64 services remained running.

**Lesson:** Remove unnecessary paths to external networks after dependency installation and verify monitoring continues across the isolated lab subnet.

## 2026-10-09 — Entry 8: Stop/start and reboot persistence

**Tried:** `sudo docker compose stop`, `sudo docker compose start`, and then `sudo reboot` on `siem-host`.

**Observed:** All three Wazuh containers stopped and started. Both agents appeared Active after stack restart. After the full host reboot at **15:57:06 UTC**, Docker was active, and all three Wazuh containers were already Up without manual intervention. Historical Notepad (`100101`) and Linux user (`5902`) alerts remained visible in Discover after reboot.

**Pending:** Capture a new screenshot showing both agents Active specifically **after** the full reboot. Take and capture final `w1-done` snapshots on all three VMs.

**Lesson:** Restart success must include data persistence, not just container liveness.

## Final submission follow-up

- [ ] Read back missing `rule.level` and `rule.description` for the sudo and Windows 4625 events.
- [ ] Check old Wazuh default password no longer logs in; no password values in Git.
- [ ] Capture VMware snapshot tree for all three VMs, including `w1-clean-install` and `w1-done`.
- [ ] Confirm Active agent screenshot after the full SIEM VM reboot.
- [ ] Review screenshots and staged Git content before publishing.
