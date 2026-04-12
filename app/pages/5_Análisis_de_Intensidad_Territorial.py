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

tasas = pd.read_excel(ruta, sheet_name="tasas")

mov = pd.read_excel(ruta, sheet_name="movimientos")

#  convertir tasa a numérico
tasas["tasa"] = tasas["tasa"].astype(str).str.replace(",", ".").astype(float)

# asegurar código como string (clave para mapas)
tasas["codigo_municipio"] = tasas["codigo_municipio"].astype(str)

#################################
#
#  Titulo
######################

st.title("🧬 Análisis de Intencidad Territorial que presentan la desaparicion de Mujeres")
st.markdown("""
<small style='color: gray;'>
- Las tasas permiten identificar territorios con mayor riesgo relativo.
- Municipios con baja población pueden presentar tasas elevadas.
- Se identifican “hotspots” territoriales persistentes.
- La desaparición presenta dinámicas espaciales complejas entre origen y destino
""", unsafe_allow_html=True)


st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")


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

    equivalencias = {
        "BOGOTA, DC": "BOGOTA",
        "BOGOTA D.C.": "BOGOTA",
        "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA": "SAN ANDRES",
        "SAN ANDRES": "SAN ANDRES",
    }

    return equivalencias.get(texto, texto)
# Limpiar el DataFrame de Excel
tasas["municipio"] = tasas["municipio"].apply(normalizar_nombre)

# Limpiar el GeoJSON (Usando los nombres que me pasaste)
for feature in geojson_muni["features"]:
    feature["properties"]["mpio_cdpmp"] = str(feature["properties"]["mpio_cdpmp"]).zfill(5)


# ========================
# CONTROL PRO (FLECHAS)
# ========================

quinquenios = sorted(tasas["quinquenio"].unique())

# inicializar estado
if "idx_q" not in st.session_state:
    st.session_state.idx_q = 0

col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅️ Anterior"):
        st.session_state.idx_q = max(0, st.session_state.idx_q - 1)

with col3:
    if st.button("Siguiente ➡️"):
        st.session_state.idx_q = min(len(quinquenios)-1, st.session_state.idx_q + 1)

# valor actual
periodo = quinquenios[st.session_state.idx_q]

# título dinámico
st.markdown(
    f"<h4 style='text-align: center;'>🗓️ {periodo}</h4>",
    unsafe_allow_html=True
)

tasas["codigo_municipio"] = tasas["codigo_municipio"].astype(str).str.zfill(5)


df = tasas[tasas["quinquenio"] == periodo]

# ========================
# COMPLETAR MUNICIPIOS (CLAVE)
# ========================

# todos los municipios del geojson
geo_df = pd.DataFrame({
    "codigo_municipio": [f["properties"]["mpio_cdpmp"] for f in geojson_muni["features"]]
})

# unir con tus datos
df_full = geo_df.merge(df, on="codigo_municipio", how="left")

# rellenar valores faltantes
df_full["tasa"] = df_full["tasa"].fillna(0)
df_full["casos"] = df_full["casos"].fillna(0)
df_full["municipio"] = df_full["municipio"].fillna("Sin datos")

# ========================
# RANKING
# ========================

ranking = df.sort_values("tasa", ascending=False).head(15)

fig_rank = px.bar(
    ranking,
    x="tasa",
    y="municipio",
    orientation="h",
    color="tasa",
    color_continuous_scale="Purples"
)

fig_rank.update_traces(
    text=ranking["tasa"].round(2),
    textposition="outside"
)

fig_rank.update_layout(
    yaxis=dict(autorange="reversed"),
    title=f"Top municipios con mayor tasa ({periodo})",
    coloraxis_showscale=False
)

# ========================
# LAYOUT
# ========================

col1, col2 = st.columns([1.2, 1])

# todos los códigos del geojson
geo_codes = set([f["properties"]["mpio_cdpmp"] for f in geojson_muni["features"]])

# todos los códigos del df
df_codes = set(df["codigo_municipio"])

# ver diferencia
#faltantes = geo_codes - df_codes

st.write("Interactúe con el mapa desplazando el cursor sobre este para visualizar el detalle de la información.")
st.write("Tasas de desaparicion por 100 mil Mujeres habitantes del municipio")

with col1:
    st.subheader(f"Mapa de tasas")

    fig_map = px.choropleth(
        df_full,
        geojson=geojson_muni,
        locations="codigo_municipio", 
        featureidkey="properties.mpio_cdpmp", 
        color="tasa",
        color_continuous_scale="Purples",
        hover_data=["municipio", "casos", "tasa"]
    )

    fig_map.update_geos(
    fitbounds="locations",
    visible=False
    )
    
    fig_map.update_layout(height=600)

    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader(f"Top municipios")
    st.plotly_chart(fig_rank, use_container_width=True)



st.markdown("### 📊 Clave de lectura")

