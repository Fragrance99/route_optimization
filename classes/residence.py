from classes.time_slot import TimeSlot


class Residence:
    def __init__(self, id: int, name: str, address: str, phone_number: str, level_of_care: int, task: str, minutes_of_time_expense: int, comment: str, open_time_slots: list[TimeSlot], distances: list['Distance']):
        self.id = id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.level_of_care = int(level_of_care)
        self.task = task
        self.minutes_of_time_expense = int(minutes_of_time_expense)
        self.comment = comment
        self.open_time_slots = open_time_slots
        self.distances = distances

    def get_time_slots_as_intervals(self) -> list[list[int]]:
        intervals: list[list[int]] = []
        for ts in self.open_time_slots:
            intervals.append(ts.to_list())
        return intervals

    def get_distance(self, dest_res: 'Residence') -> int:
        if (self.id == dest_res.id):
            return 0

        for dist_entry in self.distances:
            if (dest_res.id == dist_entry.destination.id):
                return dist_entry.minutes_of_distance

        # Fallback
        for dist_entry in dest_res.distances:
            if (self.id == dist_entry.destination.id):
                return dist_entry.minutes_of_distance

        # TODO nothing found -> error
        return -1

    def __str__(self) -> str:
        return f"Residence ID: {self.id}, Name: {self.name}, Address: {self.address}, Phone Number: {self.phone_number}, Care Level: {self.level_of_care}, Task: {self.task}, Time Expense: {self.minutes_of_time_expense}, Comment: {self.comment}, Time Slots: {'; '.join(map(TimeSlot.__str__, self.open_time_slots))}, Distances: {', '.join(map(Distance.__str__, self.distances))}"

    def add_distances(self, distances: list['Distance']):
        self.distances = distances

    def to_dict(self) -> dict:
        dictionary = {
            "id": self.id,
            "name": self.name,
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
        self.minutes_of_distance = int(minutes_of_distance)

    def __str__(self) -> str:
        return f"Destination: {self.destination.name} ({self.destination.id}), Distance: {self.minutes_of_distance}"

    def to_dict(self) -> dict:
        dictionary = {
            "destination_id": self.destination.id,
            "minutes_of_distance": self.minutes_of_distance
        }
        return dictionary
