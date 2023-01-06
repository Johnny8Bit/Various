'''
Ping sweep one /24 IPv4 subnet, return responsive and unresponsive IPs

Useful as a quick check for available IP addresses
Pauses after first 10 IPs pinged
Not very fast..

netpacket.net
'''
import sys, subprocess, msvcrt

__author__ = 'Michal Kowalik'
__version__= '0.1'
__status__ = 'Prototype'

def end():
    print('Usage: pingsweep.py </24 IPv4 subnet using format x.x.x.0>')
    sys.exit()

def summary():
    print(ping_counter, 'IPs pinged in range', input_data)
    print(fail_counter, 'IPs did not respond within 50ms')
    print('\nUnresponsive IPs in', sys.argv[1], 'range :', str(unresponsive_ips))
    print('\nResponsive IPs in', sys.argv[1], 'range :', str(responsive_ips))
    sys.exit()

def check_if_valid(subnet_split):
    '''Checks if input is a valid IPv4 network
    '''
    if len(subnet_split) != 4 or subnet_split[3] != '0': end()
    for octet in range(0, len(subnet_split)):
        if subnet_split[octet].isdigit():
            subnet_split[octet] = int(subnet_split[octet])
        else: end()
    if subnet_split[0] not in range(1,255): end()
    if subnet_split[1] not in range(0, 256) or subnet_split[2] not in range(0, 256): end()
    for octet in range(0, len(subnet_split)):
        subnet_split[octet] = str(subnet_split[octet])

if __name__ == '__main__':
    if len(sys.argv) < 2: end()
    input_data = sys.argv[1]
    input_split = input_data.split('.')
    check_if_valid(input_split)
    ping_counter, fail_counter = 0, 0
    responsive_ips, unresponsive_ips = [], []
    try:
        for last_octet in range(1,255):
            if ping_counter == 10:
                print('\nContinue rest of subnet? (y/n): ', end='')
                continue_sweep = msvcrt.getch().decode("utf-8")
                print(continue_sweep)
                if continue_sweep.upper() != 'Y': summary()
            ip_address = input_split[0] + '.' + input_split[1] + '.' + input_split[2] + '.' + str(last_octet)
            ping_string = 'ping ' + ip_address + ' -w 50 -n 1'
            ping_counter += 1
            try:
                catch_output = subprocess.check_output(ping_string)
            except subprocess.CalledProcessError:
                fail_counter += 1
                unresponsive_ips.append(last_octet)
                print('No response from', ip_address)
                continue
            responsive_ips.append(last_octet)
    except KeyboardInterrupt:
        fail_counter += 1
        print('Interuppted by user')
    summary()
