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
#print(dir_path.replace("\\py","\\ttl"))
file_out = dir_path.replace("\\py","\\ttl") + "\\" + "covid19.ttl"
file_out_rki1 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki1.ttl"
file_out_rki2 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki2.ttl"
file_out_rki3 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki3.ttl"
file_out_rki4 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki4.ttl"
file_out_rki5 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki5.ttl"

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

countriesJHU = []
for item in dataJHU:
    countriesJHU.append(str(item))

lines = []
lines2 = []

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
        lines.append("covid19:" + UUID + " " + "rdf:type" + " covid19:JHU_Dataset .")
        if cstring == "US":
            cstring = "United_States"
        lines.append("covid19:" + UUID + " " + "covid19:country" + " world:" + cstring + " .")
        lines.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + dstr + "'" + ".")
        lines.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + str(item['confirmed']) + "'" + ".")
        lines.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + str(item['deaths']) + "'" + ".")
        lines.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'" + str(item['recovered']) + "'" + ".")
        lines.append("")
print("datasetsJHU", int(i))

for item in dataECDC:
    cstr = item['countriesAndTerritories']
    cstr = cstr.replace(" ","_").replace("(","").replace(")","").replace("'","").replace("*","").replace(",","")
    dstrArr = str(item['dateRep']).split("/")
    dstr = str(dstrArr[2]).zfill(2) + "-" + str(dstrArr[1]).zfill(2) + "-" + str(dstrArr[0]).zfill(2) + "T00:00:00.000Z"
    castr = item['cases']
    destr = item['deaths']
    ccode = item['countryterritoryCode']
    m = hashlib.md5()
    m.update(ccode + dstr + "ECDC")
    UUID = str(int(m.hexdigest(), 16))[0:16]
    lines.append("covid19:" + UUID + " " + "rdf:type" + " covid19:ECDC_Dataset .")
    if cstr == "United_States_of_America":
        cstr = "United_States"
    lines.append("covid19:" + UUID + " " + "covid19:country" + " world:" + cstr + " .")
    lines.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + dstr + "'" + ".")
    lines.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + castr + "'" + ".")
    lines.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + destr + "'" + ".")
    lines.append("")

for item in dataRKI:
    bundesland = str(item["properties"]["IdBundesland"])
    blcode = "0"
    if bundesland == "1":
        blcode = "SchleswigHolstein"
    elif bundesland == "2":
        blcode = "Hamburg"
    elif bundesland == "3":
        blcode = "Niedersachsen"
    elif bundesland == "4":
        blcode = "Bremen"
    elif bundesland == "5":
        blcode = "NordrheinWestfalen"
    elif bundesland == "6":
        blcode = "Hessen"
    elif bundesland == "7":
        blcode = "RheinlandPfalz"
    elif bundesland == "8":
        blcode = "BadenWuerttemberg"
    elif bundesland == "9":
        blcode = "Bayern"
    elif bundesland == "10":
        blcode = "Saarland"
    elif bundesland == "11":
        blcode = "Berlin"
    elif bundesland == "12":
        blcode = "Brandenburg"
    elif bundesland == "13":
        blcode = "MecklenburgVorpommern"
    elif bundesland == "14":
        blcode = "Sachsen"
    elif bundesland == "15":
        blcode = "SachsenAnhalt"
    elif bundesland == "16":
        blcode = "Thueringen"
    geschlecht = str(item["properties"]["Geschlecht"])
    altersgruppe = str(item["properties"]["Altersgruppe"])
    faelle = str(item["properties"]["AnzahlFall"])
    todesfall = str(item["properties"]["AnzahlTodesfall"])
    meldedatum = str(item["properties"]["Meldedatum"])
    genesen = str(item["properties"]["AnzahlGenesen"])
    lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "rdf:type" + " covid19:RKI_Dataset .")
    lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:bundeslandcode" + " " + "'" + bundesland + "'" + ".")
    lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:bundesland" + " world:" + blcode + " .")
    lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:date" + " " + "'" + meldedatum + "'" + ".")
    lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:geschlecht" + " " + "'" + geschlecht + "'" + ".")
    lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:altersgruppe" + " " + "'" + altersgruppe + "'" + ".")
    if int(faelle) > -1:
        lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:confirmed" + " " + "'" + faelle + "'" + ".")
    else:
        lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:confirmed" + " " + "'0'" + ".")
    if int(todesfall) > -1:
        lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:deaths" + " " + "'" + todesfall + "'" + ".")
    else:
        lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:deaths" + " " + "'0'" + ".")
    if int(genesen) > -1:
        lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:recovered" + " " + "'" + genesen + "'" + ".")
    else:
        lines2.append("covid19:" + str(item["properties"]["ObjectId"]) + " " + "covid19:recovered" + " " + "'0'" + ".")
    lines2.append("")

