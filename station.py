import dataclasses


@dataclasses.dataclass
class Station:
    id: int
    name: str
    country_code: str
    population: int
    rank: int
    longitude: float
    latitude: float
