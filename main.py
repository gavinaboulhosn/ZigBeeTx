from ZigBeeTx.TxController import *
from ZigBeeTx.packetqueue import PacketQueue
from ZigBeeTx.threads import TxThread
import sys
import argparse
import os


def init_controller(port):
    txcont = TxController(port)
    txcont.connect()
    txcont.configure_remote()
    return txcont


def init_message():
    message = PacketQueue()
    message.read_csv()
    message.csv_task()
    return message

def parse_arguments():
    parser = argparse.ArgumentParser(description="Initialization for the Receiving ZigBee")
    parser.add_argument('--port', type=str,
                        help="ZigBee serial port")

    args = parser.parse_args()

    if args.port:
        with open(os.path.join(os.path.abspath('.'), 'config.ini'), 'w') as configfile:
            configfile.write(args.port)
            configfile.write("\n")
            port = args.port
        return port


    elif args.port is None:
        with open(os.path.join(os.path.abspath('.'), 'config.ini'), 'r') as configfile:
            config = configfile.readlines()
            if len(config) != 2:
                print("Configuration file is not formatted properly or does not exist")
                sys.exit(-1)
            else:
                port = config[0]


    return port

def main():
    port = parse_arguments()
    tx = init_controller(port)
    message = init_message()
    txthread = TxThread(tx, message)
    txthread.start()

main()