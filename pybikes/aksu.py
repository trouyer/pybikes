# -*- coding: utf-8 -*-
# Copyright (C) 2023, Martín González Gómez <m@martingonzalez.net>
# Distributed under the AGPL license, see LICENSE.txt

import re
import json

from pybikes import BikeShareSystem, BikeShareStation, PyBikesScraper
from pybikes.utils import filter_bounds


class Aksu(BikeShareSystem):
    unifeed = True

    def __init__(self, tag, meta, endpoint, bbox=None):
        super(Aksu, self).__init__(tag, meta)
        self.endpoint = endpoint
        self.bbox = bbox

    def update(self, scraper=None):
        scraper = scraper or PyBikesScraper()

        raw = scraper.request(self.endpoint)

        marker_var = re.search(r'var ibike = (.*)', raw, re.DOTALL)
        markers = json.loads(marker_var.group(1))

        stations = []

        for station in markers["station"]:
            stations.append(AksuStation(station))

        if self.bbox:
            stations = list(filter_bounds(stations, None, self.bbox))

        self.stations = stations

class AksuStation(BikeShareStation):
    def __init__(self, data):
        super(AksuStation, self).__init__()

        self.name = data["name"]
        self.latitude = float(data["lat"])
        self.longitude = float(data["lng"])

        self.bikes = int(data["availBike"])
        self.free = int(data["capacity"])

        self.extra = {
            "uid": data["id"],
            "address": data["address"]
        }
