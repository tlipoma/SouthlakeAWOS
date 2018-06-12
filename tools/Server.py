import requests
import os

WEATHER_URL = 'http://www.southlakeweather.net/weatherdata'
IMG_URL = 'http://www.southlakeweather.net/upload'
#WEATHER_URL = 'http://0.0.0.0:5050/weatherdata'
#IMG_URL = 'http://0.0.0.0:5050/upload'
DEFAULT_IMAGE_LOCATION = 'images/weather.jpg'


def post_weather(weather_data):
    r = requests.post(WEATHER_URL, weather_data)
    print r.text


def post_image(file_name=DEFAULT_IMAGE_LOCATION):
    header = {'Content-Length': str(os.path.getsize(file_name))}
    r = requests.post(IMG_URL, headers=header, files={'weather.jpg': open(file_name, 'rb')})
    print r.text