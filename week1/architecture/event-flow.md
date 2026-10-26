# Event journey: Windows process start to Wazuh dashboard

1. **Endpoint:** On `win-client`, a local program starts. Microsoft **Sysmon** observes the execution and writes **Event ID 1 (Process Create)** to the `Microsoft-Windows-Sysmon/Operational` Windows Event Log channel.
2. **Wazuh Agent:** The Windows Wazuh Agent, configured with an `eventchannel` `localfile` entry, collects this Sysmon record and forwards it to **Wazuh Manager** at `10.10.10.10` via the host-only network.
3. **Wazuh Manager / rules:** Manager decodes the message and applies detection rules. Default rules do not necessarily alert for every process. For the Week 1 test, the custom lab rule `100101` matched `notepad.exe` and emitted a **level 5** alert.
4. **Alert transfer:** Filebeat in the Wazuh Manager container reads the generated alert and authenticates to the **Wazuh Indexer** over TLS. During Week 1 this connection initially failed with `401 Unauthorized` after an admin credential update, and was subsequently fixed.
5. **Wazuh Indexer:** The Indexer stores the generated alert in a `wazuh-alerts-4.x-YYYY.MM.DD` index.
6. **Wazuh Dashboard:** On the physical Windows 11 laptop, the analyst opens `https://10.10.10.10` and searches **Explore → Discover**, `wazuh-alerts-*`, for `rule.id: "100101"`. The displayed record includes the agent, process, timestamp, rule description, and rule level.

**Four main Wazuh components:** Agent → Manager → Indexer → Dashboard. **Filebeat** is the forwarding service connecting Manager alerts to the Indexer.

For Linux examples, `ubuntu-web` sends system journal/authentication logs through its agent. A `useradd` event generated built-in rule `5902`; a failed SSH authentication generated rule `5503`.
