from classes.careworker import Careworker
from classes.residence import Residence
import file_handling
import solving


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
                careworkers = file_handling.import_careworkers(
                    json_file_path=path)
                for cw in careworkers:
                    print(cw)
            case "2":
                path = input(
                    "Pfad angeben (data/careworkers.json): ") or "data/careworkers.json"
                file_handling.export_careworkers(
                    json_file_path=path, careworkers=careworkers)
            case "3":
                path = input(
                    "Pfad angeben (data/residences.json): ") or "data/residences.json"
                residences = file_handling.import_residences(
                    json_file_path=path)
                for res in residences:
                    print(res)
            case "4":
                path = input(
                    "Pfad angeben (data/residences.json): ") or "data/residences.json"
                file_handling.export_residences(
                    json_file_path=path, residences=residences)
            case "5":
                if residences and careworkers:
                    solving.optimize_route(residences=residences,
                                           careworkers=careworkers)
                else:
                    print("Zuerst Residenzen und Pflegekräfte importieren.")

            case "x":
                exit()
            case _:
                print(f"Fehlerhafte Eingabe: {choice}")


if __name__ == "__main__":
    main()
