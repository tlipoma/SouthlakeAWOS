import pyttsx


class VoiceEngine(object):

    def __init__(self):
        self.voice_engine = pyttsx.init()
        self.voice_engine.setProperty('voice', 'english')
        self.voice_engine.setProperty('rate', 130)

    def speak_weather(self, weather_object, last_updated):
        s = 'South Lake Weather. '
        s += 'Last updated ' + str(last_updated.hour) + ":" + str(last_updated.minute) + '. '

        direction = str(int(weather_object['wind_direction']))
        direction = '0' + direction if len(direction) < 3 else direction
        speed = int(weather_object['average_wind_speed'])
        s += "Wind %s %s %s at %s %s knotts. " % (direction[0], direction[1], direction[2], speed / 10, speed % 10)

        s += "Altimeter %s. " % weather_object['pressure']
        self.voice_engine.say(s)