st.markdown(f"""
- El ranking muestra los municipios con mayor tasa de desaparición de mujeres en el periodo {periodo}.
- No representa volumen, sino intensidad relativa del fenómeno.
- Municipios con pocos casos pueden aparecer debido a baja población.
- Permite identificar territorios con mayor vulnerabilidad estructural para las Mujeres.
""")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("### 📍 Origen vs Destino")

st.subheader("Relación entre lugar de nacimiento y desaparición de las Mujeres")
# análisis flujo


####################################################
#
#        Novimientos
#
#########################


# mov = mov[mov["casos"] >= 50]

mov["tipo"] = np.where(
    mov["depto_nacimiento"] == mov["depto_desaparicion"],
    "mismo",
    "otro"
)

total_origen = mov.groupby("depto_nacimiento")["casos"].sum().reset_index()
total_origen.columns = ["depto_nacimiento", "total"]

fuera = mov[mov["tipo"] == "otro"] \
    .groupby("depto_nacimiento")["casos"].sum().reset_index()

fuera.columns = ["depto_nacimiento", "casos_fuera"]

df_prop = total_origen.merge(fuera, on="depto_nacimiento", how="left")
df_prop["casos_fuera"] = df_prop["casos_fuera"].fillna(0)

df_prop["porcentaje_salida"] = (
    df_prop["casos_fuera"] / df_prop["total"]
) * 100

top15 = df_prop.sort_values("porcentaje_salida", ascending=False).head(15)

fig = px.bar(
    top15,
    x="porcentaje_salida",
    y="depto_nacimiento",
    orientation="h",
    color="porcentaje_salida",
    color_continuous_scale="Purples",
    labels={
    "porcentaje_salida": "% de salida",   # 👈 CAMBIO CLAVE
    "depto_nacimiento": "Departamento nacimiento"
    }
)

fig.update_traces(
    text=top15["porcentaje_salida"].round(1),
    textposition="outside"
)

fig.update_layout(
    yaxis=dict(autorange="reversed"),
    title="Departamentos donde nacieron con mayor proporción de Mujeres desaparecidas en otros territorios",
    xaxis_title="% de casos fuera del departamento",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("### 📊 Clave de lectura")

st.markdown("""
- Mide la proporción de mujeres que desaparecen fuera de su departamento de nacimiento.
- Identifica territorios con alta movilidad o expulsión.
- No refleja volumen, sino comportamiento territorial.
- Altos valores indican dinámicas interdepartamentales fuertes.
""")



##############################

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")


# ========================
# DESTINOS POR ORIGEN (SOLO LOS QUE SALEN)
# ========================

# 1. Crear tabla de destinos
destinos = (
    mov.groupby(["depto_nacimiento", "depto_desaparicion"])["casos"]
    .sum()
    .reset_index()
)

# 2. Selector de departamento (solo top15)
depto_sel = st.selectbox(
    "Seleccione departamento de nacimiento",
    sorted(top15["depto_nacimiento"])
)

# 3. Obtener porcentaje de salida (del gráfico anterior)
porcentaje_salida = df_prop[
    df_prop["depto_nacimiento"] == depto_sel
]["porcentaje_salida"].values[0]

# 4. Filtrar SOLO los que salen (clave)
df_sel = destinos[
    (destinos["depto_nacimiento"] == depto_sel) &
    (destinos["depto_desaparicion"] != depto_sel)
].copy()

# 5. Calcular porcentaje dentro de los que salen
total_origen = mov[mov["depto_nacimiento"] == depto_sel]["casos"].sum()

df_sel["porcentaje_total"] = (
    df_sel["casos"] / total_origen
) * 100

# 6. Ordenar
df_sel = df_sel.sort_values("porcentaje_total", ascending=False)

# 7. (Opcional pero recomendado) dejar solo los más relevantes
df_sel = df_sel.sort_values("porcentaje_total", ascending=False).head(10)

# 8. Gráfico

fig = px.bar(
    df_sel.sort_values("porcentaje_total", ascending=False),
    x="porcentaje_total",
    y="depto_desaparicion",
    orientation="h",
    color="porcentaje_total",
    color_continuous_scale="Purples",
    labels={
    "porcentaje_total": "% del total",  
    "depto_desaparicion": "Departamento de desaparición"
    }
)

fig.update_traces(
    text=df_sel["porcentaje_total"].round(1),
    textposition="outside"
)

fig.update_layout(
    yaxis=dict(autorange="reversed"),
    title=f"¿En que departamento desaparecio el {porcentaje_salida:.1f}% que nacio en {depto_sel}?",
    xaxis_title="% del total de personas nacidas en el departamento",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


# ========================
# CLAVE DE LECTURA
# ========================

st.markdown("### 📊 Clave de lectura")

st.markdown(f"""
- Del total de Mujeres nacidas en **{depto_sel}**, el **{porcentaje_salida:.1f}%** desaparece fuera del departamento.
- Este gráfico muestra cómo se distribuyen esos casos.
- Los valores representan proporciones dentro del flujo de salida.
- Permite identificar los principales destinos de desaparición.
""")
