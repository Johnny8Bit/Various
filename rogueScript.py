"""
Creates CSV with summary of all rogues reported by 9800 WLC

Input:
Output from the following 3 show commands, each in a separate text file
- show_ap_summary
- show_wireless_wps_rogue_ap_ssid_summary
- show_wireless_wps_rogue_ap_summary
Each file should be named with a matching site code and suffix corresponding to the command
e.g.
TEST-apsum.txt
TEST-roguessid.txt
TEST-rogueap.txt

Usage:
python roguescript.py TEST
"""

import re, csv, json, sys

site_code = sys.argv[1]

CSV_FILE_NAME = f"{site_code.upper()}.csv"

with open(f"{site_code}-apsum.txt", "r") as f:
    show_ap_summary = f.readlines()

with open(f"{site_code}-roguessid.txt", "r") as f:
    show_wireless_wps_rogue_ap_ssid_summary = f.readlines()

with open(f"{site_code}-rogueap.txt", "r") as f:
    show_wireless_wps_rogue_ap_summary = f.readlines()


rogues = {}
detectors = {}


for line in show_ap_summary:
    if not line.startswith("Load") and not line.startswith("Time") and not line.startswith("AP"):
        ap_summary = re.match(r"(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+", line)
        try:
            mac, name = ap_summary.group(5), ap_summary.group(1)
            detectors.update({mac:name})
        except AttributeError:
            pass


for line in show_wireless_wps_rogue_ap_ssid_summary:
    if not line.startswith("Load") and not line.startswith("Time") and not line.startswith("MAC"):
        rogue_ssid = re.match(r"(\S+)\s+(\S+)\s+(\S+)\s+?(.{,33})", line)
        try:
            mac = rogue_ssid.group(1)
            rogues[mac] = {}
            rogues[mac]["ssid"] = rogue_ssid.group(4).lstrip().rstrip()
        except AttributeError:
            pass


for line in show_wireless_wps_rogue_ap_summary:
    if not line.startswith("Load") and not line.startswith("Time") and not line.startswith("MAC"):
        rogue_ap = re.match(r"(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+", line)
        try:
            mac, detecting_radio = rogue_ap.group(1), rogue_ap.group(8)
            rogues[mac]["rssi"] = rogue_ap.group(9)
            rogues[mac]["last"] = rogue_ap.group(6)
            rogues[mac]["channel"] = rogue_ap.group(10)
            rogues[mac]["detectors"] = rogue_ap.group(4)
            rogues[mac]["detecting_mac"] = detecting_radio
            rogues[mac]["detecting_name"] = detectors[detecting_radio]
        except (AttributeError, KeyError):
            pass


with open(CSV_FILE_NAME, 'w', newline='') as csvfile:
    counter = 0
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Rogue MAC", "Rogue SSID", "Rogue RSSI", "Channel", "Detectors", "Last Heard", "Strongest Detector Name", "Strongest Detector MAC"])
    for rogue, meta in rogues.items():
        if len(meta) == 7: #Skip incomplete
            counter += 1
            csv_writer.writerow([rogue, meta["ssid"], meta["rssi"], meta["channel"], meta["detectors"], meta["last"], meta["detecting_name"], meta["detecting_mac"]])

print(f"\nExported {counter} rogues to CSV")
#print(json.dumps(rogues, indent=4))