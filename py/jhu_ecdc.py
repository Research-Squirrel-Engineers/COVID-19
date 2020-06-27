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

dir_path = os.path.dirname(os.path.realpath(__file__))
# py script into a "py" folder -> ttl into a "ttl" folder
file_out_jhu = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_jhu.ttl"
file_out_ecdc = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_ecdc.ttl"
os.remove(file_out_jhu)
os.remove(file_out_ecdc)

responseJHU = requests.get("https://pomber.github.io/covid19/timeseries.json")
dataJHU = responseJHU.json()
print("countriesJHU", len(dataJHU))

responseECDC = requests.get("https://opendata.ecdc.europa.eu/covid19/casedistribution/json/")
dataECDC = responseECDC.json()['records']
print("datasetsECDC", len(dataECDC))

countriesJHU = []
for item in dataJHU:
    countriesJHU.append(str(item))

lines0 = []
lines1 = []

i = 0
for c in countriesJHU:
    cstring = str(c)
    cstring = cstring.replace(" ","_").replace("(","").replace(")","").replace("'","").replace("*","").replace(",","")
    thiscountry = dataJHU[c]
    for item in thiscountry:
        i = i+1
        m = hashlib.md5()
        m.update(cstring + str(item['date']) + "JHU")
        UUID = str(int(m.hexdigest(), 16))[0:16]
        dstrArr = str(item['date']).split("-")
        dstr = str(dstrArr[0]).zfill(2) + "-" + str(dstrArr[1]).zfill(2) + "-" + str(dstrArr[2]).zfill(2) + "T00:00:00.000Z"
        lines0.append("covid19:" + UUID + " " + "rdf:type" + " covid19:JHU_Dataset .")
        if cstring == "US":
            cstring = "United_States"
        lines0.append("covid19:" + UUID + " " + "covid19:country" + " world:" + cstring + " .")
        lines0.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + dstr + "'" + ".")
        lines0.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + str(item['confirmed']) + "'" + ".")
        lines0.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + str(item['deaths']) + "'" + ".")
        lines0.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'" + str(item['recovered']) + "'" + ".")
        lines0.append("")
print("datasetsJHU", int(i))

for item in dataECDC:
    cstr = item['countriesAndTerritories']
    cstr = cstr.replace(" ","_").replace("(","").replace(")","").replace("'","").replace("*","").replace(",","")
    dstrArr = str(item['dateRep']).split("/")
    dstr = str(dstrArr[2]).zfill(2) + "-" + str(dstrArr[1]).zfill(2) + "-" + str(dstrArr[0]).zfill(2) + "T00:00:00.000Z"
    castr = str(item['cases'])
    destr = str(item['deaths'])
    ccode = item['countryterritoryCode']
    m = hashlib.md5()
    m.update(str(ccode) + str(item['dateRep']) + "ECDC")
    UUID = str(int(m.hexdigest(), 16))[0:16]
    lines1.append("covid19:" + UUID + " " + "rdf:type" + " covid19:ECDC_Dataset .")
    if cstr == "United_States_of_America":
        cstr = "United_States"
    lines1.append("covid19:" + UUID + " " + "covid19:country" + " world:" + cstr + " .")
    lines1.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + dstr + "'" + ".")
    lines1.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + castr + "'" + ".")
    lines1.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + destr + "'" + ".")
    lines1.append("")

file = codecs.open(file_out_jhu, "w", "utf-8")
file.write("# create triples from JHU" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataJHU rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataJHU rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataJHU dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataJHU dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataJHU dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataJHU dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataJHU dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataJHU dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataJHU dc:title 'COVID-19 data by JHU' .\r\n")
file.write("covid19:COVID19_DataJHU dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataJHU dc:rights 'CC BY 4.0' .\r\n\r\n")
for line in lines0:
    file.write(line)
    file.write("\r\n")
file.close()
print("success write covid19_jhu.ttl")

file = codecs.open(file_out_ecdc, "w", "utf-8")
file.write("# create triples from ECDC" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataECDC rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataECDC rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataECDC dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataECDC dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataECDC dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataECDC dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataECDC dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataECDC dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataECDC dc:title 'COVID-19 data by ECDC' .\r\n")
file.write("covid19:COVID19_DataECDC dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataECDC dc:rights 'CC BY 4.0' .\r\n\r\n")
for line in lines1:
    file.write(line)
    file.write("\r\n")
file.close()
print("success write covid19_ecdc.ttl")
