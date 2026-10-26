# Week 2 — Mini-SOC in a Box

Week 2 adds application-log correlation, Linux/Windows file integrity monitoring, Suricata IDS and security configuration/vulnerability assessment to the Week 1 host-only SOC.

| VM | Lab IP | Services |
|---|---|---|
| siem-host | 10.10.10.10 | Wazuh 4.14.8 Manager, Indexer, Dashboard |
| ubuntu-web | 10.10.10.20 | Apache, Wazuh agent, Suricata 7.0.3 |
| win-client | 10.10.10.30 | Windows 10 Pro, Wazuh agent, Sysmon |

## Verified results

1. Custom LabShop decoder parses LOGIN_FAILED events; Wazuh rule 100102 (level 5) detects individual failed logins and rule 100103 (level 12) correlates five attempts from the same IP within 60 seconds (MITRE T1110).
2. Linux real-time FIM on /var/www/html and Windows real-time FIM on C:\LabShopData: added (554), modified (550), deleted (553), including content diff.
3. Windows scheduled Registry FIM detected HKLM\SOFTWARE\LabShop Mode baseline → modified (750). A Linux scheduled /etc test used a temporary 60-second interval, after which 43200 seconds was restored.
4. Suricata captured on ens34 and detected HTTP /admin (signature 1000001). Wazuh collected eve.json and generated rule 100110 (level 10). Normal GET / was a negative test. Temporary NAT was removed.
5. Ubuntu CIS SCA changed 119/118/42 (50%) to 121/116/42 (51%) through checks 35547 and 35548. Windows CIS SCA: 116 passed, 303 failed, 5 N/A (27%).
6. Wazuh vulnerability inventory was ranked by CVSS for both agents; top selected CVEs appear in findings.md. w2-start and w2-done VMware snapshots exist for all three VMs.

This directory includes curated evidence and a short, chronological A4 Word report. No passwords, keys or credential-bearing Wazuh Docker Compose files are supplied.
