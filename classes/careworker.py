from classes.time_slot import TimeSlot


class Careworker:
    def __init__(self, id: int, name: str, phone_number: str, level_of_care_competence: int, comment: str, maximum_working_hours: float, working_hours: list[TimeSlot]):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.level_of_care_competence = level_of_care_competence
        self.comment = comment
        self.maximum_working_hours = maximum_working_hours
        self.working_hours = working_hours

    def __str__(self) -> str:
        return f"Careworker ID: {self.id}, Name: {self.name}, Phone Number: {self.phone_number}, Care Competence: {self.level_of_care_competence}, Comment: {self.comment}, Maximum Hours: {self.maximum_working_hours}, Working Hours: {'; '.join(map(TimeSlot.__str__, self.working_hours))}"

    def to_dict(self) -> dict:
        dictionary = {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "level_of_care_competence": self.level_of_care_competence,
            "comment": self.comment,
            "maximum_working_hours": self.maximum_working_hours,
            "working_hours": list(map(TimeSlot.to_dict, self.working_hours))
        }
        return dictionary