meldedaten = set()
for item in dataRKI:
    meldedaten.add(str(item["properties"]["Meldedatum"]))
meldetdaten = sorted(meldedaten)
#print(meldedaten)

carr = {}
darr = {}
rarr = {}
carr2 = {}
darr2 = {}
rarr2 = {}

for item in dataRKI:
    carr[str(item["properties"]["Meldedatum"])] = 0
    darr[str(item["properties"]["Meldedatum"])] = 0
    rarr[str(item["properties"]["Meldedatum"])] = 0
    carr2[str(item["properties"]["Meldedatum"])] = 0
    darr2[str(item["properties"]["Meldedatum"])] = 0
    rarr2[str(item["properties"]["Meldedatum"])] = 0
#print(carr)

sumC = 0
sumD = 0
sumR = 0
for date in meldedaten:
    for item in dataRKI:
        meldedatum = str(item["properties"]["Meldedatum"])
        faelle = 0
        if int(faelle) > -1:
            faelle = int(item["properties"]["AnzahlFall"])
        todesfall = 0
        if int(todesfall) > -1:
            todesfall = int(item["properties"]["AnzahlTodesfall"])
        genesen = 0
        if int(genesen) > -1:
            genesen = int(item["properties"]["AnzahlGenesen"])
        if date == meldedatum:
            sumC = sumC + faelle
            sumD = sumD + todesfall
            sumR = sumR + genesen
            carr[meldedatum] = carr[meldedatum] + faelle
            darr[meldedatum] = darr[meldedatum] + todesfall
            rarr[meldedatum] = rarr[meldedatum] + genesen

carr_sort=sorted(carr.keys(), key=lambda x:x.lower())
for i in carr_sort:
   values=carr[i]
   print(i,values)
print("faelle",sumC)
darr_sort=sorted(darr.keys(), key=lambda x:x.lower())
for i in darr_sort:
   values=darr[i]
   print(i,values)
print("todesfall",sumD)
rarr_sort=sorted(rarr.keys(), key=lambda x:x.lower())
for i in rarr_sort:
   values=rarr[i]
   print(i,values)
print("genesen",sumR)

file = codecs.open(file_out, "w", "utf-8")
file.write("# create triples from JHU and ECDC" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_Data rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_Data rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_Data dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_Data dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_Data dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_Data dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_Data dc:language 'en' .\r\n")
file.write("covid19:COVID19_Data dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_Data dc:title 'COVID-19 data by JHU and ECDC' .\r\n")
file.write("covid19:COVID19_Data dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_Data dc:rights 'CC BY 4.0' .\r\n\r\n")
for line in lines:
    file.write(line)
    file.write("\r\n")
file.close()
print("success write covid19.ttl")

file = codecs.open(file_out_rki1, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKI rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKI rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKI dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKI dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKI dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKI dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKI dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKI dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKI dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKI dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKI dc:rights 'CC BY 4.0' .\r\n\r\n")
i = 0
for i, line in enumerate (lines2):
    if (i>0 and i<500000):
        file.write(line)
        file.write("\r\n")
file.close()
print("success write covid19_rki1.ttl")

file = codecs.open(file_out_rki2, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKI rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKI rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKI dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKI dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKI dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKI dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKI dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKI dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKI dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKI dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKI dc:rights 'CC BY 4.0' .\r\n\r\n")
i = 500000
for i, line in enumerate (lines2):
    if (i>500000 and i<1000000):
        file.write(line)
        file.write("\r\n")
file.close()
print("success write covid19_rki2.ttl")

file = codecs.open(file_out_rki3, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKI rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKI rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKI dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKI dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKI dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKI dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKI dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKI dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKI dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKI dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKI dc:rights 'CC BY 4.0' .\r\n\r\n")
i = 1500000
for i, line in enumerate (lines2):
    if (i>1500000 and i<2000000):
        file.write(line)
        file.write("\r\n")
file.close()
print("success write covid19_rki3.ttl")

file = codecs.open(file_out_rki4, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKI rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKI rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKI dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKI dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKI dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKI dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKI dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKI dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKI dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKI dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKI dc:rights 'CC BY 4.0' .\r\n\r\n")
i = 2000000
for i, line in enumerate (lines2):
    if (i>2000000 and i<2500000):
        file.write(line)
        file.write("\r\n")
file.close()
print("success write covid19_rki4.ttl")

file = codecs.open(file_out_rki5, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKI rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKI rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKI dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKI dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKI dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKI dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKI dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKI dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKI dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKI dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKI dc:rights 'CC BY 4.0' .\r\n\r\n")
i = 2500000
for i, line in enumerate (lines2):
    if (i>2500000 and i<3000000):
        file.write(line)
        file.write("\r\n")
file.close()
print("success write covid19_rki5.ttl")
