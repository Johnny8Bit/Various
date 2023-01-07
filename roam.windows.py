'''
Roaming script, print basic wireless parameters on Windows client
Saves output to CSV
"SSID:XXXXXXXX BSSID:XX:XX:XX:XX:XX:XX Channel:XX Signal:XX% TX:XXX"
Tested on Windows 10
netpacket.net
'''
from datetime import datetime
import subprocess, re, sys, time
from colorama import Fore, init

init(autoreset=True)
output_file_name = 'wifiroam.csv'
previous_bssid = None
roam_counter = 0
try:
#try/except block for file I/O operations
    output_file = open(output_file_name, "w+")
    #creates new file, overwriting existing, in folder from which the script is executed
except PermissionError:
    print('Error writing file')
    sys.exit()
    #exits on permission error when writing file
try:
#try/except block for clean exit on CTRL+C
    while True:
    #loop indefinitely
        try:
        #try/except block for output parse fail
            timestamp = str(datetime.now())[:-7]
            output = subprocess.check_output('netsh wlan show interfaces').decode('ascii')
            #assign result of netsh wlan show interfaces command to variable
            ssid = 'SSID:' + re.search(r'(SSID.+?:\s)(.+)', output).group(2).rstrip()
            bssid = 'BSSID:' + re.search(r'(BSSID.+?:\s)(.+)', output).group(2).rstrip()

            channel = 'Channel:' + re.search(r'(Channel.+?:\s)(.+)', output).group(2).rstrip()
            mode = 'Mode:' + re.search(r'(Radio type.+?:\s)(.+)', output).group(2).rstrip()
            rxrate = 'RX:' + re.search(r'(Receive rate.+?:\s)(.+)', output).group(2).rstrip()
            txrate = 'TX:' + re.search(r'(Transmit rate.+?:\s)(.+)', output).group(2).rstrip()
            signal = re.search(r'(Signal.+?:\s)(.+)', output).group(2).rstrip()
            signal = f"-{str(100-round(int(signal[:-1])/2))}"
            #search output for ssid, bssid, channel, txrate & signal and assign to variables
        except AttributeError:
            print('No output')
        else:
            #print results to screen if output was correctly parsed
            if bssid != previous_bssid:
                previous_bssid = bssid
                roam_counter += 1
            if roam_counter % 2 == 0:
                print(timestamp, ssid, Fore.CYAN + bssid, channel, mode, signal, rxrate, txrate)
                colour_change = False
            else:
                print(timestamp, ssid, Fore.YELLOW + bssid, channel, mode, signal, rxrate, txrate)
            output_file.write(f"{timestamp},{ssid},{bssid},{channel},{mode},{rxrate},{txrate},{signal}\n")
        time.sleep(0.1)
except KeyboardInterrupt:
    output_file.close()
    sys.exit()