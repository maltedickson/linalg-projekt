import json

import requests
import time

from station import read_stations_from_file

def fetch_routes_from_station(station_ids: set[int], from_station_id: int) -> list[int]:
    res = requests.get(f"https://www.chronotrains.com/api/station/{from_station_id}/suggestions?lang=en&mode=direct")
    res.raise_for_status()
    data = res.json()
    suggestions = data["suggestions"]
    destination_ids: list[int] = []
    for suggestion in suggestions:
        destination = suggestion["destination"]
        destination_id = destination["id"]
        if destination_id not in station_ids:
            continue
        destination_ids.append(destination_id)
    return destination_ids




def main():
    stations = read_stations_from_file()
    station_ids = set()
    for id in stations.keys():
        station_ids.add(id)
    all_routes: dict[int, list[int]] = dict()
    for id in station_ids:
        from_current_station = fetch_routes_from_station(station_ids, 2673730)
        all_routes[id] = from_current_station
        time.sleep(0.1)
    print(json.dumps({"routes": all_routes}, indent=4))


if __name__ == "__main__":
    main()
