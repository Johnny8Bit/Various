"""
Connects to list of WLCs via SSH, checks for BadIPChecksum packets on all WLCs, displays output to screen in table format

WLC_IP {} : Specifies WLC IP address(es) and name(s)

Requires separate creds.py file with 'username' and 'password' variables
"""

import re, time, warnings
from datetime import datetime

from cryptography.utils import CryptographyDeprecationWarning
with warnings.catch_warnings(action="ignore", category=CryptographyDeprecationWarning):
    import paramiko

from tabulate import tabulate

from creds import *


WLC_IP = {"x.x.x.x": "mywlc"}

results = []

for IP in WLC_IP:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"WLC: {IP}")
    try:
        ssh.connect(IP, username=username, password=password, timeout=3)
    except TimeoutError:
        print("Timeout")
        continue

    remote_conn = ssh.invoke_shell()
    output = remote_conn.recv(1024)
    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clearing output.
    if remote_conn.recv_ready():
        output = remote_conn.recv(1024)

    remote_conn.send("show platform hardware chassis active qfp statistics drop\n")
    time.sleep(1)
    if remote_conn.recv_ready():
        output = str(remote_conn.recv(5012))
        output_list = re.split(r"\\r\\n", output)

    time.sleep(1)
    ssh.close()

    packets = "0"
    for line in output_list:
        if line.startswith("BadIpChecksum"):
            bad_checksum = re.match(r"(BadIpChecksum\s*)(\d*)(?=\s)", line)
            packets = bad_checksum.group(2)

    print(f"Number of BadIPChecksum packets: {packets}")
    results.append([WLC_IP[IP], packets])


results.sort(key=lambda x: int(x[1]), reverse=True)
headers = ["WLC", "BadIpChecksum"]
print("\n\n" + tabulate(results, headers=headers, tablefmt="rst"))
print(f"\n{str(datetime.now())[:-7]}")
