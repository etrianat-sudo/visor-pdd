import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np

st.set_page_config(layout="wide")


# LOGO EN SIDEBAR (arriba del menú)
st.sidebar.image("assets/logo_umujer.png", use_container_width=True)

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
territomuni = pd.read_excel(ruta, sheet_name="territoriomuni")



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



######  Titilo #########
st.markdown("""
<h1 style='text-align: left; color: black;'>
🌍 Panorama General de la Desaparición de Mujeres
</h1>
<p style='font-size:18px; color:gray;'>
Una lectura territorial y cuantitativa del fenómeno en Colombia
</p>
""", unsafe_allow_html=True)

# ========================
# KPIs
# ========================

# col1, col2, col3, col4, col5, col6 = st.columns(6)

col1, col2, col3 = st.columns(3)
# primera fila

col4, col5, col6 = st.columns(3)
# segunda fila

col1.markdown(f"""
<div style='background-color:#f3e5f5; padding:20px; border-radius:10px'>
<h3>Total de Personas Dadas por Desaparecidas - PDD</h3>
<h1>{int(universo['total_pdd'][0]):,}</h1>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style='background-color:#ede7f6; padding:20px; border-radius:10px'>
<h3>Total Mujeres desaparecidas</h3>
<h1>{int(universo['mujeres'][0]):,}</h1>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style='background-color:#e1bee7; padding:20px; border-radius:10px'>
<h3>% Mujeres desaparecidas</h3>
<h1>{universo['por_mujeres'][0]*100:.1f}%</h1>
</div>
""", unsafe_allow_html=True)

# KPI 4 
col4.markdown(f"""
<div style='background-color:#f8bbd0; padding:20px; border-radius:10px'>
<h4>Tiempo promedio de desaparecidas</h4>
<h2>{universo['tiempo_prom_mujeres'][0]:.1f} años</h2>
</div>
""", unsafe_allow_html=True)

# KPI 5 
col5.markdown(f"""
<div style='background-color:#f3e5f5; padding:20px; border-radius:10px'>
<h4>Departamento con la mayor proporción de mujeres desaparecidas</h4>
<h2>{universo['dep_mayor_prop'][0]}</h2>
<p>{universo['prop_dep'][0]*100:.1f}%</p>
</div>
""", unsafe_allow_html=True)

# KPI 6 
col6.markdown(f"""
<div style='background-color:#ede7f6; padding:20px; border-radius:10px'>
<h4>Mujeres encontradas </h4>
<h2>{int(universo['mujeres_encontradas'][0]):,}</h2>
<h4> Entrega dignas 78 - Encontradas  con vida 113 </h4>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<small style='color: gray;'>
Personas dadas por desaparecidas en el contexto y razón del conflicto armado en Colombia, 
antes del 1 de diciembre de 2016.
</small>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 📍 Distribución territorial de las desapariciones")

st.markdown("""
<small style='color: gray;'>
Interactúe con el mapa desplazando el cursor sobre los departamentos para visualizar el detalle de la información.
</small>
""", unsafe_allow_html=True)


# ========================
# MAPA
# ========================
st.subheader(" Distribución territorial de las desapariciones, por departamento y municipio de la declaración de desaparición")

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
    height=600,
    margin={"r":0,"t":50,"l":0,"b":0}
)




############################################
#
#      Municipios
#
#######################################

# cargar geojson
with open(get_path("data", "Muni_SIMPLE.geojson"), encoding="utf-8") as f:
    geojson_muni = json.load(f)

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
territomuni["municipio"] = territomuni["municipio"].apply(normalizar_nombre)

# Limpiar el GeoJSON (Usando los nombres que me pasaste)
for feature in geojson_muni["features"]:
        nombre_json = feature["properties"]["mpio_cnmbr"]
        feature["properties"]["mpio_cnmbr"] = normalizar_nombre(nombre_json)

# --- Diagnóstico rápido para que tú lo veas ---
#st.write("Muestra Excel:", territorio["departamento"].unique()[:32])
#st.write("Muestra GeoJSON:", [f["properties"]["DPTO_CNMBR"] for f in geojson["features"][:32]])




# ========================
# MAPA
# ========================


tope_escala = territomuni["total"].quantile(0.9)

fig_map_muni = px.choropleth(
    territomuni,
    geojson=geojson_muni,
    locations="municipio",
    featureidkey="properties.mpio_cnmbr",
    color="total",
    hover_name="municipio",
    hover_data={
        "total": True,
        "mujeres": True,
        "por_mujeres": True
    },
    color_continuous_scale="Purples",
    range_color=[0, tope_escala]
)

fig_map_muni.update_traces(
    marker_line_width=0.8,      # Bordes más gruesos para que se noten
    marker_line_color="white",  
    #marker_opacity=0.9,
    hovertemplate=
    "<b>%{hovertext}</b><br>" +
    "Total PDD: %{customdata[0]}<br>" +
    "Mujeres: %{customdata[1]}<br>" +
    "% Mujeres: %{customdata[2]}%<extra></extra>"
)


fig_map_muni.update_geos(
    fitbounds="locations",
    visible=False
)

fig_map_muni.update_layout(
    height=700,
    margin={"r":0,"t":50,"l":0,"b":0}
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Departamentos")
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("Municipios")
    st.plotly_chart(fig_map_muni, use_container_width=True)



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