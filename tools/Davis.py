import serial.tools.list_ports as list_ports
import serial
import time
import struct
from datetime import datetime
import logging

LOGGING = logging.getLogger(__name__)

STATION_PID = 8963
STATION_VID = '7523'


class Davis(object):
    def __init__(self):
        LOGGING.debug('Setting up Davis Interface...')

        self.station_port = self.get_station_port()
        self.conn = None

        self.wind_speed = 0
        self.average_wind_speed = []
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
        else:
            LOGGING.debug('FAILED! setting up Davis...')

    def get_station_port(self):
        _ports = list_ports.comports()
        station = None
        for port in _ports:
            if type(port) == tuple:
                if port[2].split(':')[2] == STATION_VID:
                    station = port[0]
            else:
                if port.pid == STATION_PID:
                    station = (port.device)
        return station

    def close(self):
        if self.conn.is_open:
            self.conn.close()

    def open(self):
        if not self.conn:
            if not self.station_port:
                LOGGING.debug('No Weather station found! No port listed')
            else:
                self.conn = serial.Serial(self.station_port, 19200, timeout=1)
        if not self.conn.is_open:
            self.conn.open()
            self.conn.write(b'\n')

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
        # Open port
        self.open()

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
            self.average_wind_speed.append(self.wind_speed)
            if len(self.average_wind_speed) > 10:
                self.average_wind_speed.pop(0)
            self.wind_dir = int(struct.unpack('h', (data[17] + data[18]))[0])
            self.temp_outside = int(struct.unpack('h', (data[13] + data[14]))[0]) / 10.0
            self.temp_inside = int(struct.unpack('h', (data[10] + data[11]))[0]) / 10.0
            self.humidity = int(struct.unpack('b', data[34])[0])
            self.pressure = int(struct.unpack('h', (data[8] + data[9]))[0]) / 1000.0

            # mark as updated
            self.updated = True
        except:
            LOGGING.debug("Failed to update data from davis")

        # Close port
        self.close()

    def get_weather_data(self):
        self.update_data()
        if self.updated:
            weather_data = {}
            weather_data['wind_speed'] = self.wind_speed
            weather_data['average_wind_speed'] = sum(self.average_wind_speed) / float(len(self.average_wind_speed))
            weather_data['wind_direction'] = self.wind_dir
            weather_data['outside_temp'] = self.temp_outside
            weather_data['inside_temp'] = self.temp_inside
            weather_data['humidity'] = self.humidity
            weather_data['pressure'] = self.pressure

            return weather_data
        else:
            LOGGING.debug('Failed to update weather')
            return None
