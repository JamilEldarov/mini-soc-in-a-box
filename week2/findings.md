# Week 2 security findings

## SCA

| Policy | Passed | Failed | Not applicable | Score |
|---|---:|---:|---:|---:|
| Ubuntu CIS initial | 119 | 118 | 42 | 50% |
| Ubuntu CIS after remediation | 121 | 116 | 42 | 51% |
| Windows 10 Enterprise CIS policy on Windows 10 Pro | 116 | 303 | 5 | 27% |

Ubuntu check 35547 (/etc/issue) and 35548 (/etc/issue.net) were changed from Failed to Passed with authorized-access login banners. Check 35510 (/tmp separate partition) was left unremediated to avoid repartitioning the existing VM.

## Wazuh vulnerability inventory

Ubuntu: 3,858 inventory hits; 184 Critical. Windows: 2,842 hits; 60 Critical. Hits are not necessarily confirmed exploitable CVEs.

| Agent | CVE | Wazuh CVSS 3.1 | Component / scanner details |
|---|---|---:|---|
| ubuntu-web | CVE-2026-74705 | 10.0 | Linux kernel 6.8.0-146.146, UDP tunnel segmentation use-after-free |
| ubuntu-web | CVE-2026-74612 | 10.0 | Same kernel, veth/XDP buffer-length flaw |
| ubuntu-web | CVE-2026-63795 | 10.0 | Same kernel, 9p filesystem |
| win-client | CVE-2026-57092 | 9.9 | Windows build 19045.3803; scanner threshold below 19045.7548 |
| win-client | CVE-2025-49708 | 9.9 | Same Windows build; threshold below 19045.6456 |
| win-client | CVE-2026-96924 | 9.8 | Same Windows build; threshold below 19045.7807 |

Exact Ubuntu Noble package fixes were not established by the captured Wazuh `Package default status` records; check the vendor advisories before claiming patch availability. No patching was performed during this exercise. Windows builds above Wazuh's thresholds may require appropriate Windows 10 servicing/ESU eligibility.
