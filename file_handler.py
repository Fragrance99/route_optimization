import json
from datetime import time

from classes.time_slot import TimeSlot
from classes.careworker import Careworker
from classes.residence import Distance, Residence


def import_careworkers(json_file_path: str) -> list[Careworker]:
    with open(json_file_path, "r") as file:
        data = json.load(file)

    careworkers: list[Careworker] = []
    for cw_data in data['careworkers']:
        working_hours = []
        for wh_data in cw_data['working_hours']:
            beginning = time.fromisoformat(wh_data['beginning'])
            end = time.fromisoformat(wh_data['end'])
            time_slot = TimeSlot(beginning=beginning, end=end)
            working_hours.append(time_slot)

        careworker = Careworker(
            id=cw_data['id'],
            name=cw_data['name'],
            phone_number=cw_data['phone_number'],
            level_of_care_competence=cw_data['level_of_care_competence'],
            comment=cw_data['comment'],
            maximum_working_hours=cw_data['maximum_working_hours'],
            working_hours=working_hours
        )
        careworkers.append(careworker)

    return careworkers


def export_careworkers(json_file_path: str, careworkers: list[Careworker]):
    if careworkers:
        data = {"careworkers": list(map(Careworker.to_dict, careworkers))}
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent='\t')


def import_residences(json_file_path: str) -> list[Residence]:
    with open(json_file_path, "r") as file:
        data = json.load(file)

    residences: list[Residence] = []
    for res_data in data['residences']:
        time_slots = []
        for ts_data in res_data['open_time_slots']:
            beginning = time.fromisoformat(ts_data['beginning'])
            end = time.fromisoformat(ts_data['end'])
            time_slot = TimeSlot(beginning=beginning, end=end)
            time_slots.append(time_slot)

        residence = Residence(
            id=res_data['id'],
            name=res_data['name'],
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
            if start_res.id == res_data['id']:
                # json entry for residence object found
                distances: list[Distance] = []
                for dest_data in res_data['distances']:
                    for dest_res in residences:
                        if dest_res.id == dest_data['destination_id']:
                            # found residence object entry in list -> create Distance object and append
                            distance = Distance(destination=dest_res,
                                                minutes_of_distance=dest_data['minutes_of_distance'])
                            distances.append(distance)
                start_res.add_distances(distances)

    return residences


def export_residences(json_file_path: str, residences: list[Residence]):
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
