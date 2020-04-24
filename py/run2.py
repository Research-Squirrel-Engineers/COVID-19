__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2020, Florian Thiery, Research Squirrel Engineers"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "rse@fthiery.de"
__status__ = "final"

from SPARQLWrapper import SPARQLWrapper, JSON
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
file_out = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki_fs_cum.ttl"
file_out2 = dir_path.replace("\\py","\\ttl") + "\\" + "covid19_rki_ger_cum.ttl"
os.remove(file_out)
os.remove(file_out2)

endpoint_url = "http://sandbox.mainzed.org/covid19/sparql"

query = "PREFIX covid19: <http://covid19.squirrel.link/ontology#> PREFIX world: <http://world.squirrel.link/ontology#> PREFIX geosparql: <http://www.opengis.net/ont/geosparql#> SELECT ?date ?c ?d ?r ?bl WHERE { ?item a covid19:RKI_Dataset_FS. ?item covid19:date ?date. ?item covid19:bundesland ?bl. OPTIONAL {?item covid19:confirmed ?c.} OPTIONAL {?item covid19:deaths ?d.} OPTIONAL {?item covid19:recovered ?r.} } ORDER BY ASC(?date)"

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url, agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

results = get_results(endpoint_url, query)

bindings = results["results"]["bindings"]

meldedaten = set()
for i in bindings:
    meldedaten.add(i["date"]["value"])
meldedaten = sorted(meldedaten)
#print(meldedaten)

fedstates = set()
for i in bindings:
    fedstates.add(i["bl"]["value"])
fedstates = sorted(fedstates)
#print(fedstates)

carr = {}
darr = {}
rarr = {}
carr2 = {}
darr2 = {}
rarr2 = {}
carr3 = {}
darr3 = {}
rarr3 = {}

for md in meldedaten:
    for fs in fedstates:
        MDBL = str(md) + ";" + str(fs)
        MD = str(md)
        carr[MDBL] = 0
        darr[MDBL] = 0
        rarr[MDBL] = 0
        carr2[MD] = 0
        darr2[MD] = 0
        rarr2[MD] = 0
        carr3[MD] = 0
        darr3[MD] = 0
        rarr3[MD] = 0

for fs in fedstates:
    thisc = 0;
    thisr = 0;
    thisd = 0;
    print(fs)
    for md in meldedaten:
        for item in bindings:
            meldedatum = item["date"]["value"]
            state = item["bl"]["value"]
            MDBL = str(meldedatum) + ";" + str(state)
            faelle = 0
            if int(faelle) > -1:
                faelle = int(item["c"]["value"])
            todesfall = 0
            if int(todesfall) > -1:
                todesfall = int(item["d"]["value"])
            genesen = 0
            if int(genesen) > -1:
                genesen = int(item["r"]["value"])
            if (md == meldedatum and fs == state):
                carr[MDBL] = thisc + faelle
                darr[MDBL] = thisd + todesfall
                rarr[MDBL] = thisr + genesen
                thisc = carr[MDBL]
                thisd = darr[MDBL]
                thisr = rarr[MDBL]
print(carr)

for md in meldedaten:
    thisc = 0;
    thisr = 0;
    thisd = 0;
    print(md)
    for item in bindings:
        meldedatum = item["date"]["value"]
        MD = str(meldedatum)
        faelle = 0
        if int(faelle) > -1:
            faelle = int(item["c"]["value"])
        todesfall = 0
        if int(todesfall) > -1:
            todesfall = int(item["d"]["value"])
        genesen = 0
        if int(genesen) > -1:
            genesen = int(item["r"]["value"])
        if (md == meldedatum):
            print(thisc,faelle)
            carr2[MD] = thisc + faelle
            darr2[MD] = thisd + todesfall
            rarr2[MD] = thisr + genesen
            thisc = carr2[MD]
            thisd = darr2[MD]
            thisr = rarr2[MD]
print(carr2)

thisc = 0
thisr = 0
thisd = 0
for md in meldedaten:
    carr3[md] = thisc + carr2[md]
    thisc = carr3[md]
    darr3[md] = thisd + darr2[md]
    thisd = darr3[md]
    rarr3[md] = thisr + rarr2[md]
    thisr = rarr3[md]
print(carr3)

