"""Returns a list of all the cities"""

import os
import json

def all_cities():
    """Returns a list of all the cities."""
    citiesDataPath = os.path.join(os.getcwd(), 'all_cities.json')
    with open(citiesDataPath) as jsonFile:
        citiesData = json.load(jsonFile)

    return citiesData

all_cities = all_cities()