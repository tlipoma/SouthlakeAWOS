from tools import Server
from tools import Camera
from tools import Davis

davis = Davis.Davis()
weather_data = davis.get_weather_data()

Camera.capture_and_save('images/weather.jpg')

Server.post_weather(weather_data)
Server.post_image('images/weather.jpg')
