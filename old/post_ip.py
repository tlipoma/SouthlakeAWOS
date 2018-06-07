import netifaces as ni
import requests

SERVER = 'http://104.236.10.146:5001/postip'

# Get ip address
ip = ni.ifaddresses('wlan0')[2][0]['addr']

# Send ip
r = requests.post(SERVER, data={'ip_address': ip})
