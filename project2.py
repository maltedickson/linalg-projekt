import json
from dataclasses import dataclass

import numpy as np
import station
from station import Station
from country_codes import country_codes

def read_routes_from_file() -> dict[int, list[int]]:
    with open("routes.json") as f:
        data = json.load(f)
    return data["routes"]

def search_station(stations: dict[int, Station]) -> int:
    codes = []
    for station in stations.values():
        if station.country_code not in codes:
            codes.append(station.country_code)
    for i, code in enumerate(codes):
        s = f"{code} {country_codes[code]}"
        print(s.ljust(20, " "), end="")
        if i % 2 == 1:
            print()
    start_country = input('Vilket land vill du starta i? Ange landskod: ').strip()
    stations_in_country = [station for station in stations.values() if station.country_code == start_country]
    for station in stations_in_country:
        print(station.name)
    start_station = input('Vilken station vill du starta i? Ange stationens namn: ').strip()
    return next(station for station in stations.values() if station.name == start_station).id

def transfer_trains():
    number_of_transfers = int(input('Hur många byten vill du göra? '))
    return number_of_transfers

def number_of_suggestions():
    number_of_suggestions = int(input('Hur många förslag vill du ha? '))
    return number_of_suggestions

def filter_destinations():
    filter = int(input('Vad vill du filtrera dina resultat efter? Ange 1 för population och 2 för fågelavstånd: '))
    if filter == 1:
        return "population"
    elif filter == 2:
        return "distance"

def station_distance(station1: Station, station2: Station) -> float:
    pass


def sort_destinations(destinations: list[Station], filter: str) -> list[Station]:
    if filter == "population":
        return sorted(destinations, key=lambda station: station.population, reverse=True)
    elif filter == "distance":
        return sorted(destinations, key=lambda station: station_distance(station, start_station))
        

def main():
    stations = station.read_stations_from_file()
    routes = read_routes_from_file()

    stations_list = [id for id in stations.keys()]
    stations_list.sort()

    id_to_index: dict[int, int] = dict()
    for i, id in enumerate(stations_list):
        id_to_index[id] = i


    matrix = np.zeros((len(stations), len(stations)), dtype=int)

    for i, station_id in enumerate(stations_list):
        for j, other_id in enumerate(stations_list):
            if other_id in routes[f"{station_id}"] or station_id in routes[f"{other_id}"]:
                matrix[i, j] = 1

    
    # print(np.linalg.matrix_power(matrix, 2))

    start_station_id = search_station(stations)

    v = np.zeros(len(stations), dtype=int)
    v[id_to_index[start_station_id]] = 1

    # print("v:", v)

    amount_of_transfers = transfer_trains()
    possible_destinations = np.linalg.matrix_power(matrix, amount_of_transfers) @ v

    count = 0
    for i, col in enumerate(possible_destinations):
        if col != 0:
            print(stations[stations_list[i]].name)
            count += 1
    print("Totalt antal stationer: ", len(stations))
    print("Antal destinationer: ", count)



if __name__ == "__main__":
    main()

