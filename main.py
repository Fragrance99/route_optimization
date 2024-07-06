from os import error
from classes.careworker import Careworker
from classes.residence import Residence
import file_handler

# TODO: change unique_name to name and add ID from 0 to ...


def main():
    careworkers = []
    residences = []

    while 1:
        print("")
        print("********* Hauptmenü *********")
        print("1: Pflegekräfte importieren")
        print("2: Pflegekräfte exportieren")
        print("3: Residenzen importieren")
        print("4: Residenzen exportieren")
        print("5: Routen optimieren")
        print("x: Beenden\n")

        choice = input("Option auswählen: ")

        match choice:
            case "1":
                path = input(
                    "Pfad angeben (data/careworkers.json): ") or "data/careworkers.json"
                careworkers = file_handler.import_careworkers(
                    json_file_path=path)
                for cw in careworkers:
                    print(cw)
            case "2":
                path = input(
                    "Pfad angeben (data/careworkers.json): ") or "data/careworkers.json"
                file_handler.export_careworkers(
                    json_file_path=path, careworkers=careworkers)
            case "3":
                path = input(
                    "Pfad angeben (data/residences.json): ") or "data/residences.json"
                residences = file_handler.import_residences(
                    json_file_path=path)
                for res in residences:
                    print(res)
            case "4":
                path = input(
                    "Pfad angeben (data/residences.json): ") or "data/residences.json"
                file_handler.export_residences(
                    json_file_path=path, residences=residences)
            case "5":
                if residences and careworkers:
                    optimize_route(residences=residences,
                                   careworkers=careworkers)
                else:
                    print("Zuerst Residenzen und Pflegekräfte importieren.")

            case "x":
                exit()
            case _:
                print(f"Fehlerhafte Eingabe: {choice}")


def optimize_route(residences: list[Residence], careworkers: list[Careworker]):
    for start in residences:
        for dest in residences:
            print(f"{start.name} -> {dest.name
                                     }: {start.get_distance(dest)}")


if __name__ == "__main__":
    main()
