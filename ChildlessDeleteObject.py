"""
Connects to list of WLCs via SSH, runs list of show commands, saves output in text file per WLC

WLC {} : Specifies WLC IP address and name
COMMANDS [] : Specifies list of commands to run

Requires separate creds.py file with 'username' and 'password' variables
"""

import time, warnings
from datetime import datetime

from cryptography.utils import CryptographyDeprecationWarning
with warnings.catch_warnings(action="ignore", category=CryptographyDeprecationWarning):
    import paramiko

from creds import *


WLC = {"x.x.x.x": "mywlc"}

COMMANDS = [
            "sh plat soft object- chas act F0 child",
            "sh plat soft object- chas sta F0 child",
            "sh plat soft capwap chassis active f0",
            "sh plat soft capwap chassis standby f0"
            ]


for ip in WLC:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"WLC: {WLC[ip]}")
    try:
        ssh.connect(ip, username=username, password=password, timeout=3)
    except TimeoutError:
        print("Timeout")
        continue

    remote_conn = ssh.invoke_shell()
    output = remote_conn.recv(8192)
    remote_conn.send("terminal length 0\n")
    time.sleep(1)
    
    if remote_conn.recv_ready(): # Clearing output.
        output = remote_conn.recv(1024)

    results = ""
    for command in COMMANDS:
        print(command)
        remote_conn.send(f"{command}\n")

        output = ""
        while not output.rstrip().endswith("#"):
            output += remote_conn.recv(8192).decode("utf-8")
         
        results = f"{results}\n{output}\n\n"

    filename = f"{WLC[ip]}-{str(datetime.now())[:-16].replace("-",".")}-{str(datetime.now())[-15:-7].replace(":",".")}.txt"
    with open(filename, "w") as f:
        f.write(results)

    print(filename)
    ssh.close()
