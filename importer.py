import json
from classes.careworker import Careworker
from classes.residence import Residence
from classes.distance import Distance
from classes.time_slot import TimeSlot
from datetime import time


def import_careworkers(json_file_path) -> list[Careworker]:
    with open(json_file_path, "r") as file:
        data = json.load(file)

    careworkers = []
    for cw_data in data['careworkers']:
        working_hours = []
        for wh_data in cw_data['working_hours']:
            beginning = time.fromisoformat(wh_data['beginning'])
            end = time.fromisoformat(wh_data['end'])
            time_slot = TimeSlot(beginning=beginning, end=end)
            working_hours.append(time_slot)

        careworker = Careworker(
            unique_name=cw_data['unique_name'],
            phone_number=cw_data['phone_number'],
            level_of_care_competence=cw_data['level_of_care_competence'],
            comment=cw_data['comment'],
            maximum_working_hours=cw_data['maximum_working_hours'],
            working_hours=working_hours
        )
        careworkers.append(careworker)

    return careworkers


if __name__ == "__main__":
    careworkers = import_careworkers("data/careworkers.json")
    for cw in careworkers:
        print(f"Careworker: {cw.unique_name}, Max. working hours: {
              cw.maximum_working_hours}, Working Hours: {'; '.join(map(TimeSlot.__str__, cw.working_hours))}")
