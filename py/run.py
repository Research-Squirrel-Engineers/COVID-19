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
file_out_rki1 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki1.ttl"
file_out_rki2 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki2.ttl"
file_out_rki3 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki3.ttl"
file_out_rki4 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki4.ttl"
file_out_rki5 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki5.ttl"
file_out_rki_cum = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki_ger.ttl"
file_out_rki_fs = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki_fs.ttl"
os.remove(file_out_jhu)
os.remove(file_out_ecdc)
os.remove(file_out_rki1)
os.remove(file_out_rki2)
os.remove(file_out_rki3)
os.remove(file_out_rki4)
os.remove(file_out_rki5)
os.remove(file_out_rki_cum)
os.remove(file_out_rki_fs)

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

lines0 = []
lines1 = []
lines2 = []
lines3 = []
lines4 = []

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
    castr = item['cases']
    destr = item['deaths']
    ccode = item['countryterritoryCode']
    m = hashlib.md5()
    m.update(ccode + dstr + "ECDC")
    UUID = str(int(m.hexdigest(), 16))[0:16]
    lines1.append("covid19:" + UUID + " " + "rdf:type" + " covid19:ECDC_Dataset .")
    if cstr == "United_States_of_America":
        cstr = "United_States"
    lines1.append("covid19:" + UUID + " " + "covid19:country" + " world:" + cstr + " .")
    lines1.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + dstr + "'" + ".")
    lines1.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + castr + "'" + ".")
    lines1.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + destr + "'" + ".")
    lines1.append("")

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
    altersgruppe = item["properties"]["Altersgruppe"]
    faelle = str(item["properties"]["AnzahlFall"])
    todesfall = str(item["properties"]["AnzahlTodesfall"])
    meldedatum = str(item["properties"]["Refdatum"])
    genesen = str(item["properties"]["AnzahlGenesen"])
    lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "rdf:type" + " covid19:RKI_Dataset .")
    lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:bundeslandcode" + " " + "'" + bundesland + "'" + ".")
    lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:bundesland" + " world:" + blcode + " .")
    lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:date" + " " + "'" + meldedatum + "'" + ".")
    lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:geschlecht" + " " + "'" + geschlecht + "'" + ".")
    lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:altersgruppe" + " " + "'" + altersgruppe + "'" + ".")
    if int(faelle) > -1:
        lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:confirmed" + " " + "'" + faelle + "'" + ".")
    else:
        lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:confirmed" + " " + "'0'" + ".")
    if int(todesfall) > -1:
        lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:deaths" + " " + "'" + todesfall + "'" + ".")
    else:
        lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:deaths" + " " + "'0'" + ".")
    if int(genesen) > -1:
        lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:recovered" + " " + "'" + genesen + "'" + ".")
    else:
        lines2.append("covid19:" + str(item["properties"]["FID"]) + " " + "covid19:recovered" + " " + "'0'" + ".")
    lines2.append("")

meldedaten = set()
for item in dataRKI:
    meldedaten.add(str(item["properties"]["Refdatum"]))
meldetdaten = sorted(meldedaten)

fedstates = set()
for item in dataRKI:
    fedstates.add(int(item["properties"]["IdBundesland"]))
fedstates = sorted(fedstates)

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
    carr[str(item["properties"]["Refdatum"])] = 0
    darr[str(item["properties"]["Refdatum"])] = 0
    rarr[str(item["properties"]["Refdatum"])] = 0
    carr2[str(item["properties"]["Refdatum"])] = 0
    darr2[str(item["properties"]["Refdatum"])] = 0
    rarr2[str(item["properties"]["Refdatum"])] = 0
print(len(carr),len(darr),len(rarr),len(carr2),len(darr2),len(rarr2))

for md in meldedaten:
    for fs in fedstates:
        MDBL = str(md) + ";" + str(fs)
        carr3[MDBL] = 0
        darr3[MDBL] = 0
        rarr3[MDBL] = 0
        carr4[MDBL] = 0
        darr4[MDBL] = 0
        rarr4[MDBL] = 0
print(len(carr3),len(darr3),len(rarr3),len(carr4),len(darr4),len(rarr4))

sumC = 0
sumD = 0
sumR = 0
for date in meldedaten:
    print(date)
    for item in dataRKI:
        meldedatum = str(item["properties"]["Refdatum"])
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
print(sumC,sumD,sumR)

sumC = 0
sumD = 0
sumR = 0
lauf = 1;
for md in meldedaten:
    for fs in fedstates:
        print(md,fs,lauf)
        lauf = lauf + 1
        for item in dataRKI:
            meldedatum = str(item["properties"]["Refdatum"])
            state = int(item["properties"]["IdBundesland"])
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
print(sumC,sumD,sumR)

for item in carr:
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
    lines4.append("")

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
print("success write covid19.ttl")

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
print("success write covid19.ttl")

file = codecs.open(file_out_rki1, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKI1 rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKI1 rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKI1 dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKI1 dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKI1 dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKI1 dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKI1 dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKI1 dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKI1 dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKI1 dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKI1 dc:rights 'CC BY 4.0' .\r\n\r\n")
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
file.write("covid19:COVID19_DataRKI2 rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKI2 rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKI2 dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKI2 dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKI2 dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKI2 dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKI2 dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKI2 dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKI2 dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKI2 dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKI2 dc:rights 'CC BY 4.0' .\r\n\r\n")
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
file.write("covid19:COVID19_DataRKI3 rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKI3 rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKI3 dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKI3 dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKI3 dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKI3 dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKI3 dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKI3 dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKI3 dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKI3 dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKI3 dc:rights 'CC BY 4.0' .\r\n\r\n")
i = 1000000
for i, line in enumerate (lines2):
    if (i>1000000 and i<1500000):
        file.write(line)
        file.write("\r\n")
file.close()
print("success write covid19_rki3.ttl")

file = codecs.open(file_out_rki4, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKI4 rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKI4 rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKI4 dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKI4 dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKI4 dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKI4 dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKI4 dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKI4 dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKI4 dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKI4 dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKI4 dc:rights 'CC BY 4.0' .\r\n\r\n")
i = 1500000
for i, line in enumerate (lines2):
    if (i>1500000 and i<2000000):
        file.write(line)
        file.write("\r\n")
file.close()
print("success write covid19_rki4.ttl")

file = codecs.open(file_out_rki5, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKI5 rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKI5 rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKI5 dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKI5 dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKI5 dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKI5 dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKI5 dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKI5 dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKI5 dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKI5 dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKI5 dc:rights 'CC BY 4.0' .\r\n\r\n")
i = 2000000
for i, line in enumerate (lines2):
    if (i>2000000 and i<2500000):
        file.write(line)
        file.write("\r\n")
file.close()
print("success write covid19_rki5.ttl")

file = codecs.open(file_out_rki_cum, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKIGER rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKIGER rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKIGER dc:created '2020-04-05T10:53:21.259+0100' .\r\n")
file.write("covid19:COVID19_DataRKIGER dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKIGER dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKIGER dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKIGER dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKIGER dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKIGER dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKIGER dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKIGER dc:rights 'CC BY 4.0' .\r\n\r\n")
for line in lines3:
    file.write(line)
    file.write("\r\n")
file.close()
print("success write covid19_rki_ger.ttl")

file = codecs.open(file_out_rki_fs, "w", "utf-8")
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
print("success write covid19_rki_fs.ttl")
