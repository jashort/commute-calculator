import json
from dataclasses import dataclass

from commute_calculator.mapping import Location, Distance, Mapper


@dataclass
class Destination:
    name: str
    location: Location
    distance: Distance


@dataclass
class Address:
    name: str
    address: str


@dataclass
class Property:
    name: str
    address: str
    location: Location
    destinations: [Destination]


def load_addresses(filename: str) -> [Address]:
    output = []
    with open(filename, 'r') as in_file:
        data = json.load(in_file)
    for line in data:
        output.append(Address(**line))
    return output


def run():
    homes = load_addresses('homes.json')
    destinations = load_addresses('destinations.json')

    mapper = Mapper()

    for h in homes:
        print(f"{h.name}: {h.address}")
        for d in destinations:
            from_loc = mapper.geocode(h.address)
            to_loc = mapper.geocode(d.address)
            distance = mapper.get_distance(from_loc, to_loc)
            print(f"  to {d.name:<20} {distance}")
    mapper.save_caches()


if __name__ == '__main__':
    run()
