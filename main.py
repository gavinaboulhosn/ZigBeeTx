from ZigBeeTx.TxController import *
from ZigBeeTx.packetqueue import PacketQueue
from ZigBeeTx.GUI import PortSelectGUI
from ZigBeeTx.threads import TxThread
import sys


def init_controller():
    # port_select = PortSelectGUI()
    # port_select.display()
    port = "/dev/tty.usbserial-AD01SSNN"
    print(port)
    txcont = TxController(port)
    txcont.connect()
    txcont.configure_remote()
    return txcont


def init_message():
    message = PacketQueue()
    message.read_csv()
    message.csv_task()
    return message

def main():
    tx = init_controller()
    print(tx.xbee.get_64bit_addr())
    message = init_message()
    txthread = TxThread(tx, message)
    txthread.start()

main()