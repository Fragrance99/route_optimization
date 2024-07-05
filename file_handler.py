import json
from datetime import time
from typing import List

from classes.time_slot import TimeSlot
from classes.careworker import Careworker
from classes.residence import Distance, Residence


def import_careworkers(json_file_path: str) -> List[Careworker]:
    with open(json_file_path, "r") as file:
        data = json.load(file)

    careworkers: List[Careworker] = []
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


def export_careworkers(json_file_path: str, careworkers: List[Careworker]):
    if careworkers:
        data = {"careworkers": list(map(Careworker.to_dict, careworkers))}
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent='\t')


def import_residences(json_file_path: str) -> List[Residence]:
    with open(json_file_path, "r") as file:
        data = json.load(file)

    residences: List[Residence] = []
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
            minutes_of_time_expense=res_data['minutes_of_time_expense'],
            comment=res_data['comment'],
            open_time_slots=time_slots,
            distances=[]
        )
        residences.append(residence)

    for start_res in residences:
        for res_data in data['residences']:
            if start_res.get_unique_name() == res_data['unique_name']:
                # json entry for residence object found
                distances: List[Distance] = []
                for dest_data in res_data['distances']:
                    for dest_res in residences:
                        if dest_res.get_unique_name() == dest_data['destination']:
                            # found residence object entry in List -> create Distance object and append
                            distance = Distance(destination=dest_res,
                                                minutes_of_distance=dest_data['minutes_of_distance'])
                            distances.append(distance)
                start_res.add_distances(distances)

    return residences


def export_residences(json_file_path: str, residences: List[Residence]):
    if residences:
        data = {"residences": list(map(Residence.to_dict, residences))}
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent='\t')


# test
if __name__ == "__main__":
    careworkers = import_careworkers(json_file_path="data/careworkers.json")
    export_careworkers(json_file_path="data/careworkers.json",
                       careworkers=careworkers)
    for cw in careworkers:
        print(cw)

    print("")

    residences = import_residences("data/residences.json")
    export_residences(json_file_path="data/residences.json",
                      residences=residences)
    for res in residences:
        print(res)
