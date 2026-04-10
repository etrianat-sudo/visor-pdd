import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide")

# ========================
# CARGAR DATOS
# ========================
ruta = "data/data_universo_pdd.xlsx"

universo = pd.read_excel(ruta, sheet_name="universo")
territorio = pd.read_excel(ruta, sheet_name="territorio")

# cargar geojson
with open("../data/DPTO_POLITICO.geojson", encoding="utf-8") as f:
    geojson = json.load(f)

# ========================
# LIMPIAR DATOS
# ========================
territorio["departamento"] = (
    territorio["departamento"]
    .str.upper()
    .str.replace("BOGOTA D.C.", "BOGOTA", regex=False)
    .str.strip()
)

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
st.subheader("🌎 Distribución territorial de las desapariciones de Mujeres, por departamento de la declaración de desaparición")

fig_map = px.choropleth(
    territorio,
    geojson=geojson,
    locations="departamento",
    featureidkey="properties.DPTO_CNMBR",
    color="total",
    hover_name="departamento",
    hover_data={
        "total": True,
        "mujeres": True,
        "por_mujeres": True

    },
    color_continuous_scale="Purples"
)

fig_map.update_traces(
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
    height=600  # 🔥 hace el mapa grande
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