linesFSCUM = []
for key, value in carr.items():
    split = key.split(";")
    meldedatum = split[0]
    state = split[1]
    MDBL = str(meldedatum) + ";" + str(state)
    m = hashlib.md5()
    m.update(MDBL + "RKI_Dataset_FS_CUM")
    UUID = str(int(m.hexdigest(), 16))[0:16]
    blcode = "0"
    if state.find("SchleswigHolstein") > 0:
        bundesland = "1"
    elif state.find("Hamburg") > 0:
        bundesland = "2"
    elif state.find("Niedersachsen") > 0:
        bundesland = "2"
    elif state.find("Bremen") > 0:
        bundesland = "4"
    elif state.find("NordrheinWestfalen") > 0:
        bundesland = "5"
    elif state.find("Hessen") > 0:
        bundesland = "6"
    elif state.find("RheinlandPfalz") > 0:
        bundesland = "7"
    elif state.find("BadenWuerttemberg") > 0:
        bundesland = "8"
    elif state.find("Bayern") > 0:
        bundesland = "9"
    elif state.find("Saarland") > 0:
        bundesland = "10"
    elif state.find("Berlin") > 0:
        bundesland = "11"
    elif state.find("Brandenburg") > 0:
        bundesland = "12"
    elif state.find("MecklenburgVorpommern") > 0:
        bundesland = "13"
    elif state.find("Sachsen") > 0:
        bundesland = "14"
    elif state.find("SachsenAnhalt") > 0:
        bundesland = "15"
    elif state.find("Thueringen") > 0:
        bundesland = "16"
    linesFSCUM.append("covid19:" + UUID + " " + "rdf:type" + " covid19:RKI_Dataset_FS_CUM .")
    linesFSCUM.append("covid19:" + UUID + " " + "covid19:bundeslandcode" + " " + "'" + bundesland + "'" + ".")
    linesFSCUM.append("covid19:" + UUID + " " + "covid19:bundesland" + " world:" + state.replace("http://world.squirrel.link/ontology#","") + " .")
    linesFSCUM.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + str(meldedatum) + "'" + ".")
    if int(faelle) > -1:
        linesFSCUM.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + str(carr[MDBL]) + "'" + ".")
    else:
        linesFSCUM.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'0'" + ".")
    if int(todesfall) > -1:
        linesFSCUM.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + str(darr[MDBL]) + "'" + ".")
    else:
        linesFSCUM.append("covid19:" + UUID+ " " + "covid19:deaths" + " " + "'0'" + ".")
    if int(genesen) > -1:
        linesFSCUM.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'" + str(rarr[MDBL]) + "'" + ".")
    else:
        linesFSCUM.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'0'" + ".")
    linesFSCUM.append("")

linesGERCUM = []
for key, value in carr3.items():
    meldedatum = key
    MD = str(meldedatum)
    m = hashlib.md5()
    m.update(MDBL + "RKI_Dataset_GER_CUM")
    UUID = str(int(m.hexdigest(), 16))[0:16]
    linesGERCUM.append("covid19:" + UUID + " " + "rdf:type" + " covid19:RKI_Dataset_GER_CUM .")
    linesGERCUM.append("covid19:" + UUID + " " + "covid19:country world:Germany .")
    linesGERCUM.append("covid19:" + UUID + " " + "covid19:date" + " " + "'" + str(meldedatum) + "'" + ".")
    if int(faelle) > -1:
        linesGERCUM.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'" + str(carr3[MD]) + "'" + ".")
    else:
        linesGERCUM.append("covid19:" + UUID + " " + "covid19:confirmed" + " " + "'0'" + ".")
    if int(todesfall) > -1:
        linesGERCUM.append("covid19:" + UUID + " " + "covid19:deaths" + " " + "'" + str(darr3[MD]) + "'" + ".")
    else:
        linesGERCUM.append("covid19:" + UUID+ " " + "covid19:deaths" + " " + "'0'" + ".")
    if int(genesen) > -1:
        linesGERCUM.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'" + str(rarr3[MD]) + "'" + ".")
    else:
        linesGERCUM.append("covid19:" + UUID + " " + "covid19:recovered" + " " + "'0'" + ".")
    linesGERCUM.append("")

file = codecs.open(file_out, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKIFSCUM rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKIFSCUM rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKIFSCUM dc:created '2020-04-24T17:17:21.386+0100' .\r\n")
file.write("covid19:COVID19_DataRKIFSCUM dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKIFSCUM dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKIFSCUM dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKIFSCUM dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKIFSCUM dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKIFSCUM dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKIFSCUM dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKIFSCUM dc:rights 'CC BY 4.0' .\r\n\r\n")
for line in linesFSCUM:
    file.write(line)
    file.write("\r\n")
file.close()
print("success write covid19_rki_fs_cum.ttl")

file = codecs.open(file_out2, "w", "utf-8")
file.write("# create triples from RKI" + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX covid19: <http://covid19.squirrel.link/ontology#> \r\nPREFIX world: <http://world.squirrel.link/ontology#> \r\n\r\n";
file.write(prefixes)
file.write("covid19:COVID19_DataRKIGERCUM rdf:type rdfs:Resource .\r\n")
file.write("covid19:COVID19_DataRKIGERCUM rdf:type covid19:Dataset .\r\n")
file.write("covid19:COVID19_DataRKIGERCUM dc:created '2020-04-24T17:17:21.386+0100' .\r\n")
file.write("covid19:COVID19_DataRKIGERCUM dc:modified '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0100") + "' .\r\n")
file.write("covid19:COVID19_DataRKIGERCUM dc:creator 'Florian Thiery' .\r\n")
file.write("covid19:COVID19_DataRKIGERCUM dc:contributor 'Timo Homburg' .\r\n")
file.write("covid19:COVID19_DataRKIGERCUM dc:language 'en' .\r\n")
file.write("covid19:COVID19_DataRKIGERCUM dc:type 'ontology' .\r\n")
file.write("covid19:COVID19_DataRKIGERCUM dc:title 'COVID-19 data by RKI' .\r\n")
file.write("covid19:COVID19_DataRKIGERCUM dc:subject 'COVID-19' .\r\n")
file.write("covid19:COVID19_DataRKIGERCUM dc:rights 'CC BY 4.0' .\r\n\r\n")
for line in linesGERCUM:
    file.write(line)
    file.write("\r\n")
file.close()
print("success write covid19_rki_ger_cum.ttl")
