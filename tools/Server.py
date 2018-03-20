import requests

WEATHER_URL = 'http://104.236.10.146:5001/weatherdata'
IMG_URL = 'http://104.236.10.146:5001/upload'


def post_weather(weather_data):
    r = requests.post(WEATHER_URL, weather_data)


def post_image(file_name):
    r = requests.post(IMG_URL, files={'weather.jpg': open(file_name, 'rb')})
