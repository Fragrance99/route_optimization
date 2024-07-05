from typing import List
from classes.time_slot import TimeSlot


class Careworker:
    def __init__(self, unique_name: str, phone_number: str, level_of_care_competence: int, comment: str, maximum_working_hours: float, working_hours: List[TimeSlot]):
        self.unique_name = unique_name
        self.phone_number = phone_number
        self.level_of_care_competence = level_of_care_competence
        self.comment = comment
        self.maximum_working_hours = maximum_working_hours
        self.working_hours = working_hours

    def __str__(self) -> str:
        return f"Careworker: {self.unique_name}, Phone Number: {self.phone_number}, Care Competence: {self.level_of_care_competence}, Comment: {self.comment}, Maximum Hours: {self.maximum_working_hours}, Working Hours: {'; '.join(map(TimeSlot.__str__, self.working_hours))}"
