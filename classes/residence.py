from classes.time_slot import TimeSlot


class Residence:
    def __init__(self, unique_name: str, address: str, phone_number: str, level_of_care: int, task: str, time_expense: float, comment: str, open_time_slots: list[TimeSlot], distances: list['Distance']):
        self.unique_name = unique_name
        self.address = address
        self.phone_number = phone_number
        self.level_of_care = level_of_care
        self.task = task
        self.time_expense = time_expense
        self.comment = comment
        self.open_time_slots = open_time_slots
        self.distances = distances

    def __str__(self) -> str:
        return f"Residence: {self.unique_name}, Address: {self.address}, Phone Number: {self.phone_number}, Care Level: {self.level_of_care}, Task: {self.task}, Time Expense: {self.time_expense}, Comment: {self.comment}, Time Slots: {'; '.join(map(TimeSlot.__str__, self.open_time_slots))}, Distances: {', '.join(map(Distance.__str__, self.distances))}"

    def get_unique_name(self) -> str:
        return self.unique_name


class Distance:
    def __init__(self, destination: Residence, distance: float):
        self.destination = destination
        self.distance = distance

    def __str__(self) -> str:
        return f"Destination: {self.destination.unique_name}, Distance: {self.distance}"
