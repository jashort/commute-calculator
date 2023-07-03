""" Mapping/geocoding/routing functions """
import json
import urllib.parse
from dataclasses import dataclass
from json import JSONDecodeError

import requests

from commute_calculator.data import EnhancedJSONEncoder


@dataclass
class Location:
    lat: float
    lon: float
    name: str


@dataclass
class Distance:
    meters: float
    seconds: float

    def __str__(self):
        miles = round(self.meters * 0.0006213712, 1)
        minutes = round(self.seconds / 60, 2)
        return f"{miles} miles ({minutes} minutes)"


class Mapper:
    """ Caching interface for OpenStreetMap and APIs """
    def __init__(self):
        self.geocode_cache = {}
        self.distance_cache = {}
        self.load_geocode_cache()
        self.load_distance_cache()

    def load_geocode_cache(self):
        try:
            with open('geocode_cache.json', 'r') as in_file:
                data = json.load(in_file)
            for key in data:
                l = Location(**data[key])
                self.geocode_cache[key] = l
        except FileNotFoundError:
            pass
        except JSONDecodeError:
            pass

    def save_geocode_cache(self):
        with open('geocode_cache.json', 'w') as out_file:
            json.dump(self.geocode_cache, out_file, indent=2, cls=EnhancedJSONEncoder)

    def load_distance_cache(self):
        try:
            with open('distance_cache.json', 'r') as in_file:
                data = json.load(in_file)
            for key in data:
                l = Distance(**data[key])
                self.distance_cache[key] = l
        except FileNotFoundError:
            pass
        except JSONDecodeError:
            pass

    def save_distance_cache(self):
        with open('distance_cache.json', 'w') as out_file:
            json.dump(self.distance_cache, out_file, indent=2, cls=EnhancedJSONEncoder)

    def get_distance(self, from_loc: Location, to_loc: Location) -> Distance:
        key = f"{from_loc.lon},{from_loc.lat}:{to_loc.lon},{to_loc.lat}"
        if key in self.distance_cache:
            return self.distance_cache[key]
        else:
            resp = requests.get(
                f"http://router.project-osrm.org/route/v1/car/{from_loc.lon},{from_loc.lat};{to_loc.lon},{to_loc.lat}?overview=false""")
            routes = resp.json()

            route = routes['routes'][0]
            dist = Distance(route['distance'], route['duration'])
            self.distance_cache[key] = dist
            return dist

    def geocode(self, address: str):
        if address in self.geocode_cache:
            return self.geocode_cache[address]
        encoded = urllib.parse.quote_plus(address)
        resp = requests.get(
            f"https://nominatim.openstreetmap.org/search.php?q={encoded}&format=jsonv2"
        )
        data = resp.json()
        first = data[0]

        loc = Location(first["lat"], first["lon"], first["display_name"])
        self.geocode_cache[address] = loc
        return loc

    def save_caches(self):
        self.save_geocode_cache()
        self.save_distance_cache()


if __name__ == '__main__':
    mapper = Mapper()
    x = mapper.geocode("3415 SW Cedar Hills Blvd, Beaverton, OR 97005")
    y = mapper.geocode("12375 SW 5th St, Beaverton, OR 97005")
    print(mapper.get_distance(x, y))
    mapper.save_geocode_cache()
    mapper.save_distance_cache()
