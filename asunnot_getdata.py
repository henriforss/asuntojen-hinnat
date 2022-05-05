# Esimerkki kuinka tehtävässä käytetyn datan olisi voinut hakea API:n kautta
# suoraan Pythonilla. Tässä haetaan kaksi kolmesta datasetistä, prosessi on melkein identtinen.
# Näiden hakujen avulla voi tuottaa täysin saman kuvaajan kun aiemmin.

import requests
import pandas as pd

# API:n osoite
API_URL = "https://pxweb2.stat.fi:443/PxWeb/api/v1/fi/StatFin/ashi/statfin_ashi_pxt_112l.px"

# API:lle lähetettävät JSON-query parametrit
params = {
  "query": [
    {
      "code": "Alue",
      "selection": {
        "filter": "item",
        "values": [
          "ksu"
        ]
      }
    },
    {
      "code": "Talotyyppi",
      "selection": {
        "filter": "item",
        "values": [
          "0"
        ]
      }
    },
    {
      "code": "Huoneluku",
      "selection": {
        "filter": "item",
        "values": [
          "00"
        ]
      }
    },
    {
      "code": "Vuosi",
      "selection": {
        "filter": "item",
        "values": [
          "2015",
          "2016",
          "2017",
          "2018",
          "2019",
          "2020"
        ]
      }
    },
    {
      "code": "Tiedot",
      "selection": {
        "filter": "item",
        "values": [
          "ketjutettu_lv"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}

# Tehdään POST-request ja otetaan vastaus talteen
response = requests.post(API_URL, json=params)

# Muutetaan vastaus json-muotoon
response = response.json()

# Haetaan arvot ja asetetaan ne listaan
values_list = response["value"]

# Haetaan vuodet
years = response["dimension"]["Vuosi"]["category"]["label"]

# Tehdään vuosista uusi sanakirja
years_dict = dict(years)

# Alustetaan uusi lista
years_list = []

# Tallennetaan sanakirjasta löytyvät vuodet listaan
for keys, values in years.items():
    years_list.append(values)

# Luodaan uusi dataframe johon aluksi lisätään vuosilista
df = pd.DataFrame(years_list)

# Annetaan sarakkeelle uusi nimi
df = df.rename(columns={0: "years"})

# Lisätään arvolista dataframeen
df["values"] = values_list

# Dataframe koostuu nyt sarakkeista "years" ja "values"
print(df)

# Tässä vielä sama juttu toiselle API-haulle
API_URL_2 = "https://pxweb2.stat.fi:443/PxWeb/api/v1/fi/StatFin/velk/statfin_velk_pxt_113n.px"
params_2 = {
  "query": [
    {
      "code": "Asuntokunnan rakenne",
      "selection": {
        "filter": "item",
        "values": [
          "s"
        ]
      }
    },
    {
      "code": "Tiedot",
      "selection": {
        "filter": "item",
        "values": [
          "asuvelat"
        ]
      }
    },
    {
      "code": "Vuosi",
      "selection": {
        "filter": "item",
        "values": [
          "2015",
          "2016",
          "2017",
          "2018",
          "2019",
          "2020"
        ]
      }
    },
    {
      "code": "Suuralue",
      "selection": {
        "filter": "item",
        "values": [
          "SSS"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}
response_2 = requests.post(API_URL_2, json=params_2)
response_2 = response_2.json()
values_list_2 = response_2["value"]
years_2 = response_2["dimension"]["Vuosi"]["category"]["label"]
years_list_2 = []
for key, value in years_2.items():
    years_list_2.append(value)
df_2 = pd.DataFrame([years_list_2, values_list_2])
df_2 = df_2.transpose()
df_2 = df_2.rename(columns={0: "years", 1: "values"})
print(df_2)
