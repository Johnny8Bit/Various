'''
Encodes & decodes DHCP option 43 HEX strings used for Cisco APs

Usage (Encode):
opt43.py <wlc_ip_1> <wlc_ip_2> <wlc_ip_N>

Usage (Decode):
opt43.py <option43_hex>


netpacket.net
'''
import sys

__author__ = 'Michal Kowalik'
__version__= '1.0'
__status__ = 'Prototype'

def end():
    print('\n** Encode option 43 HEX string')
    print('Usage: opt43.py <WLC_IP_1> <WLC_IP_2> <WLC_IP_n>')
    print('Space separated IPv4 Wireless LAN Controller addreses (x.x.x.x)\n')
    print('** Decode option 43 HEX string')
    print('Usage: opt43.py <OPTION43_HEX>')
    print('Start of string should be "f1"')
    sys.exit()

def encode():
    """From list of IP addresses returns encoded DHCP option 43 HEX string
    """
    var_value_list = []
    for wlc_ip in sys.argv[1:]:
        wlc_ip_split = wlc_ip.split('.')
        if len(wlc_ip_split) != 4: end()
        for item in wlc_ip_split:
            if not item.isdigit() or int(item) not in range(0, 256): end()
            hex_item = hex(int(item))[2:]
            if len(hex_item) == 1: hex_item = '0' + hex_item
            var_value_list.append(hex_item)
    var_value = ''.join(var_value_list)
    var_len = str(hex(len(sys.argv[1:]) * 4))[2:]
    if len(var_len) == 1: var_len = '0' + var_len
    var_type = 'f1'
    print('\noption 43 hex ' + var_type + var_len + var_value)

def decode():
    """From option 43 HEX string returns number of WLCs and their IP addresses
    """
    wlc_count = int(sys.argv[1][2:4], base=16)
    hex_string = sys.argv[1][4:]
    if wlc_count % 4 != 0: end()
    else: wlc_count = wlc_count / 4
    if len(hex_string) != wlc_count * 8: end()
    for char in hex_string:
        if not char.isdigit() and ord(char.upper()) not in range(65, 71): end()
    hex_list, dec_list = [], []
    while hex_string:
        hex_list.append(hex_string[:2])
        hex_string = hex_string[2:]
    for item in hex_list: dec_list.append(str(int(item, base=16)))
    print('\nNumber of WLCs:', int(wlc_count))
    while len(dec_list) > 0:
        wlc_ip = '.'.join(dec_list[0:4])
        dec_list = dec_list[4:]
        print(wlc_ip)

if __name__ == '__main__':
    if len(sys.argv) == 1: end()
    if sys.argv[1].upper().startswith('F1'): decode()
    else: encode()
