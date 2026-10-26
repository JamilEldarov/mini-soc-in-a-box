# Configuration notes

The files in this folder are custom lab rules. Wazuh Manager paths: /var/ossec/etc/rules/labshop_rules.xml and /var/ossec/etc/rules/labshop_suricata_rules.xml. Suricata uses /etc/suricata/rules/labshop.rules and captures on ens34.

The original custom decoder labshop_decoder.xml has not been exported as a safe standalone file and is intentionally not fabricated here. In the lab it decoded action, dstuser, srcip from syslog-style events in /var/log/labshop/app.log.

Linux agent localfile: syslog /var/log/labshop/app.log and json /var/log/suricata/eve.json. FIM directory: /var/www/html realtime. Windows: C:\LabShopData realtime and HKLM\SOFTWARE\LabShop 64-bit Registry scheduled 300 seconds. Do not overwrite a full ossec.conf with these partial settings.
