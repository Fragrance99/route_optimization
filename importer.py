import json
from datetime import time

from classes.time_slot import TimeSlot
from classes.careworker import Careworker
from classes.residence import Residence


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


def import_residences(json_file_path) -> list[Residence]:
    with open(json_file_path, "r") as file:
        data = json.load(file)

    residences = []
    for res_data in data['residences']:
        time_slots = []
        for ts_data in res_data['open_time_slots']:
            beginning = time.fromisoformat(ts_data['beginning'])
            end = time.fromisoformat(ts_data['end'])
            time_slot = TimeSlot(beginning=beginning, end=end)
            time_slots.append(time_slot)

        residence = Residence(
            unique_name=res_data['unique_name'],
            address=res_data['address'],
            phone_number=res_data['phone_number'],
            level_of_care=res_data['level_of_care'],
            task=res_data['task'],
            time_expense=res_data['time_expense'],
            comment=res_data['comment'],
            open_time_slots=time_slots,
            distances=[]
        )
        residences.append(residence)

    return residences


if __name__ == "__main__":
    careworkers = import_careworkers("data/careworkers.json")
    for cw in careworkers:
        print(cw)

    residences = import_residences("data/residences.json")
    for res in residences:
        print(res)
