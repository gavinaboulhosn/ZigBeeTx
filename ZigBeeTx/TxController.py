from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
from ZigBeeTx.ports import serial_ports
import serial
import time


class TxController:
    """ Class for managing serial connection with XBee Pro S1 """
    def __init__(self, port=None, baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.remote = None
        self.xbee = None

    def connect(self):
        try:
            if self.port is None:
                self.port = serial_ports()[0]    # will display text box later for options
                self.xbee = XBeeDevice(port=self.port, baud_rate=self.baud_rate)
                print(self.xbee.get_64bit_addr())
                self.xbee.open()
                return True

            elif self.port is not None:
                self.xbee = XBeeDevice(port=self.port, baud_rate=self.baud_rate)
                self.xbee.open()
                return True

            else:
                if self.is_open():
                    self.xbee.close()
                    print("Disconnected from {}".format(self.port))
                    return False

        except serial.SerialException:
            return False

    def is_open(self):
        return self.xbee.is_open()

    def disconnect(self):
        try:
            if self.is_open():
                self.xbee.close()
                return True
            else:
                return False
        except serial.SerialException:
            return False

    def send_synchronous(self, message):
        self.xbee.send_data(self.remote, message)

    def send_asynchronous(self, message):
        self.xbee.send_data_async(self.remote, message)

    def configure_remote(self):
        if self.xbee.get_64bit_addr() == "0013A2004093DF98":
            self.remote = RemoteXBeeDevice(self.xbee, XBee64BitAddress.from_hex_string('0013A2004093DFA1'))
        else:
            self.remote = RemoteXBeeDevice(self.xbee, XBee64BitAddress.from_hex_string("0013A2004093DF98"))

    @staticmethod
    def list_ports():
        return serial_ports()

    def __del__(self):
        if self.is_open():
            self.disconnect()
        del self








