import davis
import netifaces as ni
import requests

SERVER = 'http://104.236.10.146:5001/weatherdata'

# build data
data = davis.Davis()
weather_data = {}
weather_data['wind_spead'] = data.wind_speed
weather_data['wind_direction'] = data.wind_dir
weather_data['outside_temp'] = data.temp_outside
weather_data['inside_temp'] = data.temp_inside
weather_data['humidity'] = data.humidity
weather_data['pressure'] = data.pressure

'''
print data.wind_speed
print data.wind_dir
print data.temp_outside
print data.temp_inside
print data.humidity
print data.pressure
'''

# close serial to conserve
data.close()

# send data
r = requests.post(SERVER, weather_data)

