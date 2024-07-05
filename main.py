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
            case "x":
                exit()
            case _:
                print("Fehlerhafte Eingabe")


if __name__ == "__main__":
    main()
