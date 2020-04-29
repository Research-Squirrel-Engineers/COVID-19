__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2020, Florian Thiery, Research Squirrel Engineers"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "rse@fthiery.de"
__status__ = "final"

import json
import requests
import uuid
import pandas as pd
import os
import codecs
import datetime
import hashlib

responseJHU = requests.get("https://pomber.github.io/covid19/timeseries.json")
dataJHU = responseJHU.json()
print("countriesJHU", len(dataJHU))

responseECDC = requests.get("https://opendata.ecdc.europa.eu/covid19/casedistribution/json/")
dataECDC = responseECDC.json()['records']
print("datasetsECDC", len(dataECDC))

responseRKI = requests.get("https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.geojson")
# docu https://www.arcgis.com/home/item.html?id=dd4580c810204019a7b8eb3e0b329dd6
# data https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0/data
dataRKI = responseRKI.json()['features']
print("datasetsRKI", len(dataRKI))
