""" Data input/output helpers """

import dataclasses
import json


class EnhancedJSONEncoder(json.JSONEncoder):
    """ Handle dataclasses in JSON """
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
