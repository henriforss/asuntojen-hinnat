# Lataa tarvittavat kirjastot
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Lataa tiedot
# 112l -- Vanhojen osakeasuntojen hintaindeksi (2015=100) ja kauppojen lukumäärät, vuositasolla, 2015-2021
as_hinnat = pd.read_csv("asuntojen_hinnat2.csv", encoding="ISO 8859-1", sep=";")
as_hinnat = as_hinnat[["Vuosi", "Koko maa"]]
as_hinnat = as_hinnat.rename(columns={"Koko maa": "Indeksi"})

# Lataa tiedot
# 12ij -- Kotitalouden tulot asunnon hallintasuhteen mukaan, 1987-2020
as_tulot = pd.read_csv("kotitalouksien_tulot2.csv", encoding="ISO 8859-1", sep=";")
as_tulot = as_tulot[["Vuosi", "Oma asunto"]]
as_tulot = as_tulot.rename(columns={"Oma asunto": "Tulot"})

# Lataa tiedot
# 113n -- Asuntokuntien velat ja rakenne suuralueittain, vuoden 2020 rahassa, 2002-2020
as_velat_asuntokunta = pd.read_csv("asuntovelat_asuntokunta.csv", encoding="ISO 8859-1", sep=";")
as_velat_asuntokunta = as_velat_asuntokunta[["Vuosi", "Asuntovelat, euroa Yhteensä", "Asuntovelallisia asuntokuntia, lkm Yhteensä"]]
as_velat_asuntokunta = as_velat_asuntokunta.rename(columns={"Asuntovelat, euroa Yhteensä": "Asuntovelka yhteensä", "Asuntovelallisia asuntokuntia, lkm Yhteensä": "Asuntovelallisia lkm"})

# Laske velat/velallinen
as_velat_asuntokunta["Velkaa/velallinen"] = as_velat_asuntokunta["Asuntovelka yhteensä"] / as_velat_asuntokunta["Asuntovelallisia lkm"]

# Muuta tulot indeksimuotoon
as_tulot["Muutos"] = as_tulot["Tulot"] / 55644 * 100

# Alusta kuvaaja
fig = go.Figure()

# Alusta kaksi y-akselia
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Lisää tracet
fig.add_trace(go.Scatter(
  x=as_tulot["Vuosi"],
  y=as_tulot["Muutos"],
  name="Tulot (indeksi)",
  mode="lines",
  line={"color": "#bccad6", "width": 10}
  ),
  secondary_y=True)

fig.add_trace(go.Scatter(
  x=as_hinnat["Vuosi"],
  y=as_hinnat["Indeksi"],
  name="Asuntojen hinnat (indeksi)",
  mode="lines",
  line={"color": "#8d9db6", "width": 10}
  ),
  secondary_y=True)

fig.add_trace(go.Bar(
  x=as_velat_asuntokunta["Vuosi"],
  y=as_velat_asuntokunta["Velkaa/velallinen"],
  name="Asuntovelkaa/velallinen (euroa)",
  width=0.3,
  marker={"color": "#667292"}
  ),
  secondary_y=False)

# Päivitä layoutia
fig.update_layout(
  autosize=False,
  width=1000,
  height=650,
  plot_bgcolor="#f1e3dd",
  title={"text":"Asuntojen hinnat, asuntokuntien tulot ja asuntovelan määrä", "x": 0.478, "font": {"size": 25}},
  xaxis_title="Vuosi",
  legend={"x": 0.585, "y": 0.03, "font": {"size":15}},
  yaxis={"tickformat": ",.0f"}
  )

# Päivitä y-akseleiden layoutia
fig.update_yaxes(title_text="Indeksi", secondary_y=True)
fig.update_yaxes(title_text="Euroa", secondary_y=False)

# Lisää lähde
fig.add_annotation({
  "text": "Lähde: Tilastokeskus.",
  "x": 0.945,
  "y": -0.12,
  "showarrow": False,
  "xref": "paper",
  "yref": "paper",
  "font": {"size": 11}
  })

# Piirrä kuvaaja
fig.show()