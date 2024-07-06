from datetime import time


def _time_to_minutes(time: time) -> int:
    return time.hour * 60 + time.minute


class TimeSlot:
    def __init__(self, beginning: time, end: time):
        self.beginning = beginning
        self.end = end

    def __str__(self) -> str:
        return f"Beginning: {self.beginning.isoformat()}, End: {self.end.isoformat()}"

    def to_dict(self) -> dict:
        dictionary = {
            "beginning": self.beginning.isoformat(),
            "end": self.end.isoformat()
        }
        return dictionary

    def to_tuple(self) -> tuple[int, int]:
        return (_time_to_minutes(self.beginning), _time_to_minutes(self.end))
