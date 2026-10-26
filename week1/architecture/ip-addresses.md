# Week 1 network address and resource table

This table reflects the VMs built during the Week 1 lab and the screenshots captured in the lab walkthrough.

| Device | Operating system | Role | VMnet1 host-only IP | VMnet8 NAT | RAM | vCPU | Disk |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| Windows 11 physical laptop | Windows 11 | VMware host / lab browser | `10.10.10.1` **planned; host adapter not independently verified** | Physical host internet access | 32 GB total | Host CPU | 1 TB total |
| `siem-host` | Ubuntu Server 24.04.5 LTS | Wazuh 4.14.8 single-node Docker SIEM | `10.10.10.10/24` | VMnet8 DHCP, observed `192.168.121.144/24` (may change) | 16 GB | 6 | 250 GB |
| `ubuntu-web` | Ubuntu Server 24.04.5 LTS | Apache2 and Wazuh Linux agent | `10.10.10.20/24` | Removed after installation | 2 GB | 2 | 40 GB |
| `win-client` | Windows 10 Pro | Wazuh Windows agent + Sysmon | `10.10.10.30/24` | Removed after installation | 4 GB | 2 | 80 GB |

## Virtual network configuration

- **VMnet1:** host-only, `10.10.10.0/24`, netmask `255.255.255.0`, VMware DHCP disabled. Both monitored endpoints use **static IPv4 addresses** with **no default IPv4 route**.
- **VMnet8:** NAT, `192.168.121.0/24`, allows **only siem-host** permanent outbound internet access to retrieve packages and container images. The two endpoints had NAT adapters **temporarily during setup**; the adapters were removed after required software installation.
- **Services:** Wazuh dashboard: `https://10.10.10.10` (external TCP 443); agent events: TCP 1514; enrollment: TCP 1515; Apache: `http://10.10.10.20` (TCP 80). Agent traffic is limited to the host-only network in this lab.
- **Isolation scope:** This verifies the intended VMware adapter layout and absence of **default IPv4 routes** on the endpoint VMs. IPv6 internet routes and any other host forwarding arrangements are not independently audited in the supplied screenshots.

## Why isolate the lab?

The lab contains deliberately induced failed authentication attempts and is intended for future controlled testing. The host-only network prevents the two endpoints from having a direct internet route and keeps lab traffic separate from other networks. Do not use this lab to test systems you do not own or control.
