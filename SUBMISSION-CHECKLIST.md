# Week 1 submission status / last-mile checklist

These are the grading requirements from the course brief. **Pass/partial/pending** status reflects screenshots supplied in the walkthrough, not anything assumed from missing evidence.

| ID | Requirement | Current evidence/status |
| --- | --- | --- |
| L1 | Three VMs and hardware allocations | VMs used throughout; siem-host VMware settings captured; add screenshot for the two endpoint allocations if required |
| L2 | Static host-only addresses, siem-host NAT only | Pass: isolation and address screenshots |
| L3 | All VMs can communicate, dashboard from host, correct clocks | Largely verified; Windows-to-both, ubuntu-to-siem tests and dashboard; time comparison verified; full all-pairs test can be repeated |
| L4 | Official Docker repository, kernel persists | Pass: install, Docker test, persistent sysctl |
| L5 | Two named snapshots per VM | `w1-clean-install` reported done; **`w1-done` and snapshot screenshots still pending** |
| W1 | Single-node Wazuh 4.14.x | Pass: 4.14.8 Docker containers |
| W2 | Dashboard HTTPS; certificate explanation | Pass: dashboard screenshot and README |
| W3 | Default admin password changed securely | New password applied; Filebeat fixed; **verify original default login fails** |
| W4 | Persistence across stop/start/reboot | Container restart and alert retention after reboot passed; **post-reboot Active-agents screenshot pending** |
| W5 | Idle memory per Wazuh container | Recorded single sample; optional repeat after idle period |
| A1 | Linux agent Active | Pass |
| A2 | Windows agent Active | Pass after stack restart; post-reboot screenshot pending |
| A3 | Sysmon with community config, event visible | Pass: custom Wazuh Notepad rule detects Sysmon process event |
| A4 | Apache default page reachable from Dell | Pass |
| V1 | Five induced events with rule desc/level/screenshot | All five indexed; **read and fill missing sudo and Windows rule fields** |
| V2 | Explain event path | Complete in architecture/event-flow.md |
| S1 | No passwords/keys/certs in Git; show .gitignore, check index | `.gitignore` + checker provided; **run scan on your staged Git files** |
| S2 | Endpoint VMs no permanent internet route | IPv4 isolation pass; optional check IPv6 routing and VMware adapter layout |
| D1 | Repo + README + architecture/ + evidence/ + journal | Files prepared; **publishing actual GitHub repo pending** |
| D2 | Correct start/stop order in README | Prepared |
| D3 | Journal at least five entries | Prepared: eight entries, grounded in observed lab work |

## Before declaring Week 1 complete

1. Finalize missing Wazuh rule descriptions/levels from Discover (no guessing).
2. Verify **both agents Active after reboot** and capture the proof.
3. On each VM, use **VMware → Snapshot → Take a Snapshot**, name it `w1-done`, then screenshot each VM's snapshot list showing both names.
4. Review README/journal for exact environment and your own phrasing and observations; screenshots should correspond to the text.
5. Initialize Git, `git add .`, run `python3 scripts/check_repo.py`, manually review the staged file paths and all screenshots, then commit and publish only if clean.
