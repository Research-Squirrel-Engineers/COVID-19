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
file_out_rki_lk = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki_lk.ttl"
#os.remove(file_out_rki_lk)

responseRKI = requests.get("https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.geojson")
# docu https://www.arcgis.com/home/item.html?id=dd4580c810204019a7b8eb3e0b329dd6
# data https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0/data
dataRKI = responseRKI.json()['features']
print("datasetsRKI", len(dataRKI))

lines2 = []
lines3 = []
lines4 = []

meldedaten = set()
for item in dataRKI:
    meldedaten.add(str(item["properties"]["Meldedatum"]))
meldetdaten = sorted(meldedaten)
print("meldetdaten",len(meldetdaten))

districts = set()
for item in dataRKI:
    districts.add(int(item["properties"]["IdLandkreis"]))
districts = sorted(districts)
print("districts",len(districts))

carr = {}
darr = {}
rarr = {}
carr2 = {}
darr2 = {}
rarr2 = {}

carr3 = {}
darr3 = {}
rarr3 = {}
carr4 = {}
darr4 = {}
rarr4 = {}

for item in dataRKI:
    carr[str(item["properties"]["Meldedatum"])] = 0
    darr[str(item["properties"]["Meldedatum"])] = 0
    rarr[str(item["properties"]["Meldedatum"])] = 0
    carr2[str(item["properties"]["Meldedatum"])] = 0
    darr2[str(item["properties"]["Meldedatum"])] = 0
    rarr2[str(item["properties"]["Meldedatum"])] = 0
print("carr",len(carr))

for md in meldedaten:
    for d in districts:
        MDBL = str(md) + ";" + str(d)
        carr3[MDBL] = 0
        darr3[MDBL] = 0
        rarr3[MDBL] = 0
        carr4[MDBL] = 0
        darr4[MDBL] = 0
        rarr4[MDBL] = 0
print("carr3",len(carr3))

sumC = 0
sumD = 0
sumR = 0
lauf = 1
for item in dataRKI:
    if (lauf % 2500) == 0:
        print("lauf",lauf)
    lauf = lauf + 1
    for date in meldedaten:
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
print("cases","deaths","recovered",sumC,sumD,sumR)

sumC = 0
sumD = 0
sumR = 0
lauf = 1
for item in dataRKI:
    if (lauf % 1) == 0:
        print("lauf",lauf)
    lauf = lauf + 1
    for fs in districts:
        for md in meldedaten:
            meldedatum = str(item["properties"]["Meldedatum"])
            state = int(item["properties"]["IdLandkreis"])
            MDBL = str(meldedatum) + ";" + str(state)
            faelle = 0
            if int(faelle) > -1:
                faelle = int(item["properties"]["AnzahlFall"])
            todesfall = 0
            if int(todesfall) > -1:
                todesfall = int(item["properties"]["AnzahlTodesfall"])
            genesen = 0
            if int(genesen) > -1:
                genesen = int(item["properties"]["AnzahlGenesen"])
            if (md == meldedatum and fs == state):
                sumC = sumC + faelle
                sumD = sumD + todesfall
                sumR = sumR + genesen
                carr3[MDBL] = carr3[MDBL] + faelle
                darr3[MDBL] = darr3[MDBL] + todesfall
                rarr3[MDBL] = rarr3[MDBL] + genesen
print("cases","deaths","recovered",sumC,sumD,sumR)

'''for item in carr:
    #print(item,carr[item])
    m = hashlib.md5()
    m.update(item + "RKI_Dataset_CUM")
    UUID = str(int(m.hexdigest(), 16))[0:16]
    lines3.append("covid19:" + UUID + " " + "rdf:type" + " covid19:RKI_Dataset_GER .")
    lines3.append("covid19:" + UUID + " " + "covid19:country" + " world:Germany .")
    lines3.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + item + "'" + ".")
    if int(faelle) > -1:
        lines3.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + str(carr[item]) + "'" + ".")
    else:
        lines3.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'0'" + ".")
    if int(todesfall) > -1:
        lines3.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + str(darr[item]) + "'" + ".")
    else:
        lines3.append("covid19:" + UUID+ " " + "covid19:deaths" + " " + "'0'" + ".")
    if int(genesen) > -1:
        lines3.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'" + str(rarr[item]) + "'" + ".")
    else:
        lines3.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'0'" + ".")
    lines3.append("")

for item in carr3:
    m = hashlib.md5()
    m.update(item + "RKI_Dataset_FS")
    UUID = str(int(m.hexdigest(), 16))[0:16]
    split = item.split(';')
    bundesland = str(split[1])
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
    lines4.append("covid19:" + UUID + " " + "rdf:type" + " covid19:RKI_Dataset_FS .")
    lines4.append("covid19:" + UUID + " " + "covid19:bundeslandcode" + " " + "'" + bundesland + "'" + ".")
    lines4.append("covid19:" + UUID + " " + "covid19:bundesland" + " world:" + blcode + " .")
    lines4.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + str(split[0]) + "'" + ".")
    if int(faelle) > -1:
        lines4.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + str(carr3[item]) + "'" + ".")
    else:
        lines4.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'0'" + ".")
    if int(todesfall) > -1:
        lines4.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + str(darr3[item]) + "'" + ".")
    else:
        lines4.append("covid19:" + UUID+ " " + "covid19:deaths" + " " + "'0'" + ".")
    if int(genesen) > -1:
        lines4.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'" + str(rarr3[item]) + "'" + ".")
    else:
        lines4.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'0'" + ".")
    lines4.append("")'''

'''file = codecs.open(file_out_rki_fs, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKIFS rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKIFS rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKIFS dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKIFS dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKIFS dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKIFS dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKIFS dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKIFS dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKIFS dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKIFS dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKIFS dc:rights 'CC BY 4.0' .\r\n\r\n")
for line in lines4:
    file.write(line)
    file.write("\r\n")
file.close()
print("success write covid19_rki_fs.ttl")'''
