import serial.tools.list_ports as list_ports
import serial
import logging

LOGGER = logging.getLogger(__name__)

SWITCH_PID = 29987
SWITCH_ON = 'A00101A2'.decode('hex')
SWITCH_OFF = 'A00100A1'.decode('hex')


class USBSwitch(object):
    def __init__(self):
        LOGGER.debug("Initializing USB switches")
        # Get switches
        self.switches = self.get_switch_ports()

        # Initialize Off
        self.switches_off()

    def get_switch_ports(self):
        _ports = list_ports.comports()
        switches = []
        for port in _ports:
            if port.pid == SWITCH_PID:
                switches.append(port.device)
        return switches

    def switches_off(self):
        for i in range(len(self.switches)):
            LOGGER.debug("Turning OFF switch %s" % (i))
            send_serial_command(self.switches[i], SWITCH_OFF)

    def switches_on(self):
        for i in range(len(self.switches)):
            LOGGER.debug("Turning ON switch %s" % (i))
            send_serial_command(self.switches[i], SWITCH_ON)


def send_serial_command(port, command):
    try:
        ser = serial.Serial(port, 9600)
        ser.write(command)
        ser.close()
    except:
        LOGGER.debug('Error in serial communications')
