import serial
import time
import struct
from datetime import datetime
import logging

LOGGING = logging.getLogger(__name__)


class Davis:
    def __init__(self):
        LOGGING.debug('Setting up Davis Interface...')

        self.conn = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)
        self.conn.write(b'\n')
        self.wind_speed = 0
        self.wind_dir = 0
        self.temp_outside = 0
        self.temp_inside = 0
        self.humidity = 0
        self.pressure = 0
        self.last_update = datetime.now()
        self.updated = False

        # init
        weather_data = self.get_weather_data()

        if weather_data:
            LOGGING.debug('Done setting up Davis!')
            return weather_data
        else:
            LOGGING.debug('FAILED! setting up Davis...')
        return None

    def close(self):
        self.conn.close()

    def readline(self):
        return self.conn.readline()

    def read(self, charNum):
        return self.conn.read(charNum)

    def clear(self):
        self.conn.flushOutput()
        self.conn.flushInput()

    def test(self):
        self.clear()
        self.conn.write(b'TEST\n')
        print self.readline()
        print self.readline()
        return

    def update_data(self):
        self.updated = False
        try:
            # wake up
            self.clear()
            self.conn.write(b'\n')
            time.sleep(0.5)

            self.clear()
            self.conn.write(b'LPS 2 1\n')
            time.sleep(2)

            # get data
            data = self.read(97)

            # parse data
            self.wind_speed = int(struct.unpack('b', data[15])[0])
            self.wind_dir = int(struct.unpack('h', (data[17] + data[18]))[0])
            self.temp_outside = int(struct.unpack('h', (data[13] + data[14]))[0]) / 10.0
            self.temp_inside = int(struct.unpack('h', (data[10] + data[11]))[0]) / 10.0
            self.humidity = int(struct.unpack('b', data[34])[0])
            self.pressure = int(struct.unpack('h', (data[8] + data[9]))[0]) / 1000.0

            # mark as updated
            self.updated = True
        except:
            LOGGING.debug("Failed to update data from davis")

    def get_weather_data(self):
        self.update_data()
        if self.updated:
            weather_data = {}
            weather_data['wind_spead'] = self.data.wind_speed
            weather_data['wind_direction'] = self.data.wind_dir
            weather_data['outside_temp'] = self.data.temp_outside
            weather_data['inside_temp'] = self.data.temp_inside
            weather_data['humidity'] = self.data.humidity
            weather_data['pressure'] = self.data.pressure

            return weather_data
        else:
            LOGGING.debug('Failed to update weather')
            return None
