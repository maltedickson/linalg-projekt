import json
from dataclasses import dataclass

import numpy as np
import station



def read_routes_from_file() -> dict[int, list[int]]:
    with open("routes.json") as f:
        data = json.load(f)
    return data["routes"]


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
    
    for i, station_id in enumerate(stations_list):
        print(i+1, stations[station_id])
    
    print(np.linalg.matrix_power(matrix, 2))

    v = np.zeros(len(stations), dtype=int)
    v[id_to_index[2673730]] = 1

    print("v:", v)

    from_stockholm = np.linalg.matrix_power(matrix, 2) @ v

    for i, col in enumerate(from_stockholm):
        if col != 0:
            print(stations[stations_list[i]].name)

    print(len(stations))
    print(len(from_stockholm))


if __name__ == "__main__":
    main()

