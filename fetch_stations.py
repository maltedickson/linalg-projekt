import dataclasses
import json

import requests

from station import Station


def fetch_stations() -> list[Station]:
    res = requests.get("https://www.chronotrains.com/api/stations")
    res.raise_for_status()
    data = res.json()
    return parse_stations(data)


def read_stations_from_file():
    with open("stations_api_response.json") as f:
        data = json.load(f)
    return parse_stations(data)


def parse_stations(data) -> list[Station]:
    stations = []
    for feature in data["features"]:
        properties = feature["properties"]
        if "population" not in properties:
            continue
        if "isCity" not in properties or not properties["isCity"]:
            continue
        longitude, latitude = feature["geometry"]["coordinates"]
        station = Station(
            id=properties["id"],
            name=properties["name"],
            country_code=properties["countryCode"],
            population=properties["population"],
            rank=properties["rank"],
            longitude=longitude,
            latitude=latitude,
        )
        stations.append(station)
    return stations


def main():
    stations = read_stations_from_file()
    print(json.dumps({"stations": stations}, default=dataclasses.asdict, indent=4))


if __name__ == "__main__":
    main()
