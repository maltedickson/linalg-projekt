import dataclasses
import json

@dataclasses.dataclass
class Station:
    id: int
    name: str
    country_code: str
    population: int
    rank: int
    longitude: float
    latitude: float

def read_stations_from_file() -> dict[int, Station]:
    stations = {}
    with open("stations.json") as f:
        data = json.load(f)
    station_list = [Station(**item) for item in data["stations"]]
    for station in station_list:
        # if station.rank > 5:
        #     continue
        if (station.population < 100000 and station.rank > 5) or station.rank > 20:
            continue
        stations[station.id] = station
    return stations