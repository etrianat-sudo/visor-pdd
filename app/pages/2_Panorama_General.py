import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np

st.set_page_config(layout="wide")

# ========================
# CARGAR DATOS
# ========================

import os

def get_path(*paths):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base, *paths)

ruta = get_path("data", "data_universo_pdd.xlsx")

universo = pd.read_excel(ruta, sheet_name="universo")
territorio = pd.read_excel(ruta, sheet_name="territorio")



# cargar geojson
with open(get_path("data", "DEPTO_SIMPLE.geojson"), encoding="utf-8") as f:
    geojson = json.load(f)

# st.write("Muestra GeoJSON:", [f["properties"]["dpto_cnmbr"] for f in geojson["features"][:32]])


# ========================
# LIMPIAR DATOS
# ========================
import unicodedata

def normalizar_nombre(texto):
    if not texto:
        return ""
    
    import unicodedata
    
    texto = str(texto).strip().upper()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')

    # 🔥 SOLO equivalencias exactas
    equivalencias = {
        "BOGOTA, DC": "BOGOTA",
        "BOGOTA D.C.": "BOGOTA",
        "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA": "SAN ANDRES",
        "SAN ANDRES": "SAN ANDRES",
    }

    return equivalencias.get(texto, texto)

# Limpiar el DataFrame de Excel
territorio["departamento"] = territorio["departamento"].apply(normalizar_nombre)

# Limpiar el GeoJSON (Usando los nombres que me pasaste)
for feature in geojson["features"]:
        nombre_json = feature["properties"]["dpto_cnmbr"]
        feature["properties"]["dpto_cnmbr"] = normalizar_nombre(nombre_json)

# --- Diagnóstico rápido para que tú lo veas ---
#st.write("Muestra Excel:", territorio["departamento"].unique()[:32])
#st.write("Muestra GeoJSON:", [f["properties"]["DPTO_CNMBR"] for f in geojson["features"][:32]])


# ========================
# KPIs
# ========================
st.title("🌍 Universo de Personas Desaparecidas")

col1, col2, col3 = st.columns(3)

col1.metric("Total PDD", f"{int(universo['total_pdd'][0]):,}")
col2.metric("Total Mujeres", f"{int(universo['mujeres'][0]):,}")
col3.metric("% Mujeres", f"{universo['por_mujeres'][0]*100:.2f}%")

st.markdown("---")



# ========================
# MAPA
# ========================
st.subheader(" Distribución territorial de las desapariciones de Mujeres, por departamento de la declaración de desaparición")

tope_escala = territorio["total"].quantile(0.9)

fig_map = px.choropleth(
    territorio,
    geojson=geojson,
    locations="departamento",
    featureidkey="properties.dpto_cnmbr",
    color="total",
    hover_name="departamento",
    hover_data={
        "total": True,
        "mujeres": True,
        "por_mujeres": True
    },
    color_continuous_scale="Purples",
    range_color=[0, tope_escala]
)

fig_map.update_traces(
    marker_line_width=0.8,      # Bordes más gruesos para que se noten
    marker_line_color="white",  
    #marker_opacity=0.9,
    hovertemplate=
    "<b>%{hovertext}</b><br>" +
    "Total PDD: %{customdata[0]}<br>" +
    "Mujeres: %{customdata[1]}<br>" +
    "% Mujeres: %{customdata[2]}%<extra></extra>"
)


fig_map.update_geos(
    fitbounds="locations",
    visible=False
)

fig_map.update_layout(
    height=700,
    margin={"r":0,"t":50,"l":0,"b":0}
)

st.plotly_chart(fig_map, use_container_width=True)

##################################
#  analisis 
#####################

st.markdown("---")

st.markdown("""
### 📊 Lectura territorial

La distribución de las personas dadas por desaparecidas evidencia una concentración significativa en departamentos con mayor densidad poblacional y dinámicas históricas del conflicto armado.

Territorios como Antioquia, Meta, Valle del Cauca y Bogotá concentran los mayores volúmenes de casos, lo que refleja tanto su tamaño poblacional como su papel en dinámicas de movilidad, control territorial y presencia de actores armados.

Este patrón territorial confirma que la desaparición no fue un fenómeno aislado, sino extendido en regiones estratégicas del país.
""")