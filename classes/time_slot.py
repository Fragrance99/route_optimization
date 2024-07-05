from datetime import time


class TimeSlot:
    def __init__(self, beginning: time, end: time):
        self.beginning = beginning
        self.end = end
