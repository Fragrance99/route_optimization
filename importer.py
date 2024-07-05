import json
from classes.careworker import Careworker
from classes.residence import Residence
from classes.distance import Distance
from classes.time_slot import TimeSlot


def import_careworkers(json_file_path):
    with open(json_file_path, "r") as file:
        data = json.load(file)

    careworkers = []
    for cw_data in data['careworkers']:
        pass
