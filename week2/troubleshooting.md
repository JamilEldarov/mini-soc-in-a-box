# Troubleshooting

| Issue | Cause and resolution |
|---|---|
| Malformed Wazuh agent XML | A duplicate root/closing element caused `junk after document element`; corrected structure and validated logcollector. |
| Wazuh rule 100102 failed validation | Matching `action` as a static field was invalid; changed to `<field name="action" type="pcre2">`. |
| Unexpected logtest decoding | Accidentally pasted two syslog events together; entered each line separately. |
| Windows Registry alert was delayed | Registry FIM runs on a schedule (300 seconds), unlike realtime folder monitoring. |
| Linux scheduled FIM test was too slow | Temporarily changed from 43200 seconds to 60 seconds and restored it after verification. |
| Suricata failed to start | Default interface `eth0` didn't exist; changed AF_PACKET interface to `ens34`. |
| Suricata loaded no signatures | Added a local `labshop.rules` and set the absolute rule path in suricata.yaml. |
| Windows vulnerability inventory blank | Ubuntu-specific `agent.id:001` filter conflicted with win-client; opened the agent 002 view. |
