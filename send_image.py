import requests

SERVER = 'http://104.236.10.146:5001/upload'

r = requests.post(SERVER, files={'weather.jpg': open('images/weather.jpg', 'rb')})

print r.text
