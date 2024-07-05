from classes.distance import Distance
from classes.time_slot import TimeSlot


class Residence:
    def __init__(self, unique_name: str, address: str, phone_number: str, level_of_care: int, task: str, time_expense: float, comment: str, open_time_slots: list[TimeSlot], distances: list[Distance]):
        self.unique_name = unique_name
        self.address = address
        self.phone_number = phone_number
        self.level_of_care = level_of_care
        self.task = task
        self.time_expense = time_expense
        self.comment = comment
        self.open_time_slots = open_time_slots
        self.distances = distances
