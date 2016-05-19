import requests

SERVER = 'http://10.0.31.114:5000/upload'

r = requests.post(SERVER, files={'weather.jpg': open('images/weather.jpg', 'rb')})

print r.text
