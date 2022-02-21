from properties import *


class Lifetime:
    def __init__(self, interval):
        self.interval = interval
        self.init_time = Properties.time
        begin, end = self.interval
        if begin is None:
            begin = 0
        if end is None:
            end = float('inf')
        begin = int(begin)
        if end < float('inf'):
            end = int(end)
        self.interval = (begin, end)

    def get_valid_time(self):
        t = Properties.time - self.init_time
        begin, end = self.interval
        if t < begin:
            t = begin
        if t > end:
            t = end
        return t - begin

    def get_relative_time(self):
        t = Properties.time - self.init_time
        begin, end = self.interval
        return t - begin

    def valid(self):
        t = Properties.time - self.init_time
        begin, end = self.interval
        if begin <= t <= end:
            return True
        return False

