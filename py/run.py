__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2020, Florian Thiery, Research Squirrel Engineers"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "rse@fthiery.de"
__status__ = "draft"

import json
import requests
import uuid
import pandas as pd
import os
import codecs
import datetime
import hashlib

dir_path = os.path.dirname(os.path.realpath(__file__))
file_out = dir_path + "\\" + "covid19.ttl"

response = requests.get("https://pomber.github.io/covid19/timeseries.json")
data = response.json()

countries = []
for item in data:
    countries.append(str(item))

lines = []
for c in countries:
    cstring = str(c)
    thiscountry = data[c]
    for item in thiscountry:
        m = hashlib.md5()
        m.update("Germany" + str(item['date']))
        UUID = str(int(m.hexdigest(), 16))[0:16]
        lines.append("covid19:" + UUID + " " + "rdf:type" + " covid19:JHU_Dataset .")
        lines.append("covid19:" + UUID + " " + "covid19:country" + " world:" + str(cstring).replace(" ","_") + " .")
        lines.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + str(item['date']) + "'" + ".")
        lines.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + str(item['confirmed']) + "'" + ".")
        lines.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + str(item['deaths']) + "'" + ".")
        lines.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'" + str(item['recovered']) + "'" + ".")
        lines.append("")

file = codecs.open(file_out, "w", "utf-8")
file.write("# create triples from https://pomber.github.io/covid19/timeseries.json" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
for line in lines:
    file.write(line)
    file.write("\r\n")
file.close()
