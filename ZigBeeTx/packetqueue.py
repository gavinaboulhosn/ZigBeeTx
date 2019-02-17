import pandas as pd
from threading import Timer

class PacketQueue:
    def __init__(self, csv_file='../data.csv'):
        self.csv_file = csv_file
        self.prev_row = 0
        self.data_frame = None
        self.refresh_time = 4
        self.refresh_rate = 1/self.refresh_time
        self.packet = None
        self.resets = 0
        self.timeout = 10


    def read_csv(self):
        self.data_frame = pd.read_csv('../data.csv')
        self.packet = self.data_frame.get_values()

    def generate_message(self):
        if self.data_frame is None:
            self.read_csv()

        if self.packet_ready():
            try:
                packet = self.packet[self.prev_row]
                self.prev_row = self.prev_row + 1
                return ' '.join(str(x) for x in packet)

            except IndexError:
                pass

        else:
            return

    def packet_ready(self):
        try:
            return self.packet[self.prev_row] is not None
        except IndexError:
            self.resets += 1
            return False

    def csv_task(self):
        csvthread = Timer(self.refresh_rate, self.csv_task)
        csvthread.start()
        self.read_csv()
        if self.resets >= self.timeout:
            csvthread.cancel()
            return










