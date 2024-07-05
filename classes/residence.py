from typing import List
from classes.time_slot import TimeSlot


class Residence:
    def __init__(self, unique_name: str, address: str, phone_number: str, level_of_care: int, task: str, minutes_of_time_expense: int, comment: str, open_time_slots: List[TimeSlot], distances: List['Distance']):
        self.unique_name = unique_name
        self.address = address
        self.phone_number = phone_number
        self.level_of_care = level_of_care
        self.task = task
        self.minutes_of_time_expense = minutes_of_time_expense
        self.comment = comment
        self.open_time_slots = open_time_slots
        self.distances = distances

    def __str__(self) -> str:
        return f"Residence: {self.unique_name}, Address: {self.address}, Phone Number: {self.phone_number}, Care Level: {self.level_of_care}, Task: {self.task}, Time Expense: {self.minutes_of_time_expense}, Comment: {self.comment}, Time Slots: {'; '.join(map(TimeSlot.__str__, self.open_time_slots))}, Distances: {', '.join(map(Distance.__str__, self.distances))}"

    def get_unique_name(self) -> str:
        return self.unique_name

    def add_distances(self, distances: List['Distance']):
        self.distances = distances

    def to_dict(self) -> dict:
        dictionary = {
            "unique_name": self.unique_name,
            "address": self.address,
            "phone_number": self.phone_number,
            "level_of_care": self.level_of_care,
            "task": self.task,
            "minutes_of_time_expense": self.minutes_of_time_expense,
            "comment": self.comment,
            "open_time_slots": list(map(TimeSlot.to_dict, self.open_time_slots)),
            "distances": list(map(Distance.to_dict, self.distances))
        }
        return dictionary


class Distance:
    def __init__(self, destination: Residence, minutes_of_distance: int):
        self.destination = destination
        self.minutes_of_distance = minutes_of_distance

    def __str__(self) -> str:
        return f"Destination: {self.destination.get_unique_name()}, Distance: {self.minutes_of_distance}"

    def to_dict(self) -> dict:
        dictionary = {
            "destination": self.destination.get_unique_name(),
            "minutes_of_distance": self.minutes_of_distance
        }
        return dictionary
