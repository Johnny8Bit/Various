'''
Base64 encodes Username : Password credentials

Usage: mybase64.py <username> <password>

netpacket.net
'''
import base64, sys

encoded = base64.b64encode(f"{sys.argv[1]}:{sys.argv[2]}".encode('UTF-8')).decode('ASCII')
print(encoded)
