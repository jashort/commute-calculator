import json
from dataclasses import dataclass

from .mapping import Location, Distance, Mapper


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
        print(h)
    for d in destinations:
        print(d)


if __name__ == '__main__':
    run()

    # data = load_data()
    #
    # with open('destinations.json', 'r') as in_file:
    #     destinations = json.load(in_file)

    # for location in data:
    #     for dest in destinations:
    #         if dest['name'] not in location['destinations']:
    #             location['destinations'][dest['name']] = 0

    # print(data)
    # for d in data:
    #     print(d)
    #     for dest in d.destinations:
    #         print(f"  {dest}: {d['destinations'][dest]}")

    # save_data(data)
