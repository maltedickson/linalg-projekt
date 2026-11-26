import json
from dataclasses import dataclass

#import matplotlib.pyplot as plt
import numpy as np
import requests
#from mpl_toolkits.basemap import Basemap
import station

from station import Station
import sys
import numpy



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

    v = np.zeros(len(stations), dtype=int)
    v[id_to_index[2673730]] = 1
    # print(v)

    from_stockholm = matrix @ v

    for i, col in enumerate(from_stockholm):
        if col == 1:
            print(stations[stations_list[i]].name)



    # print(matrix)


    print(len(stations))
    # draw_map(stations)


if __name__ == "__main__":
    main()

# for i in range(2):
#     res = requests.get(
#         url_for_suggestions_from_station_by_id(START_STATION_ID)
#     )
#     res.raise_for_status()
#     data = res.json()
#     for suggestion in data["suggestions"]:
#         dest = suggestion["destination"]
#         if dest["countryCode"] == "FR":
#             continue
#         print(dest["name"])
